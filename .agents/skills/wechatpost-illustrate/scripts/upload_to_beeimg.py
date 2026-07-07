#!/usr/bin/env python3
"""beeimg 图床上传脚本（Lsky Pro API）
将本地图片上传到 beeimg 图床，返回公开访问 URL。

用法:
    python upload_to_beeimg.py --file "illustrations/01-xxx.png"
    python upload_to_beeimg.py --file "illustrations/01-xxx.png" --permission 1
    python upload_to_beeimg.py --file "img.png" --token "Bearer xxx" --base-url "https://www.beeimg.cn"

依赖: httpx
API: Lsky Pro (兰空图床) — POST /api/v1/upload
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import httpx
except ImportError:
    print(json.dumps({"success": False, "error": "缺少依赖 httpx，请执行: pip install httpx"}))
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════
# 配置加载（与 mitu_client.py 一致）
# ═══════════════════════════════════════════════════════════════════════════

def load_config() -> dict:
    """从环境变量和 .env 文件加载 beeimg 配置"""
    # 先尝试加载 .env 文件
    candidates = [
        Path.cwd() / ".env",
        Path.cwd() / ".grindraft" / "config.env",
        Path(__file__).resolve().parent / ".env",
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
        "token": os.environ.get("BEEIMG_TOKEN", ""),
        "base_url": os.environ.get("BEEIMG_BASE_URL", "https://www.beeimg.cn").rstrip("/"),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 上传函数
# ═══════════════════════════════════════════════════════════════════════════

def upload_image(file_path: str, *,
                 token: str = "",
                 base_url: str = "https://www.beeimg.cn",
                 strategy_id: str = "",
                 permission: int = 1,
                 timeout: int = 120) -> dict:
    """上传图片到 beeimg 图床

    参数:
        file_path: 本地 PNG 文件路径
        token: Bearer Token
        base_url: 图床 API 地址
        strategy_id: 储存策略 ID（必填，如不传则自动获取第一个可用策略）
        permission: 1=公开, 0=私有
        timeout: 超时秒数

    返回:
        成功 → {"success": true, "url": "https://...", "markdown": "![...](...)"}
        失败 → {"success": false, "error": "..."}
    """
    # 参数校验
    if not token:
        return {"success": False, "error": "BEEIMG_TOKEN 未配置。请在 .env 或 .grindraft/config.env 中设置 BEEIMG_TOKEN=你的Token"}

    # 自动获取储存策略（如果未指定）
    if not strategy_id:
        try:
            headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
            with httpx.Client(timeout=15) as client:
                resp = client.get(f"{base_url.rstrip('/')}/api/v1/strategies", headers=headers)
            if resp.status_code == 200:
                strategies = resp.json().get("data", {}).get("strategies", [])
                if strategies:
                    strategy_id = str(strategies[0]["id"])
        except Exception:
            pass
        if not strategy_id:
            return {"success": False, "error": "无法获取储存策略 ID，请手动指定 --strategy-id"}

    p = Path(file_path)
    if not p.exists():
        return {"success": False, "error": f"文件不存在: {file_path}"}
    if not p.is_file():
        return {"success": False, "error": f"路径不是文件: {file_path}"}

    url = f"{base_url.rstrip('/')}/api/v1/upload"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    try:
        with open(file_path, "rb") as f:
            files = {"file": (p.name, f, "image/png")}
            data = {"permission": str(permission), "strategy_id": strategy_id}

            with httpx.Client(timeout=timeout) as client:
                resp = client.post(url, headers=headers, files=files, data=data)
    except httpx.TimeoutException:
        return {"success": False, "error": f"上传超时（>{timeout}s）"}
    except httpx.ConnectError:
        return {"success": False, "error": f"无法连接图床服务: {base_url}"}
    except httpx.HTTPError as e:
        return {"success": False, "error": f"网络异常: {e}"}

    if resp.status_code != 200:
        return {"success": False, "error": f"图床返回 {resp.status_code}: {resp.text[:500]}"}

    try:
        data = resp.json()
    except (json.JSONDecodeError, ValueError):
        return {"success": False, "error": f"图床返回非 JSON: {resp.text[:300]}"}

    if not data.get("status"):
        msg = data.get("message", "未知错误")
        return {"success": False, "error": f"上传失败: {msg}"}

    links = data.get("data", {}).get("links", {})
    image_url = links.get("url", "")
    markdown = links.get("markdown", "")

    if not image_url:
        return {"success": False, "error": "图床返回成功但未包含图片 URL", "raw": data}

    return {
        "success": True,
        "url": image_url,
        "markdown": markdown,
        "key": data["data"].get("key"),
        "name": data["data"].get("name", p.name),
        "size": data["data"].get("size", 0),
    }


# ═══════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="beeimg 图床上传脚本")
    parser.add_argument("--file", "-f", required=True, help="本地图片路径")
    parser.add_argument("--permission", "-p", type=int, default=1,
                        choices=[0, 1], help="0=私有, 1=公开（默认）")
    parser.add_argument("--token", "-t", default="",
                        help="Bearer Token（默认从 BEEIMG_TOKEN 环境变量读取）")
    parser.add_argument("--base-url", "-b", default="",
                        help="图床地址（默认从 BEEIMG_BASE_URL 读取，兜底 https://www.beeimg.cn）")
    parser.add_argument("--timeout", type=int, default=120,
                        help="超时秒数（默认 120）")
    parser.add_argument("--strategy-id", "-s", default="",
                        help="储存策略 ID（默认自动获取第一个可用策略）")
    args = parser.parse_args()

    config = load_config()
    token = args.token or config["token"]
    base_url = args.base_url or config["base_url"]

    print(f"[·] 上传中: {args.file} → {base_url}", file=sys.stderr)

    result = upload_image(
        file_path=args.file,
        token=token,
        base_url=base_url,
        strategy_id=args.strategy_id,
        permission=args.permission,
        timeout=args.timeout,
    )

    if result["success"]:
        print(f"[OK] {result['url']}", file=sys.stderr)
    else:
        print(f"[FAIL] {result['error']}", file=sys.stderr)

    print(json.dumps(result, ensure_ascii=False))
    if not result["success"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
