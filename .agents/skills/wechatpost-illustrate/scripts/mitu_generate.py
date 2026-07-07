#!/usr/bin/env python3
"""觅图 (Mitu) — 命令行 AI 图片生成工具
基于云雾 API，支持文生图、图生图、多图参考生成。

使用方法:
    python mitu_generate.py "一只可爱的橘猫坐在窗台上"
    python mitu_generate.py "未来城市" -m dall-e-3 -r 16:9 --mp 2 -n 2
    python mitu_generate.py "把猫变成金色" -e input.jpg
    python mitu_generate.py "改背景" -e input.jpg --mask mask.png
    python mitu_generate.py "融合风格" --ref img1.jpg img2.jpg
    python mitu_generate.py "猫" -m black-forest-labs/flux-schnell
    python mitu_generate.py "猫" -o ./my_images --key sk-xxx

依赖: httpx
"""

import os
import sys
import time
import uuid
import argparse
import asyncio
import base64
from pathlib import Path

import httpx

# 从同目录导入 mitu_client 模块
from mitu_client import (
    MituClient, MituAPIError,
    is_replicate_model, resolve_size,
    download_image, save_base64_image, get_config,
)


# ═══════════════════════════════════════════════════════════════════════════
# 图片处理辅助
# ═══════════════════════════════════════════════════════════════════════════

def _read_image_file(path: str) -> tuple[bytes, str]:
    """读取图片文件，返回 (data, filename)"""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"图片文件不存在: {path}")
    if not p.is_file():
        raise ValueError(f"路径不是文件: {path}")
    data = p.read_bytes()
    if len(data) == 0:
        raise ValueError(f"图片文件为空: {path}")
    return data, p.name


def _generate_prefix(prompt: str) -> str:
    """从 prompt 生成短前缀，用于文件名"""
    clean = prompt.strip()[:30].replace(" ", "_").replace("/", "_").replace("\\", "_")
    clean = "".join(c for c in clean if c.isalnum() or c in "_-")
    return clean or "image"


# ═══════════════════════════════════════════════════════════════════════════
# 核心生图逻辑
# ═══════════════════════════════════════════════════════════════════════════

