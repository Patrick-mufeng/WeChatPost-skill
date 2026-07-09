#!/usr/bin/env python
"""Video download + audio extraction + Whisper transcription pipeline.

Two download paths:
  1. parse-video-py (Douyin, Bilibili, Xiaohongshu, Kuaishou) — no cookies needed
  2. yt-dlp fallback (YouTube, international platforms, or when --ytdlp is passed)

Usage:
    python scripts/transcribe.py --url "<url>" [--model tiny] [--asr whisper|volc] [--json]
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import asdict, is_dataclass
from pathlib import Path
from urllib.parse import urlparse


SCRIPT_DIR = Path(__file__).resolve().parent
VENDOR_DIR = SCRIPT_DIR / "vendor"
if VENDOR_DIR.exists():
    sys.path.insert(0, str(VENDOR_DIR))


DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

WHISPER_MODELS = ["tiny", "base", "small", "medium", "large"]

# Platforms supported by parse-video-py (no cookies needed)
PARSE_VIDEO_PLATFORMS = {
    "douyin": "douyin",
    "v.douyin": "douyin",
    "bilibili": "bilibili",
    "b23.tv": "bilibili",
    "xiaohongshu": "xiaohongshu",
    "xhslink": "xiaohongshu",
    "kuaishou": "kuaishou",
    "v.kuaishou": "kuaishou",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def to_plain(value):
    """Convert dataclass to plain dict."""
    if is_dataclass(value):
        return {k: to_plain(v) for k, v in asdict(value).items()}
    if isinstance(value, dict):
        return {k: to_plain(v) for k, v in value.items()}
    if isinstance(value, list):
        return [to_plain(v) for v in value]
    return value


def looks_like_direct_media_url(url: str) -> bool:
    """Check if URL is a direct media/play URL."""
    parsed = urlparse(url)
    path = parsed.path.lower()
    if path.endswith((".mp4", ".m4a", ".mp3", ".wav")):
        return True
    if "mime_type=video_mp4" in parsed.query:
        return True
    if "douyinvod.com" in parsed.netloc.lower() or "bilivideo.com" in parsed.netloc.lower():
        return True
    if parsed.netloc.lower() == "www.douyin.com" and path.startswith("/aweme/v1/play/"):
        return True
    return False


def detect_parse_video_platform(url: str) -> str | None:
    """Detect if URL is from a parse-video-py supported platform."""
    url_lower = url.lower()
    for keyword, platform in PARSE_VIDEO_PLATFORMS.items():
        if keyword in url_lower:
            return platform
    return None


# Platform name mapping: internal key → 飞书表格 option
PLATFORM_MAP = {
    "douyin": "抖音",
    "bilibili": "B站",
    "xiaohongshu": "小红书",
    "kuaishou": "其他平台",
    "youtube": "油管",
    "youtu.be": "油管",
    "tiktok": "其他平台",
}


def detect_platform(url: str) -> str:
    """Detect platform from URL, return 飞书表格 option name."""
    url_lower = url.lower()
    for keyword, name in PLATFORM_MAP.items():
        if keyword in url_lower:
            return name
    return "其他平台"


# ---------------------------------------------------------------------------
# Path 1: parse-video-py (Douyin, Bilibili, Xiaohongshu, Kuaishou)
# ---------------------------------------------------------------------------

async def parse_video_share(url: str) -> dict:
    """Parse video share URL with parse-video-py, return metadata + direct video_url."""
    from parse_video_py import parse_video_share_url
    from parse_video_py.utils import extract_url

    url = extract_url(url)
    info = await parse_video_share_url(url)
    result = to_plain(info)
    result["source_url"] = url
    result["direct_media"] = False
    return result


def download_direct(url: str, out_path: Path) -> Path:
    """Download with httpx (for direct media URLs, no cookies needed)."""
    import httpx

    headers = {"User-Agent": DEFAULT_UA, "Referer": "https://www.douyin.com/"}
    with httpx.Client(follow_redirects=True, timeout=120, headers=headers) as client:
        with client.stream("GET", url) as response:
            response.raise_for_status()
            with out_path.open("wb") as f:
                for chunk in response.iter_bytes():
                    if chunk:
                        f.write(chunk)
    if out_path.stat().st_size == 0:
        raise RuntimeError("Downloaded file is empty")
    return out_path


# ---------------------------------------------------------------------------
# Path 2: yt-dlp fallback (YouTube, international platforms)
# ---------------------------------------------------------------------------

def download_ytdlp(url: str, out_dir: Path, cookies_from_browser: str | None = None, cookies_file: str | None = None) -> dict:
    """Download video with yt-dlp and return metadata dict."""
    output_template = str(out_dir / "%(title).100s.%(ext)s")

    cmd = [
        "yt-dlp",
        "--no-playlist",
        "--print-json",
        "--no-simulate",
        "-o", output_template,
    ]

    if cookies_from_browser:
        cmd.extend(["--cookies-from-browser", cookies_from_browser])
    elif cookies_file:
        cmd.extend(["--cookies", cookies_file])

    cmd.append(url)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

    if result.returncode != 0:
        stderr = result.stderr[-500:] if len(result.stderr) > 500 else result.stderr
        raise RuntimeError(f"yt-dlp download failed: {stderr}")

    lines = [l for l in result.stdout.strip().split("\n") if l.strip()]
    if not lines:
        raise RuntimeError("yt-dlp produced no output")

    meta = json.loads(lines[-1])
    ext = meta.get("ext", "mp4")
    title = meta.get("title", "video")
    safe_title = "".join(c for c in title if c.isalnum() or c in " ._-")[:100]
    video_path = out_dir / f"{safe_title}.{ext}"

    if not video_path.exists():
        candidates = list(out_dir.glob(f"*.{ext}"))
        if candidates:
            video_path = candidates[0]
        else:
            raise RuntimeError(f"Downloaded file not found in {out_dir}")

    return {
        "title": title,
        "duration": meta.get("duration", 0),
        "uploader": meta.get("uploader", ""),
        "description": meta.get("description", "")[:500],
        "video_path": str(video_path),
        "ext": ext,
    }


# ---------------------------------------------------------------------------
# FFmpeg: extract audio
# ---------------------------------------------------------------------------

def extract_audio(video_path: Path, audio_path: Path, ffmpeg_bin: str = "ffmpeg") -> Path:
    """Extract mono 16kHz WAV audio from video."""
    cmd = [
        ffmpeg_bin,
        "-y",
        "-i", str(video_path),
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        str(audio_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg audio extraction failed: {result.stderr[-500:]}")

    if not audio_path.exists() or audio_path.stat().st_size == 0:
        raise RuntimeError("Audio file is empty or missing")

    return audio_path


# ---------------------------------------------------------------------------
# Whisper: transcribe
# ---------------------------------------------------------------------------

def transcribe_whisper(audio_path: Path, model_name: str = "tiny", language: str = "zh") -> str:
    """Transcribe audio with local Whisper model."""
    import whisper

    model = whisper.load_model(model_name)
    result = model.transcribe(str(audio_path), language=language, fp16=False)
    return result.get("text", "").strip()


# ---------------------------------------------------------------------------
# Volcengine ASR (stub)
# ---------------------------------------------------------------------------

def transcribe_volcengine(audio_path: Path) -> str:
    """Transcribe audio with Volcengine ASR API."""
    raise NotImplementedError(
        "Volcengine ASR not yet implemented. "
        "Set VOLC_ACCESS_KEY and VOLC_SECRET_KEY, then implement the ASR call."
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download video and transcribe audio to text."
    )
    parser.add_argument("--url", required=True, help="Video URL (share link or direct media URL).")
    parser.add_argument(
        "--asr",
        choices=["whisper", "volc"],
        default="whisper",
        help="ASR engine (default: whisper).",
    )
    parser.add_argument(
        "--model",
        default="tiny",
        choices=WHISPER_MODELS,
        help="Whisper model size (default: tiny).",
    )
    parser.add_argument("--language", default="zh", help="Audio language (default: zh).")
    parser.add_argument(
        "--ffmpeg",
        default="ffmpeg",
        help="Path to ffmpeg executable.",
    )
    parser.add_argument("--keep-temp", action="store_true", help="Keep temporary files.")
    parser.add_argument("--cookies-from-browser", default=None, help="Browser for yt-dlp cookies (e.g. chrome).")
    parser.add_argument("--cookies", default=None, help="Path to cookies.txt for yt-dlp.")
    parser.add_argument("--ytdlp", action="store_true", help="Force use yt-dlp instead of parse-video-py.")
    parser.add_argument("--output-dir", default=None, help="Output directory for saving transcript files. Creates subfolder: {title}_{date}/")
    parser.add_argument("--json", action="store_true", help="Output JSON (default when piped).")

    args = parser.parse_args()
    use_json = args.json or not sys.stdout.isatty()

    # Ensure ffmpeg is on PATH for Whisper's internal load_audio
    ffmpeg_dir = str(Path(args.ffmpeg).parent) if args.ffmpeg != "ffmpeg" else ""
    if ffmpeg_dir and ffmpeg_dir not in os.environ.get("PATH", ""):
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

    try:
        temp_ctx = None
        if args.keep_temp:
            temp_dir = Path(tempfile.mkdtemp(prefix="wechatpost-"))
        else:
            temp_ctx = tempfile.TemporaryDirectory(prefix="wechatpost-")
            temp_dir = Path(temp_ctx.name)

        # --- Step 1: Get video URL and metadata ---
        meta = {}
        video_url = ""

        if args.ytdlp:
            # Force yt-dlp path
            meta = download_ytdlp(args.url, temp_dir, args.cookies_from_browser, args.cookies)
            video_path = Path(meta["video_path"])
        elif looks_like_direct_media_url(args.url):
            # Direct media URL — download with httpx
            video_path = temp_dir / "video.mp4"
            download_direct(args.url, video_path)
            meta = {"title": "video", "duration": 0, "uploader": ""}
        elif detect_parse_video_platform(args.url):
            # Platforms supported by parse-video-py
            if not use_json:
                print(f"[1/4] Parsing video link...", file=sys.stderr)
            parsed = asyncio.run(parse_video_share(args.url))
            video_url = parsed.get("video_url", "")
            if not video_url:
                raise RuntimeError("No video_url found. This may be an image-only post.")
            meta = {
                "title": parsed.get("title", ""),
                "uploader": parsed.get("author", {}).get("name", ""),
                "cover_url": parsed.get("cover_url", ""),
                "duration": 0,
            }
            # Download with httpx
            if not use_json:
                print(f"[2/4] Downloading video...", file=sys.stderr)
            video_path = temp_dir / "video.mp4"
            download_direct(video_url, video_path)
        else:
            # Fallback to yt-dlp for other platforms (YouTube, etc.)
            meta = download_ytdlp(args.url, temp_dir, args.cookies_from_browser, args.cookies)
            video_path = Path(meta["video_path"])

        # --- Step 2: Extract audio ---
        if not use_json:
            print(f"[3/4] Extracting audio...", file=sys.stderr)
        audio_path = temp_dir / "audio.wav"
        extract_audio(video_path, audio_path, args.ffmpeg)

        # --- Step 3: Transcribe ---
        if not use_json:
            print(f"[4/4] Transcribing with {args.asr}...", file=sys.stderr)
        if args.asr == "volc":
            transcript = transcribe_volcengine(audio_path)
        else:
            transcript = transcribe_whisper(audio_path, args.model, args.language)

        # --- Cleanup ---
        if not args.keep_temp:
            video_path.unlink(missing_ok=True)
            audio_path.unlink(missing_ok=True)

        # --- Save output files ---
        output_dir = ""
        if args.output_dir:
            from datetime import datetime
            safe_title = "".join(c for c in meta.get("title", "untitled") if c.isalnum() or c in " ._-#（）()")[:40].strip()
            date_str = datetime.now().strftime("%Y-%m-%d")
            folder_name = f"{safe_title}_{date_str}" if safe_title else f"video_{date_str}"
            out_path = Path(args.output_dir) / folder_name
            out_path.mkdir(parents=True, exist_ok=True)

            # metadata.json
            meta_out = {
                "title": meta.get("title", ""),
                "uploader": meta.get("uploader", ""),
                "duration": meta.get("duration", 0),
                "cover_url": meta.get("cover_url", ""),
                "source_url": args.url,
                "transcribed_at": datetime.now().isoformat(),
            }
            (out_path / "metadata.json").write_text(json.dumps(meta_out, ensure_ascii=False, indent=2), encoding="utf-8")

            # transcript_raw.txt
            (out_path / "transcript_raw.txt").write_text(transcript, encoding="utf-8")

            # transcript_corrected.txt (placeholder — filled by LLM correction step)
            (out_path / "transcript_corrected.txt").write_text(
                "# 此文件待 LLM 纠错后覆盖\n# 原始转录见 transcript_raw.txt\n", encoding="utf-8"
            )

            output_dir = str(out_path)

        # --- Output ---
        output = {
            "title": meta.get("title", ""),
            "duration": meta.get("duration", 0),
            "uploader": meta.get("uploader", ""),
            "platform": detect_platform(args.url),
            "transcript": transcript,
            "transcript_length": len(transcript),
            "output_dir": output_dir,
            "keep_temp_dir": str(temp_dir) if args.keep_temp else None,
        }

        if use_json:
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            print(f"标题: {output['title']}")
            print(f"作者: {output['uploader']}")
            print(f"---")
            print(transcript)

        return 0

    except Exception as exc:
        message = str(exc) or exc.__class__.__name__
        if use_json:
            print(json.dumps({"error": message}, ensure_ascii=False))
        else:
            print(f"ERROR: {message}", file=sys.stderr)
        return 1
    finally:
        if temp_ctx is not None:
            temp_ctx.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
