"""觅图 API 客户端 — 独立版
支持两种格式:
  1. OpenAI 兼容格式: POST /v1/images/generations — 即时返回
  2. Replicate 格式:   POST /replicate/v1/models/{model}/predictions — 异步任务 + 轮询

完全不依赖原项目，可单独使用。
"""

import os
import json as json_module
import time
import base64
import asyncio
import httpx
from pathlib import Path


# ═══════════════════════════════════════════════════════════════════════════
# 尺寸映射表
# ═══════════════════════════════════════════════════════════════════════════

SIZE_MAP = {
    ("1:1", "1"): "1024x1024",   ("1:1", "2"): "2048x2048",   ("1:1", "4"): "4096x4096",
    ("16:9", "1"): "1280x720",   ("16:9", "2"): "2560x1440",  ("16:9", "4"): "3840x2160",
    ("9:16", "1"): "720x1280",   ("9:16", "2"): "1440x2560",  ("9:16", "4"): "2160x3840",
    ("4:3", "1"): "1152x864",    ("4:3", "2"): "2048x1536",   ("4:3", "4"): "4096x3072",
    ("3:4", "1"): "864x1152",    ("3:4", "2"): "1536x2048",   ("3:4", "4"): "3072x4096",
}


def is_replicate_model(model: str) -> bool:
    """判断模型使用 Replicate 格式还是 OpenAI 格式"""
    return model.startswith("black-forest-labs/") or model.startswith("flux-")


def resolve_size(ratio: str, megapixels: str | int) -> str:
    """根据比例和分辨率获取 OpenAI size 字符串"""
    return SIZE_MAP.get((ratio, str(megapixels)), "1024x1024")


# ═══════════════════════════════════════════════════════════════════════════
# 配置加载 (优先级: 命令行参数 > 环境变量 > 当前目录 .env > 脚本目录 .env)
# ═══════════════════════════════════════════════════════════════════════════

