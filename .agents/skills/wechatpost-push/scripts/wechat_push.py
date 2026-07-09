#!/usr/bin/env python3
"""
WeChatPost 公众号推送脚本
将排版后的文章推送到微信公众号草稿箱。

用法:
    python wechat_push.py <文章目录>

示例:
    python wechat_push.py "outputs/DeepSeek价格战_2026-07-09/article"

前置:
    - 项目根目录 .env 中配置 WECHAT_APPID / WECHAT_APPSECRET
    - 文章目录下须有 final.md / output.html / cover/cover-combined.png

API 文档:
    https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Add_draft.html
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API_BASE = "https://api.weixin.qq.com"
API_PATH = "/cgi-bin"


# ═══════════════════════════════════════════════════════════════
# 配置加载
# ═══════════════════════════════════════════════════════════════

def load_env() -> dict:
    """从项目根目录 .env 加载微信凭证"""
    candidates = [
        Path.cwd() / ".env",
        Path(__file__).resolve().parent.parent.parent.parent.parent / ".env",
    ]
    for env_file in candidates:
        if env_file.exists():
            try:
                with open(env_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, _, val = line.partition("=")
                            key = key.strip()
                            val = val.strip()
                            if val and key not in os.environ:
                                os.environ[key] = val
            except Exception:
                pass

    return {
        "appid": os.environ.get("WECHAT_APPID", ""),
        "appsecret": os.environ.get("WECHAT_APPSECRET", ""),
    }


# ═══════════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════════

def log(msg: str):
    print(f"[·] {msg}", file=sys.stderr)

def ok(msg: str):
    print(f"✅ {msg}", file=sys.stderr)

def err(msg: str):
    print(f"❌ {msg}", file=sys.stderr)
    sys.exit(1)


def _is_network_error(e: BaseException) -> bool:
    if isinstance(e, urllib.error.URLError):
        return True
    if isinstance(e, TimeoutError):
        return True
    if isinstance(e, urllib.error.HTTPError) and e.code and e.code >= 500:
        return True
    return False


def _api_get(url: str) -> dict:
    for attempt in range(2):
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read())
        except Exception as e:
            if attempt == 0 and _is_network_error(e):
                log("网络请求失败，1秒后重试...")
                time.sleep(1)
                continue
            raise


def _api_post_json(url: str, body: dict) -> dict:
    payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
    for attempt in range(2):
        try:
            req = urllib.request.Request(
                url, data=payload, headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read())
        except Exception as e:
            if attempt == 0 and _is_network_error(e):
                log("网络请求失败，1秒后重试...")
                time.sleep(1)
                continue
            raise


def _upload_file(url: str, file_path: str, field_name: str = "media") -> dict:
    """multipart/form-data 文件上传（纯标准库）"""
    boundary = f"----WechatPush{int(time.time() * 1000)}"
    path = Path(file_path)
    if not path.exists():
        err(f"文件不存在: {file_path}")

    with open(path, "rb") as f:
        file_data = f.read()

    filename = path.name
    mime_type = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"

    body = bytearray()
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(
        f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'.encode("utf-8")
    )
    body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
    body.extend(file_data)
    body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    req = urllib.request.Request(
        url,
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )

    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read())
        except Exception as e:
            if attempt == 0 and _is_network_error(e):
                log("上传网络失败，1秒后重试...")
                time.sleep(1)
                continue
            raise


# ═══════════════════════════════════════════════════════════════
# 微信 API
# ═══════════════════════════════════════════════════════════════

def get_access_token(appid: str, appsecret: str) -> str:
    """获取 access_token（有效期 2 小时，进程内使用不缓存）"""
    url = (
        f"{API_BASE}{API_PATH}/token?"
        f"grant_type=client_credential&appid={appid}&secret={appsecret}"
    )
    data = _api_get(url)
    if "access_token" not in data:
        errcode = data.get("errcode", -1)
        hint = ""
        if errcode in (40013, 40125, 40164):
            hint = "（AppID/AppSecret 错误或 IP 未加白名单）"
        elif errcode == -1:
            hint = f"（系统繁忙或网络问题: {data}）"
        err(f"获取 access_token 失败: errcode={errcode} {hint}")
    return data["access_token"]


def upload_cover(token: str, image_path: str) -> dict:
    """上传封面图为永久素材，返回 {media_id, url}"""
    log(f"上传封面: {image_path}")
    url = f"{API_BASE}{API_PATH}/material/add_material?access_token={token}&type=image"
    data = _upload_file(url, image_path)
    if "media_id" not in data:
        err(f"上传封面失败: {data}")
    ok(f"封面上传成功: media_id={data['media_id']}")
    return {"media_id": data["media_id"], "url": data.get("url", "")}


def create_draft(
    token: str,
    title: str,
    author: str,
    digest: str,
    content: str,
    thumb_media_id: str,
) -> str:
    """创建草稿，返回 media_id"""
    log("创建草稿...")
    url = f"{API_BASE}{API_PATH}/draft/add?access_token={token}"
    body = {
        "articles": [
            {
                "title": title,
                "author": author,
                "digest": digest,
                "content": content,
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 0,
                "only_fans_can_comment": 0,
            }
        ]
    }
    data = _api_post_json(url, body)
    if "media_id" not in data:
        errcode = data.get("errcode", -1)
        errmsg = data.get("errmsg", str(data))
        hints = {
            40001: "access_token 无效或已过期",
            40007: "media_id 无效",
            40014: "access_token 无效",
            40132: "微信号不合法",
            41001: "缺少 access_token 参数",
            42001: "access_token 超时",
            44002: "POST 数据包为空",
            45009: "接口调用频率超限",
            45166: "正文内容包含不支持的标签或格式",
        }
        hint = hints.get(errcode, "")
        if hint:
            hint = f"（{hint}）"
        err(f"创建草稿失败: errcode={errcode} errmsg={errmsg} {hint}")
    ok(f"草稿创建成功: media_id={data['media_id']}")
    return data["media_id"]


# ═══════════════════════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════════════════════

def push(article_dir: str) -> dict:
    """一键推送到公众号草稿箱。

    参数:
        article_dir: 文章目录路径（含 final.md / output.html / cover/cover-combined.png）

    返回:
        {"success": True, "media_id": "xxx", "title": "..."}
    """
    article = Path(article_dir)
    if not article.is_dir():
        err(f"文章目录不存在: {article_dir}")

    # 1. 加载凭证
    config = load_env()
    appid = config["appid"]
    appsecret = config["appsecret"]
    if not appid or not appsecret:
        err(
            "WECHAT_APPID 或 WECHAT_APPSECRET 未配置。\n"
            "请在项目根目录 .env 中设置:\n"
            "  WECHAT_APPID=wx1234567890\n"
            "  WECHAT_APPSECRET=your-secret\n\n"
            "获取方式: 公众号后台 → 设置与开发 → 基本配置"
        )

    # 2. 读取元数据
    final_md = article / "final.md"
    if not final_md.exists():
        err(f"未找到 final.md: {final_md}")

    frontmatter = _parse_frontmatter(final_md)
    title = frontmatter.get("title", article.parent.name)
    author = frontmatter.get("author", "")
    summary = frontmatter.get("summary", "")

    if not title:
        err("final.md 中未找到 title")
    if not author:
        log("final.md 中未找到 author，将使用空作者名")

    # 3. 读取正文
    output_html = article / "output.html"
    if not output_html.exists():
        err(f"未找到 output.html: {output_html}")
    content = output_html.read_text(encoding="utf-8")

    # 4. 封面
    cover_path = article / "cover" / "cover-combined.png"
    if not cover_path.exists():
        err(f"未找到封面图: {cover_path}")

    # 5. 换 token → 上传封面 → 创建草稿
    log(f"文章: {title}")
    log(f"作者: {author or '(未设置)'}")
    token = get_access_token(appid, appsecret)
    thumb = upload_cover(token, str(cover_path))
    media_id = create_draft(token, title, author, summary, content, thumb["media_id"])

    result = {
        "success": True,
        "media_id": media_id,
        "title": title,
        "author": author,
    }
    print(json.dumps(result, ensure_ascii=False))
    return result


def _parse_frontmatter(md_path: Path) -> dict:
    """解析 Markdown 文件的 YAML frontmatter"""
    text = md_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}

    end = text.find("---", 3)
    if end == -1:
        return {}

    raw = text[3:end].strip()
    result = {}
    for line in raw.split("\n"):
        line = line.strip()
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and val:
                result[key] = val
    return result


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python wechat_push.py <文章目录>", file=sys.stderr)
        print('示例: python wechat_push.py "outputs/DeepSeek价格战_2026-07-09/article"', file=sys.stderr)
        sys.exit(1)

    push(sys.argv[1])