async def generate_text_to_image(client: MituClient, args):
    """文生图"""
    size = resolve_size(args.ratio, args.mp)
    prefix = _generate_prefix(args.prompt)
    task_id = uuid.uuid4().hex[:12]

    if is_replicate_model(args.model):
        # ── Replicate 格式 ──
        print(f"\n{'='*60}")
        print(f"🚀 文生图 (Replicate 异步模式)")
        print(f"{'='*60}")
        print(f"  模型:     {args.model}")
        print(f"  比例:     {args.ratio}")
        print(f"  分辨率:   {args.mp}MP")
        print(f"  数量:     {args.num}")
        print(f"  输出目录: {args.output}")
        print(f"  Prompt:   {args.prompt[:100]}{'...' if len(args.prompt) > 100 else ''}")
        print(f"{'='*60}\n")

        t0 = time.time()
        print("📤 创建 Replicate 预测任务...")
        prediction = await client.create_prediction(
            prompt=args.prompt, aspect_ratio=args.ratio,
            megapixels=args.mp, num_outputs=args.num,
            output_format=args.format, output_quality=args.quality,
            num_inference_steps=args.steps, model=args.model,
        )

        rid = prediction.get("id", task_id)
        print(f"✅ 任务创建成功: {rid}")
        print(f"   初始状态: {prediction.get('status', 'unknown')}")

        if prediction.get("status") in ("succeeded", "failed", "canceled"):
            result = prediction
        else:
            print(f"\n⏳ 等待生成中...")

            last_log_len = 0

            def on_progress(info):
                nonlocal last_log_len
                status = info["status"]
                logs = info["logs"]
                elapsed = info["elapsed"]
                # 打印新增日志
                if logs and len(logs) > last_log_len:
                    new_part = logs[last_log_len:]
                    for line in new_part.split("\n"):
                        line = line.strip()
                        if line:
                            print(f"  [API] {line}")
                    last_log_len = len(logs)
                # 进度提示
                if status == "processing":
                    print(f"\r⏳ 生成中... {elapsed:.0f}s", end="", flush=True)

            result = await client.wait_for_completion(rid, on_progress=on_progress)

        elapsed = time.time() - t0

        if result.get("status") == "succeeded":
            print(f"\n\n✅ 生成成功! 耗时: {elapsed:.1f}s\n")

            output_urls = result.get("output", [])
            if isinstance(output_urls, str):
                output_urls = [output_urls]

            saved = []
            for idx, url in enumerate(output_urls):
                print(f"📥 下载图片 {idx+1}/{len(output_urls)}...")
                local_path = await download_image(url, args.output, prefix, idx)
                if local_path:
                    saved.append(local_path)
                    print(f"   ✅ {local_path}")
                else:
                    print(f"   ❌ 下载失败")

            if saved:
                print(f"\n🎉 共保存 {len(saved)} 张图片到 {os.path.abspath(args.output)}/")
            else:
                print(f"\n❌ 未成功下载任何图片")
                if output_urls:
                    print(f"   远程 URL: {output_urls}")
        else:
            err = result.get("error", "未知错误")
            print(f"\n❌ 生成失败: {err}")

    else:
        # ── OpenAI 格式 ──
        print(f"\n{'='*60}")
        print(f"🎨 文生图 (OpenAI 即时模式)")
        print(f"{'='*60}")
        print(f"  模型:     {args.model}")
        print(f"  尺寸:     {size}")
        print(f"  数量:     {args.num}")
        print(f"  输出目录: {args.output}")
        print(f"  Prompt:   {args.prompt[:100]}{'...' if len(args.prompt) > 100 else ''}")
        print(f"{'='*60}\n")

        t0 = time.time()
        print("📤 发送请求到 API...")
        result = await client.openai_generate(
            prompt=args.prompt, model=args.model,
            size=size, n=args.num,
        )

        api_time = time.time() - t0
        print(f"✅ API 响应成功 (耗时 {api_time:.1f}s)\n")

        data_items = result.get("data", [])
        if isinstance(data_items, dict):
            data_items = [data_items]

        if not data_items:
            print("⚠ API 返回空结果")
            print(f"   完整响应: {result}")
            return

        saved = []
        for idx, item in enumerate(data_items):
            print(f"📥 处理图片 {idx+1}/{len(data_items)}...")

            # 自定义文件名（仅 n=1 时生效）
            if args.output_name and args.num == 1:
                output_name = args.output_name
            else:
                if args.output_name and args.num > 1:
                    print(f"   ⚠ --output-name 仅在 -n 1 时生效，当前 -n {args.num}，将使用自动命名")
                output_name = None

            if item.get("url"):
                if output_name:
                    local_path = os.path.join(args.output, output_name)
                    os.makedirs(args.output, exist_ok=True)
                    async with httpx.AsyncClient(timeout=120.0) as dl:
                        dl_resp = await dl.get(item["url"])
                        dl_resp.raise_for_status()
                        with open(local_path, "wb") as f:
                            f.write(dl_resp.content)
                else:
                    local_path = await download_image(item["url"], args.output, prefix, idx)
            elif item.get("b64_json"):
                if output_name:
                    os.makedirs(args.output, exist_ok=True)
                    tmp_path = save_base64_image(item["b64_json"], args.output, "tmp_generated", 0)
                    if not tmp_path:
                        print(f"   ⚠ base64 解码失败，跳过")
                        continue
                    new_path = os.path.join(args.output, output_name)
                    if tmp_path != new_path:
                        if os.path.exists(new_path):
                            os.remove(new_path)
                        os.replace(tmp_path, new_path)
                    local_path = new_path
                else:
                    local_path = save_base64_image(item["b64_json"], args.output, prefix, idx)
            else:
                print(f"   ⚠ 无可用图片数据")
                continue

            if local_path:
                saved.append(local_path)
                print(f"   ✅ {local_path}")
                if item.get("revised_prompt"):
                    print(f"   📝 修订提示词: {item['revised_prompt'][:100]}...")
            else:
                print(f"   ❌ 保存失败")

        total_elapsed = time.time() - t0
        if saved:
            print(f"\n🎉 共保存 {len(saved)} 张图片到 {os.path.abspath(args.output)}/")
            print(f"   总耗时: {total_elapsed:.1f}s (API: {api_time:.1f}s)")
        else:
            print(f"\n❌ 未成功保存任何图片")
            print(f"   API 返回数据: {data_items}")


