#!/bin/bash
# WeChatPost 一键安装脚本 (macOS/Linux)
# 用法: bash scripts/install.sh

set -e

echo "============================================"
echo "  WeChatPost 环境安装"
echo "============================================"
echo ""

# ── 1. 检查 Python ──
echo "[1/5] 检查 Python..."
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "❌ Python 未安装。请先安装 Python 3.10+: https://python.org"
    exit 1
fi
echo "  ✅ $($PYTHON --version)"

# ── 2. 安装 Python 包 ──
echo "[2/5] 安装 Python 依赖..."
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
$PYTHON -m pip install -r "$SCRIPT_DIR/requirements.txt" -q
echo "  ✅ Python 依赖安装完成"

# ── 3. 检查/安装 ffmpeg ──
echo "[3/5] 检查 ffmpeg..."
if command -v ffmpeg &>/dev/null; then
    echo "  ✅ $(ffmpeg -version 2>&1 | head -1)"
else
    echo "  ⚠️ ffmpeg 未安装。尝试安装..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &>/dev/null; then
            brew install ffmpeg
            echo "  ✅ ffmpeg 安装完成"
        else
            echo "  ❌ 请先安装 Homebrew: https://brew.sh"
            echo "     然后运行: brew install ffmpeg"
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &>/dev/null; then
            sudo apt-get update && sudo apt-get install -y ffmpeg
        elif command -v yum &>/dev/null; then
            sudo yum install -y ffmpeg
        elif command -v dnf &>/dev/null; then
            sudo dnf install -y ffmpeg
        else
            echo "  ❌ 请手动安装 ffmpeg: https://ffmpeg.org/download.html"
        fi
        echo "  ✅ ffmpeg 安装完成"
    fi
fi

# ── 4. 检查/安装 lark-cli ──
echo "[4/5] 检查 lark-cli..."
if command -v lark-cli &>/dev/null; then
    echo "  ✅ lark-cli $(lark-cli --version)"
else
    echo "  ⚠️ lark-cli 未安装。安装中..."
    if command -v npm &>/dev/null; then
        npm install -g @larksuite/cli
        echo "  ✅ lark-cli 安装完成"
    else
        echo "  ❌ 请先安装 Node.js: https://nodejs.org"
        echo "     然后运行: npm install -g @larksuite/cli"
    fi
fi

# ── 5. 验证安装 ──
echo "[5/5] 验证安装..."
ERRORS=0

$PYTHON -c "import yt_dlp; print('  ✅ yt-dlp')" 2>/dev/null || { echo "  ❌ yt-dlp"; ERRORS=$((ERRORS+1)); }
$PYTHON -c "import whisper; print('  ✅ whisper')" 2>/dev/null || { echo "  ❌ whisper"; ERRORS=$((ERRORS+1)); }
$PYTHON -c "import httpx; print('  ✅ httpx')" 2>/dev/null || { echo "  ❌ httpx"; ERRORS=$((ERRORS+1)); }
ffmpeg -version &>/dev/null && echo "  ✅ ffmpeg" || { echo "  ❌ ffmpeg"; ERRORS=$((ERRORS+1)); }

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "🎉 全部安装完成！说"初始化"继续配置。"
else
    echo "⚠️ $ERRORS 项安装失败，请手动检查。"
fi
