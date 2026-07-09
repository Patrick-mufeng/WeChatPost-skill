# WeChatPost 一键安装脚本 (Windows PowerShell)
# 用法: powershell -ExecutionPolicy Bypass -File scripts/install.ps1

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  WeChatPost 环境安装" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# ── 1. 检查 Python ──
Write-Host "[1/5] 检查 Python..." -ForegroundColor Yellow
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) { $pythonCmd = "python" }
elseif (Get-Command python3 -ErrorAction SilentlyContinue) { $pythonCmd = "python3" }

if (-not $pythonCmd) {
    Write-Host "  ❌ Python 未安装。请先安装 Python 3.10+: https://python.org" -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ $(& $pythonCmd --version)" -ForegroundColor Green

# ── 2. 安装 Python 包 ──
Write-Host "[2/5] 安装 Python 依赖..." -ForegroundColor Yellow
& $pythonCmd -m pip install -r "$ScriptDir\..\requirements.txt" -q
Write-Host "  ✅ Python 依赖安装完成" -ForegroundColor Green

# ── 3. 检查/安装 ffmpeg ──
Write-Host "[3/5] 检查 ffmpeg..." -ForegroundColor Yellow
if (Get-Command ffmpeg -ErrorAction SilentlyContinue) {
    Write-Host "  ✅ $(& ffmpeg -version 2>&1 | Select-Object -First 1)" -ForegroundColor Green
} else {
    Write-Host "  ⚠️ ffmpeg 未安装。尝试通过 winget 安装..." -ForegroundColor Yellow
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install --id Gyan.FFmpeg --accept-source-agreements --accept-package-agreements
        Write-Host "  ✅ ffmpeg 安装完成（请重启终端）" -ForegroundColor Green
    } else {
        Write-Host "  ❌ winget 不可用。请手动安装 ffmpeg:" -ForegroundColor Red
        Write-Host "     下载: https://www.gyan.dev/ffmpeg/builds/" -ForegroundColor Yellow
        Write-Host "     解压后将 bin 目录加入 PATH 环境变量" -ForegroundColor Yellow
    }
}

# ── 4. 检查/安装 lark-cli ──
Write-Host "[4/5] 检查 lark-cli..." -ForegroundColor Yellow
if (Get-Command lark-cli -ErrorAction SilentlyContinue) {
    Write-Host "  ✅ lark-cli $(& lark-cli --version)" -ForegroundColor Green
} else {
    Write-Host "  ⚠️ lark-cli 未安装。安装中..." -ForegroundColor Yellow
    if (Get-Command npm -ErrorAction SilentlyContinue) {
        npm install -g @larksuite/cli
        Write-Host "  ✅ lark-cli 安装完成" -ForegroundColor Green
    } else {
        Write-Host "  ❌ 请先安装 Node.js: https://nodejs.org" -ForegroundColor Red
        Write-Host "     然后运行: npm install -g @larksuite/cli" -ForegroundColor Yellow
    }
}

# ── 5. 验证安装 ──
Write-Host "[5/5] 验证安装..." -ForegroundColor Yellow
$errors = 0

& $pythonCmd -c "import yt_dlp; print('  ✅ yt-dlp')" 2>$null
if ($LASTEXITCODE -ne 0) { Write-Host "  ❌ yt-dlp" -ForegroundColor Red; $errors++ }

& $pythonCmd -c "import whisper; print('  ✅ whisper')" 2>$null
if ($LASTEXITCODE -ne 0) { Write-Host "  ❌ whisper" -ForegroundColor Red; $errors++ }

& $pythonCmd -c "import httpx; print('  ✅ httpx')" 2>$null
if ($LASTEXITCODE -ne 0) { Write-Host "  ❌ httpx" -ForegroundColor Red; $errors++ }

ffmpeg -version 2>$null
if ($LASTEXITCODE -eq 0) { Write-Host "  ✅ ffmpeg" -ForegroundColor Green } else { Write-Host "  ❌ ffmpeg" -ForegroundColor Red; $errors++ }

Write-Host ""
if ($errors -eq 0) {
    Write-Host "🎉 全部安装完成！说'初始化'继续配置。" -ForegroundColor Green
} else {
    Write-Host "⚠️ $errors 项安装失败，请手动检查。" -ForegroundColor Yellow
}