async def generate_image_to_image(client: MituClient, args):
    """图生图"""
    image_data, filename = _read_image_file(args.edit)
    mask_data = None
    mask_filename = "mask.png"

    if args.mask:
        mask_data, mask_filename = _read_image_file(args.mask)

    size = resolve_size(args.ratio, args.mp)
    prefix = _generate_prefix(args.prompt)

    print(f"\n{'='*60}")
    print(f"🖼️ 图生图编辑")
    print(f"{'='*60}")
    print(f"  模型:     {args.model}")
    print(f"  图片:     {args.edit} ({len(image_data)} bytes)")
    if mask_data:
        print(f"  蒙版:     {args.mask} ({len(mask_data)} bytes)")
    print(f"  尺寸:     {size}")
    print(f"  数量:     {args.num}")
    print(f"  输出目录: {args.output}")
    print(f"  Prompt:   {args.prompt[:100]}{'...' if len(args.prompt) > 100 else ''}")
    print(f"{'='*60}\n")

    t0 = time.time()
    print("📤 上传图片并发送请求...")

    result = await client.edit_image(
        image_data=image_data, prompt=args.prompt,
        filename=filename, model=args.model,
        mask_data=mask_data, mask_filename=mask_filename,
        n=args.num, size=size,
    )

    api_time = time.time() - t0
    print(f"✅ API 响应成功 (耗时 {api_time:.1f}s)\n")

    data_items = result.get("data", {})
    if isinstance(data_items, dict):
        data_items = [data_items]

    saved = []
    for idx, item in enumerate(data_items):
        if isinstance(item, dict):
            print(f"💾 保存图片 {idx+1}...")
            if item.get("b64_json"):
                local_path = save_base64_image(item["b64_json"], args.output, prefix, idx)
            elif item.get("url"):
                local_path = await download_image(item["url"], args.output, prefix, idx)
            else:
                print(f"   ⚠ 无可用图片数据")
                continue

            if local_path:
                saved.append(local_path)
                print(f"   ✅ {local_path}")
            else:
                print(f"   ❌ 保存失败")

    total_elapsed = time.time() - t0
    if saved:
        print(f"\n🎉 共保存 {len(saved)} 张图片到 {os.path.abspath(args.output)}/")
        print(f"   总耗时: {total_elapsed:.1f}s (API: {api_time:.1f}s)")
    else:
        print(f"\n❌ 未成功保存任何图片")
        print(f"   API 返回数据: {result}")


async def generate_reference(client: MituClient, args):
    """多图参考生成"""
    image_urls = []
    for path in args.ref:
        data, filename = _read_image_file(path)
        ext = Path(path).suffix.lower()
        mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                     ".webp": "image/webp", ".gif": "image/gif"}
        mime = mime_map.get(ext, "image/png")
        data_url = f"data:{mime};base64,{base64.b64encode(data).decode('utf-8')}"
        image_urls.append(data_url)

    size = resolve_size(args.ratio, args.mp)
    prefix = _generate_prefix(args.prompt)

    print(f"\n{'='*60}")
    print(f"🔗 多图参考生成")
    print(f"{'='*60}")
    print(f"  模型:     {args.model}")
    print(f"  参考图:   {len(args.ref)} 张")
    for p in args.ref:
        print(f"    - {p}")
    print(f"  尺寸:     {size}")
    print(f"  数量:     {args.num}")
    print(f"  输出目录: {args.output}")
    print(f"  Prompt:   {args.prompt[:100]}{'...' if len(args.prompt) > 100 else ''}")
    print(f"{'='*60}\n")

    t0 = time.time()
    print("📤 发送多图参考请求...")

    result = await client.reference_generate(
        prompt=args.prompt, image_urls=image_urls,
        model=args.model, size=size, n=args.num,
    )

    api_time = time.time() - t0
    print(f"✅ API 响应成功 (耗时 {api_time:.1f}s)\n")

    data_items = result.get("data", [])
    if isinstance(data_items, dict):
        data_items = [data_items]

    saved = []
    for idx, item in enumerate(data_items):
        print(f"📥 处理图片 {idx+1}/{len(data_items)}...")
        if item.get("url"):
            local_path = await download_image(item["url"], args.output, prefix, idx)
        elif item.get("b64_json"):
            local_path = save_base64_image(item["b64_json"], args.output, prefix, idx)
        else:
            print(f"   ⚠ 无可用图片数据")
            continue

        if local_path:
            saved.append(local_path)
            print(f"   ✅ {local_path}")
        else:
            print(f"   ❌ 保存失败")

    total_elapsed = time.time() - t0
    if saved:
        print(f"\n🎉 共保存 {len(saved)} 张图片到 {os.path.abspath(args.output)}/")
        print(f"   总耗时: {total_elapsed:.1f}s (API: {api_time:.1f}s)")
    else:
        print(f"\n❌ 未成功保存任何图片")
        print(f"   API 返回数据: {result}")