def _load_env():
    """从 .env 文件加载配置。
    加载顺序：脚本目录 .env → 根目录 .env
    规则：后加载覆盖先加载；环境变量（脚本运行前已设置）始终保持最高优先级，不会被任何文件覆盖。
    """
    # 记录脚本运行前已存在的环境变量，这些绝不被覆盖
    pre_existing = set(os.environ.keys())

    candidates = [
        Path.cwd() / ".env",                              # 运行脚本的当前目录
        Path(__file__).resolve().parent / ".env",          # 脚本所在目录（最高文件优先级）
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
                            # 跳过空值；预置环境变量不可覆盖
                            if not val:
                                continue
                            if key not in pre_existing:
                                os.environ[key] = val
            except PermissionError:
                import sys as _sys
                print(f"[WARN] 无法读取配置文件 {env_file}（权限不足）", file=_sys.stderr)
            except UnicodeError:
                import sys as _sys
                print(f"[WARN] 配置文件 {env_file} 编码异常，已跳过", file=_sys.stderr)
            except Exception:
                import sys as _sys
                print(f"[WARN] 读取配置文件 {env_file} 时发生未知错误", file=_sys.stderr)


_load_env()


def get_config():
    """获取配置字典"""
    return {
        "api_key": os.getenv("YUNWU_API_KEY", ""),
        "base_url": os.getenv("YUNWU_BASE_URL", "https://yunwu.ai"),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 异常定义
# ═══════════════════════════════════════════════════════════════════════════

class MituAPIError(Exception):
    """API 错误，携带完整请求/响应信息"""

    def __init__(self, message: str, request_info: dict = None, response_info: dict = None):
        super().__init__(message)
        self.request_info = request_info or {}
        self.response_info = response_info or {}

    def to_dict(self) -> dict:
        return {
            "error": str(self),
            "request": self.request_info,
            "response": self.response_info,
        }


# ═══════════════════════════════════════════════════════════════════════════
# API 客户端
# ═══════════════════════════════════════════════════════════════════════════

class MituClient:
    """觅图 API 客户端 — 异步"""

    def __init__(self, api_key: str = "", base_url: str = ""):
        config = get_config()
        self.api_key = api_key or config["api_key"]
        self.base_url = (base_url or config["base_url"]).rstrip("/")
        self._timeout = 500.0

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    @staticmethod
    def _safe_json(resp, req_info: dict) -> dict:
        """安全解析 JSON 响应"""
        resp_info = {
            "status": resp.status_code,
            "headers": dict(resp.headers),
            "body": resp.text[:2000],
        }
        try:
            return resp.json()
        except (json_module.JSONDecodeError, ValueError) as e:
            raise MituAPIError(
                f"API 返回非 JSON 响应 ({resp.status_code}): {resp.text[:300]}",
                request_info=req_info,
                response_info=resp_info,
            ) from e

    # ── OpenAI 格式：文生图 ──────────────────────────────────────

    async def openai_generate(self, prompt: str, model: str = "gpt-image-2",
                               size: str = "1024x1024", n: int = 1) -> dict:
        """调用 OpenAI 兼容的 /v1/images/generations 接口（即时返回）"""
        payload = {"model": model, "prompt": prompt, "n": n, "size": size}
        url = f"{self.base_url}/v1/images/generations"
        req_info = {
            "method": "POST", "url": url,
            "headers": {k: v[:50] for k, v in self._headers().items()},
            "body": payload,
        }

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.post(url, headers=self._headers(), json=payload)
        except httpx.TimeoutException as e:
            raise MituAPIError(f"OpenAI 生图超时（超过 {self._timeout}s），请降低分辨率或重试", request_info=req_info) from e
        except httpx.ConnectError as e:
            raise MituAPIError(f"无法连接 API 服务器，请检查 Base URL 和网络", request_info=req_info) from e
        except httpx.HTTPError as e:
            raise MituAPIError(f"网络请求异常: {e}", request_info=req_info) from e

        if resp.status_code != 200:
            raise MituAPIError(
                f"OpenAI 生图失败 ({resp.status_code}): {resp.text[:500]}",
                request_info=req_info,
                response_info={"status": resp.status_code, "headers": dict(resp.headers), "body": resp.text[:2000]},
            )

        return self._safe_json(resp, req_info)

    # ── Replicate 格式：异步任务 ─────────────────────────────────

    async def create_prediction(self, prompt: str, aspect_ratio: str = "1:1",
                                 megapixels: str = "1", num_outputs: int = 1,
                                 output_format: str = "jpg", output_quality: int = 80,
                                 num_inference_steps: int = 4,
                                 model: str = "black-forest-labs/flux-schnell") -> dict:
        """创建 Replicate 格式预测任务"""
        payload = {
            "input": {
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "megapixels": megapixels,
                "num_outputs": num_outputs,
                "output_format": output_format,
                "output_quality": output_quality,
                "num_inference_steps": num_inference_steps,
            }
        }

        url = f"{self.base_url}/replicate/v1/models/{model}/predictions"
        req_info = {"method": "POST", "url": url, "headers": {k: v[:50] for k, v in self._headers().items()}, "body": payload}

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.post(url, headers=self._headers(), json=payload)
        except httpx.TimeoutException as e:
            raise MituAPIError(f"创建任务超时，请重试", request_info=req_info) from e
        except httpx.ConnectError as e:
            raise MituAPIError(f"无法连接 API 服务器", request_info=req_info) from e
        except httpx.HTTPError as e:
            raise MituAPIError(f"网络请求异常: {e}", request_info=req_info) from e

        if resp.status_code not in (200, 201):
            raise MituAPIError(
                f"创建任务失败 ({resp.status_code}): {resp.text[:500]}",
                request_info=req_info,
                response_info={"status": resp.status_code, "headers": dict(resp.headers), "body": resp.text[:2000]},
            )

        return self._safe_json(resp, req_info)

    async def get_prediction(self, task_id: str) -> dict:
        """查询 Replicate 格式预测任务状态"""
        url = f"{self.base_url}/replicate/v1/predictions/{task_id}"
        req_info = {"method": "GET", "url": url}

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.get(url, headers=self._headers())
        except httpx.TimeoutException as e:
            raise MituAPIError(f"查询任务超时", request_info=req_info) from e
        except httpx.ConnectError as e:
            raise MituAPIError(f"无法连接 API 服务器", request_info=req_info) from e
        except httpx.HTTPError as e:
            raise MituAPIError(f"网络请求异常: {e}", request_info=req_info) from e

        if resp.status_code != 200:
            raise MituAPIError(
                f"查询任务失败 ({resp.status_code}): {resp.text[:500]}",
                request_info=req_info,
                response_info={"status": resp.status_code, "headers": dict(resp.headers), "body": resp.text[:2000]},
            )

        return self._safe_json(resp, req_info)

    async def wait_for_completion(self, task_id: str, on_progress=None,
                                   poll_interval: float = 0.8) -> dict:
        """轮询等待 Replicate 任务完成"""
        t0 = time.time()

        while True:
            data = await self.get_prediction(task_id)
            status = data.get("status", "")

            if on_progress:
                on_progress({
                    "status": status,
                    "logs": data.get("logs", ""),
                    "elapsed": time.time() - t0,
                })

            if status in ("succeeded", "failed", "canceled"):
                data["_elapsed"] = time.time() - t0
                return data

            if time.time() - t0 > 500:
                raise MituAPIError("任务超时 (500s)")

            await asyncio.sleep(poll_interval)

    # ── OpenAI 格式：图生图编辑 ────────────────────────────────────

    async def edit_image(self, image_data: bytes, prompt: str,
                          filename: str = "image.png",
                          model: str = "gpt-image-2",
                          mask_data: bytes | None = None,
                          mask_filename: str = "mask.png",
                          n: int = 1, size: str = "1024x1024",
                          quality: str = "auto", background: str = "auto") -> dict:
        """调用 OpenAI 兼容的 /v1/images/edits 接口（multipart 上传）"""
        url = f"{self.base_url}/v1/images/edits"

        req_info = {
            "method": "POST", "url": url,
            "body": {"prompt": prompt, "model": model, "n": n, "size": size,
                     "quality": quality, "background": background, "image_size": len(image_data)},
        }

        files = {
            "image": (filename, image_data, "image/png"),
            "prompt": (None, prompt),
            "model": (None, model),
            "n": (None, str(n)),
            "size": (None, size),
            "quality": (None, quality),
            "background": (None, background),
        }

        if mask_data:
            files["mask"] = (mask_filename, mask_data, "image/png")
            req_info["body"]["mask_size"] = len(mask_data)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.post(url, headers=headers, files=files)
        except httpx.TimeoutException as e:
            raise MituAPIError(f"图生图超时，请降低分辨率或重试", request_info=req_info) from e
        except httpx.ConnectError as e:
            raise MituAPIError(f"无法连接 API 服务器", request_info=req_info) from e
        except httpx.HTTPError as e:
            raise MituAPIError(f"网络请求异常: {e}", request_info=req_info) from e

        if resp.status_code != 200:
            raise MituAPIError(
                f"图生图编辑失败 ({resp.status_code}): {resp.text[:500]}",
                request_info=req_info,
                response_info={"status": resp.status_code, "headers": dict(resp.headers), "body": resp.text[:2000]},
            )

        return self._safe_json(resp, req_info)

    # ── OpenAI 格式：多图参考生成 ─────────────────────────────────

    async def reference_generate(self, prompt: str, image_urls: list[str],
                                  model: str = "gpt-image-2-all",
                                  size: str = "1024x1024", n: int = 1) -> dict:
        """调用 gpt-image-2-all 多图参考生成接口"""
        payload = {
            "model": model, "prompt": prompt, "n": n, "size": size,
            "image": image_urls,
        }

        url = f"{self.base_url}/v1/images/generations"
        req_info = {"method": "POST", "url": url, "headers": {k: v[:50] for k, v in self._headers().items()}, "body": payload}

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.post(url, headers=self._headers(), json=payload)
        except httpx.TimeoutException as e:
            raise MituAPIError(f"多图参考生成超时，请重试", request_info=req_info) from e
        except httpx.ConnectError as e:
            raise MituAPIError(f"无法连接 API 服务器", request_info=req_info) from e
        except httpx.HTTPError as e:
            raise MituAPIError(f"网络请求异常: {e}", request_info=req_info) from e

        if resp.status_code != 200:
            raise MituAPIError(
                f"多图参考生成失败 ({resp.status_code}): {resp.text[:500]}",
                request_info=req_info,
                response_info={"status": resp.status_code, "headers": dict(resp.headers), "body": resp.text[:2000]},
            )

        return self._safe_json(resp, req_info)


# ═══════════════════════════════════════════════════════════════════════════
# 图片下载/保存工具
# ═══════════════════════════════════════════════════════════════════════════

async def download_image(url: str, save_dir: str, filename_prefix: str, index: int) -> str | None:
    """从 URL 下载图片到本地，返回保存路径"""
    os.makedirs(save_dir, exist_ok=True)

    ext = url.split(".")[-1].split("?")[0] or "jpg"
    if ext not in ("jpg", "jpeg", "png", "webp", "gif", "bmp"):
        ext = "jpg"
    filepath = os.path.join(save_dir, f"{filename_prefix}_{index}.{ext}")

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            with open(filepath, "wb") as f:
                f.write(resp.content)
            return filepath
        except Exception as e:
            print(f"  ⚠ 下载图片失败 {url}: {e}")
            return None


def save_base64_image(b64_json: str, save_dir: str, filename_prefix: str, index: int) -> str | None:
    """保存 base64 编码的图片到本地，返回保存路径"""
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, f"{filename_prefix}_{index}.png")

    try:
        raw = base64.b64decode(b64_json)
        with open(filepath, "wb") as f:
            f.write(raw)
        return filepath
    except Exception as e:
        print(f"  ⚠ 保存 base64 图片失败: {e}")
        return None
