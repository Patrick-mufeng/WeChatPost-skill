#!/usr/bin/env python3
"""beeimg 图床删除脚本（Lsky Pro API）
删除已上传到 beeimg 图床的图片。

用法:
    # 单张删除
    python delete_from_beeimg.py --key 83890

    # 批量删除（从 JSON 文件读取）
    python delete_from_beeimg.py --keys-file "illustrations/uploaded-keys.json"

    # 指定 Token 和地址
    python delete_from_beeimg.py --key 83890 --token "Bearer xxx" --base-url "https://www.beeimg.cn"

依赖: httpx
API: Lsky Pro — DELETE /api/v1/images/{key}
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
# 配置加载
# ═══════════════════════════════════════════════════════════════════════════

def load_config() -> dict:
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
# 删除函数
# ═══════════════════════════════════════════════════════════════════════════

def delete_image(key: int, *, token: str, base_url: str, timeout: int = 30) -> dict:
    """删除单张图片"""
    url = f"{base_url.rstrip('/')}/api/v1/images/{key}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    try:
        with httpx.Client(timeout=timeout) as client:
            resp = client.delete(url, headers=headers)
    except httpx.TimeoutException:
        return {"success": False, "key": key, "error": "超时"}
    except httpx.ConnectError:
        return {"success": False, "key": key, "error": "无法连接图床"}
    except httpx.HTTPError as e:
        return {"success": False, "key": key, "error": str(e)}

    if resp.status_code == 204 or resp.status_code == 200:
        return {"success": True, "key": key}
    else:
        return {"success": False, "key": key, "error": f"HTTP {resp.status_code}: {resp.text[:200]}"}


def delete_batch(keys: list[int], *, token: str, base_url: str, timeout: int = 30) -> dict:
    """批量删除图片

    参数:
        keys: 图片 key 列表（整数）
        token, base_url, timeout: 同 delete_image

    返回:
        {"success": true, "deleted": 3, "failed": 0, "results": [...]}
    """
    results = []
    for key in keys:
        r = delete_image(key, token=token, base_url=base_url, timeout=timeout)
        results.append(r)

    deleted = sum(1 for r in results if r["success"])
    failed = len(results) - deleted
    return {
        "success": failed == 0,
        "deleted": deleted,
        "failed": failed,
        "results": results,
    }


# ═══════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="beeimg 图床删除脚本")
    parser.add_argument("--key", "-k", type=int, default=0,
                        help="单张图片的 key（整数）")
    parser.add_argument("--keys-file", "-f", default="",
                        help="JSON 文件路径，格式 {\"文件名\": key, ...}")
    parser.add_argument("--token", "-t", default="",
                        help="Bearer Token（默认从 BEEIMG_TOKEN 环境变量读取）")
    parser.add_argument("--base-url", "-b", default="",
                        help="图床地址（默认从 BEEIMG_BASE_URL 读取）")
    parser.add_argument("--timeout", type=int, default=30,
                        help="超时秒数（默认 30）")
    args = parser.parse_args()

    config = load_config()
    token = args.token or config["token"]
    base_url = args.base_url or config["base_url"]

    if not token:
        print(json.dumps({"success": False, "error": "BEEIMG_TOKEN 未配置"}))
        sys.exit(1)

    if args.keys_file:
        # 批量模式
        keys_path = Path(args.keys_file)
        if not keys_path.exists():
            print(json.dumps({"success": False, "error": f"文件不存在: {args.keys_file}"}))
            sys.exit(1)

        try:
            with open(keys_path, "r", encoding="utf-8") as f:
                keys_map = json.load(f)
        except (json.JSONDecodeError, ValueError) as e:
            print(json.dumps({"success": False, "error": f"keys 文件格式错误: {e}"}))
            sys.exit(1)

        keys = list(keys_map.values())
        print(f"[·] 批量删除 {len(keys)} 张图片...", file=sys.stderr)

    elif args.key:
        # 单张模式
        keys = [args.key]
        print(f"[·] 删除图片 key={args.key}", file=sys.stderr)

    else:
        print(json.dumps({"success": False, "error": "请指定 --key 或 --keys-file"}))
        sys.exit(1)

    result = delete_batch(keys, token=token, base_url=base_url, timeout=args.timeout)

    if result["success"]:
        print(f"[OK] 全部删除成功 ({result['deleted']} 张)", file=sys.stderr)
        # 删除成功后清理 keys 文件
        if args.keys_file:
            try:
                os.remove(args.keys_file)
                print(f"[·] 已清理 {args.keys_file}", file=sys.stderr)
            except OSError:
                pass
    else:
        print(f"[WARN] {result['failed']}/{len(keys)} 删除失败", file=sys.stderr)
        for r in result["results"]:
            if not r["success"]:
                print(f"  key={r['key']}: {r['error']}", file=sys.stderr)

    print(json.dumps(result, ensure_ascii=False))
    if not result["success"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