# ═══════════════════════════════════════════════════════════════════════════
# 命令行参数解析
# ═══════════════════════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="觅图 (Mitu) — 命令行 AI 图片生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python mitu_generate.py "一只可爱的橘猫坐在窗台上"
  python mitu_generate.py "未来城市" -m dall-e-3 -r 16:9 --mp 2 -n 2
  python mitu_generate.py "把猫变成金色" -e input.jpg
  python mitu_generate.py "改背景" -e input.jpg --mask mask.png
  python mitu_generate.py "融合风格" --ref img1.jpg img2.jpg
  python mitu_generate.py "猫" -m black-forest-labs/flux-schnell
  python mitu_generate.py "猫" -o ./my_images --key sk-xxx
        """,
    )

    # ── 位置参数 ──
    parser.add_argument(
        "prompt", nargs="?", default="",
        help="图片描述提示词 (图生图模式下可省略或作为编辑描述)",
    )

    # ── 生成模式 ──
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "-e", "--edit", metavar="IMAGE",
        help="图生图模式: 上传图片进行 AI 编辑",
    )
    mode_group.add_argument(
        "--ref", nargs="+", metavar="IMAGE",
        help="多图参考模式: 上传多张参考图进行生成 (gpt-image-2-all)",
    )

    # ── 图生图选项 ──
    parser.add_argument(
        "--mask", metavar="MASK",
        help="蒙版图片 (仅图生图模式，PNG格式)",
    )

    # ── 模型参数 ──
    parser.add_argument(
        "-m", "--model", default="gpt-image-2",
        help="模型名称 (默认: gpt-image-2). 也支持 dall-e-3, gpt-image-1, "
             "gpt-image-2-all, black-forest-labs/flux-schnell 等",
    )
    parser.add_argument(
        "-r", "--ratio", default="1:1",
        choices=["1:1", "16:9", "9:16", "4:3", "3:4"],
        help="画面比例 (默认: 1:1)",
    )
    parser.add_argument(
        "--mp", type=int, default=1, choices=[1, 2, 4],
        help="分辨率: 1=1MP标准, 2=2MP高清, 4=4MP超清 (默认: 1)",
    )
    parser.add_argument(
        "-n", "--num", type=int, default=1,
        help="生成数量 (默认: 1, 最大: 4)",
    )

    # ── Replicate 专属参数 ──
    replicate_group = parser.add_argument_group("Replicate 格式参数 (FLUX 等异步模型)")
    replicate_group.add_argument(
        "--format", default="jpg", choices=["jpg", "png", "webp"],
        help="输出格式 (默认: jpg)",
    )
    replicate_group.add_argument(
        "--quality", type=int, default=80,
        help="画质 1-100 (默认: 80)",
    )
    replicate_group.add_argument(
        "--steps", type=int, default=4,
        help="推理步数 (默认: 4)",
    )

    # ── 输出选项 ──
    parser.add_argument(
        "-o", "--output", default="./output",
        help="图片输出目录 (默认: ./output)",
    )
    parser.add_argument(
        "--output-name", default="",
        help="自定义输出文件名 (如 \"01-封面.png\")，仅 n=1 时生效；不指定则从 prompt 自动生成",
    )

    # ── API 配置 ──
    parser.add_argument(
        "--key", default="",
        help="云雾 API Key (不指定则从 .env 文件或环境变量 YUNWU_API_KEY 读取)",
    )
    parser.add_argument(
        "--base-url", default="",
        help="API 基础地址 (默认: https://yunwu.ai)",
    )

    return parser


# ═══════════════════════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════════════════════

async def main_async(args: argparse.Namespace):
    config = get_config()
    api_key = args.key or config["api_key"]
    base_url = args.base_url or config["base_url"]

    if not api_key or api_key in ("sk-your-api-key-here", "sk-YOUR_API_KEY"):
        print("\n❌ 错误: 请先配置 API Key!")
        print("  方法1: 在项目根目录 .grindraft/config.env 中填入 YUNWU_API_KEY=sk-xxx（推荐）")
        print("  方法2: 在项目根目录 .env 或脚本目录 .env 中填入 YUNWU_API_KEY=sk-xxx")
        print("  方法3: 设置环境变量 YUNWU_API_KEY")
        print("  方法4: 使用 --key 参数: python mitu_generate.py --key sk-xxx \"prompt\"")
        sys.exit(1)

    client = MituClient(api_key=api_key, base_url=base_url)

    if args.ref:
        if not args.prompt:
            args.prompt = input("请输入提示词: ").strip()
            if not args.prompt:
                print("❌ 提示词不能为空")
                sys.exit(1)
        await generate_reference(client, args)

    elif args.edit:
        if not args.prompt:
            args.prompt = input("请输入编辑提示词: ").strip()
            if not args.prompt:
                print("❌ 提示词不能为空")
                sys.exit(1)
        await generate_image_to_image(client, args)

    else:
        if not args.prompt:
            args.prompt = input("请输入图片描述: ").strip()
            if not args.prompt:
                print("❌ 提示词不能为空")
                sys.exit(1)
        await generate_text_to_image(client, args)


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        asyncio.run(main_async(args))
    except KeyboardInterrupt:
        print("\n\n⚠ 用户中断")
        sys.exit(130)
    except MituAPIError as e:
        print(f"\n❌ API 错误: {e}")
        if hasattr(e, "to_dict"):
            detail = e.to_dict()
            if detail.get("response", {}).get("body"):
                print(f"   响应: {detail['response']['body'][:500]}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\n❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 未知错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
