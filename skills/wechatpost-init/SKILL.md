---
name: wechatpost-init
description: "Initialize WeChatPost project. Use when the user says 初始化, init, 首次使用, 开始使用, or 配置. Checks environment, guides API configuration, selects ASR engine, validates Feishu base, and creates project scaffolding (style_guide.md + WORKFLOW.md). Must run before any other WeChatPost skill."
---

# wechatpost-init — 项目初始化

> 首次使用必跑。6 阶段：环境检查 → API 配置 → ASR 引擎 → 飞书验证 → 风格设定 → 完成。

---

## Workflow

```
用户: "初始化"
  ↓
Phase 1: 环境检查（Python/ffmpeg/whisper/yt-dlp/lark-cli + Node.js/puppeteer/canvas）
  ↓
Phase 2: API 配置（云雾+配图开关）
  ↓
Phase 3: 🆕 公众号推送配置（可选）
  ↓
Phase 4: ASR 引擎选择（Whisper/火山）
  ↓
Phase 5: 飞书表格验证
  ↓
Phase 6: 风格设定 + 创建项目文件（outputs/ + style_guide.md + WORKFLOW.md）
  ↓
Phase 7: 完成提示
```

---

## Phase 1 · 环境检查

### 方式一：一键安装（推荐）

```bash
# Windows PowerShell
powershell -ExecutionPolicy Bypass -File scripts/install.ps1

# macOS / Linux
bash scripts/install.sh
```

> 脚本路径相对于 `wechatpost-skill` 目录（`../wechatpost-skill/scripts/install.sh`）。

### 方式二：逐项检查

```bash
# Python 依赖（转录管线）
python --version         2>&1
ffmpeg -version          2>&1
# 验证：输出版本信息即通过（如 "ffmpeg version 6.x"）
python -c "import whisper; print('whisper OK')" 2>&1
yt-dlp --version         2>&1
python -c "import httpx; print('httpx OK')" 2>&1
lark-cli auth status     2>&1

# Node.js 依赖（封面截图）
node --version           2>&1
npm --version            2>&1
node -e "require('puppeteer'); console.log('puppeteer OK')" 2>&1

# 微信公众号 API（可选，推送功能）
grep -E "^WECHAT_APPID=|^WECHAT_APPSECRET=" .env 2>/dev/null || echo "WECHAT_NOT_CONFIGURED"
```

### 输出 + 修复

```
🔍 环境检查
  □ Python 3.14 ✅
  □ ffmpeg ❌ → 已自动安装 ✅
  □ whisper ❌ → pip install openai-whisper
  □ yt-dlp ✅
  □ httpx ✅
  □ lark-cli ✅（Patrick）
  □ Node.js 20.x ✅
  □ puppeteer ❌ → npm install（见下方）
  □ 微信推送 ⚠️ 未配置 → 可选，见 Phase 3

全部通过 ✅
```

缺什么自动尝试安装，或给出具体命令：

| 缺失 | Windows | macOS | Linux |
|------|---------|-------|-------|
| Python | https://python.org 下载安装 | `brew install python` | `sudo apt install python3` |
| ffmpeg | `winget install Gyan.FFmpeg` | `brew install ffmpeg` | `sudo apt install ffmpeg` |
| Python 包 | `pip install -r requirements.txt` | 同上 | 同上 |
| lark-cli | `npm install -g @larksuite/cli` | 同上 | 同上 |
| Node.js | https://nodejs.org 下载 LTS | `brew install node` | `sudo apt install nodejs npm` |
| puppeteer | `cd cover-templates && npm install` | 同上 | 同上 |

> `requirements.txt` 和安装脚本在 `wechatpost-skill/` 下，包含所有 Python 依赖。
> `cover-templates/package.json` 管理 Node.js 依赖（puppeteer）。
> lark-cli 未授权 → `lark-cli auth login --recommend`。

---

## Phase 2 · API 配置

### 2.1 检查 .env

```bash
cat .env 2>/dev/null || echo "MISSING"
```

### 2.2 不存在 → 创建模板

```bash
cat > .env << 'EOF'
# ── 生图 API（云雾）── 用于正文配图 ──
# 注册：https://yunwu.ai/register?aff=zM1f
# 将下方 your-key-here 替换为你的真实 Key
YUNWU_API_KEY=sk-your-api-key-here
YUNWU_BASE_URL=https://yunwu.ai/

# ── 配图开关 ──
# true=启用配图（需填上面 Key） false=跳过配图阶段
ILLUSTRATE_ENABLED=true
EOF
```

### 2.3 引导用户

```
⚙️ 配图功能需要云雾 API：

① 云雾 API（gpt-image-2 生图）
   注册：https://yunwu.ai/register?aff=zM1f
   → 复制 API Key 填入 .env 的 YUNWU_API_KEY=

图片生成后保存为本地 PNG，推送阶段自动上传到微信 CDN，无需额外图床。

现在怎么做？
A) 我去注册，填好 Key 后说"配置完成"
B) 先跳过配图（ILLUSTRATE_ENABLED=false），后面可重新初始化
```

选 B → `.env` 已创建，`ILLUSTRATE_ENABLED=false`。后续配图阶段检测到此值自动跳过。

### 2.4 已有 .env → 验证

```
📋 API 配置
  □ YUNWU_API_KEY：已配置 ✅ / 未填写 ⚠️
  □ ILLUSTRATE_ENABLED：true / false
```

---

## Phase 3 · 公众号推送配置（可选）

### 询问用户

```
📤 是否需要「推送到公众号草稿箱」功能？

启用后，排版完成可直接通过微信 API 推送到公众号草稿箱，不用手动复制粘贴。

A) 需要 — 我去配置微信凭证
B) 不需要 — 继续手动粘贴发布

选 A / B？
```

### A. 引导配置

选 A → 引导用户获取凭证：

```
🔑 微信公众号 API 凭证

1. 登录公众号后台：https://mp.weixin.qq.com
2. 左侧菜单 → 设置与开发 → 基本配置
3. 复制「开发者ID(AppID)」和「开发者密码(AppSecret)」
   （AppSecret 需管理员扫码才能查看，请妥善保管）

4. 将凭证写入 .env：
   WECHAT_APPID=wx1234567890
   WECHAT_APPSECRET=你的appsecret
   WECHAT_AUTHOR=你的作者名

5. ⚠️ IP 白名单：在「基本配置」页面将本机出口 IP 加入白名单
   （可搜索"我的 IP"获取，或使用 curl ifconfig.me）

配置完成后说"配置完成"，我帮你验证。
```

### 验证凭证

用户说"配置完成"后，测试 token 获取：

```bash
python -c "
import urllib.request, json, os
from pathlib import Path
# 加载 .env
env_file = Path('.env')
if env_file.exists():
    for line in env_file.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, _, v = line.partition('=')
            os.environ[k.strip()] = v.strip()
appid = os.environ.get('WECHAT_APPID','')
secret = os.environ.get('WECHAT_APPSECRET','')
if not appid or not secret:
    print('MISSING')
else:
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}'
    try:
        resp = urllib.request.urlopen(url, timeout=15)
        data = json.loads(resp.read())
        if 'access_token' in data:
            print('OK')
        else:
            print(f'FAIL: errcode={data.get(\"errcode\")} {data.get(\"errmsg\",\"\")}')
    except Exception as e:
        print(f'NETWORK_ERROR: {e}')
"
```

| 结果 | 含义 |
|------|------|
| `OK` | 凭证有效 ✅ |
| `FAIL: errcode=40013` | AppID 错误 |
| `FAIL: errcode=40125` | AppSecret 错误 |
| `FAIL: errcode=40164` | IP 未加白名单 |
| `NETWORK_ERROR` | 网络问题或 IP 白名单未配置 |

### 设置公众号作者名

凭证验证通过后，询问作者名：

```
✏️ 公众号文章作者名是什么？

这个名称会出现在每篇文章的标题下方，通常是你公众号的运营者名字。

输入作者名（如"Patrick"，后续所有推送统一使用）：
```

用户输入后，追加到 `.env`：

```env
WECHAT_AUTHOR=Patrick
```

> 如果用户暂时不想设置，可以说"跳过"——推送时会 fallback 使用视频原作者名。之后可以手动在 `.env` 中添加 `WECHAT_AUTHOR=你的名字`。

### B. 跳过

选 B → 不配置，`.env` 中不写 WECHAT_APPID/WECHAT_APPSECRET。后续推送时自动跳过并提示手动操作。

---

## Phase 4 · ASR 引擎选择

```
🎙 语音识别引擎：

1. 本地 Whisper — 免费，tiny模型，约1GB内存，中文需LLM纠错（推荐）
2. 火山引擎 ASR — 云端，识别更精准，需配置 VOLC_ACCESS_KEY + VOLC_SECRET_KEY

选哪个？（默认 1）
```

选 2 → 引导创建火山引擎配置：

```env
# 火山引擎 ASR（语音转文字）
VOLC_ACCESS_KEY=your-access-key
VOLC_SECRET_KEY=your-secret-key
```

追加到 `.env`。

---

## Phase 5 · 飞书表格验证

```bash
lark-cli base +record-list \
  --base-token ROfJb313faU478s3oXDcKjbknUc \
  --table-id tblKkOBWDtAgarcT \
  --as user
```

输出：

```
📊 飞书表格连接 ✅
   名称：视频链接
   字段：12 个
   记录：N 条（待处理：X，已转录：Y，已完成：Z）
```

连接失败 → 检查 `lark-cli auth status`，提示重新授权。

---

## Phase 6 · 风格设定 + 创建项目文件

### 6.0 询问风格模式

```
✏️ 风格设定——让 AI 写得像你

A) 口头描述 — 简单说说你的风格偏好
B) 提供文章 — 5 篇以上你写过的文章，AI 分析后自动提取风格
C) 先跳过 — 用默认风格，后续每次改稿 AI 自动学习

选哪个？
```

### 6A · 口头描述

```
你怎么形容你的公众号？
A) 硬核科技，敢说真话，接地气
B) 温暖治愈，娓娓道来，生活感
C) 专业干货，条理清晰，教科书级
D) 其他（自己说）

格式偏好？
- 小标题：1. 数字序号 / · 符号引导 / 纯文字
- 加粗：核心观点 / 关键数字 / 不太用加粗
- 段落：短(1-3句) / 中(3-5句) / 长
- 结尾：总结收束 / 抛问题 / 留白 / 行动呼吁
```

用户一句话说完 → 填入 `style_guide.md`。

### 6B · 提供文章分析（≥5 篇）

#### 输入

```
📄 提供 5 篇以上你写过的公众号文章。

可以：
- 直接粘贴 Markdown/纯文本
- 给公众号链接（我帮你抓取正文）
- 指定本地文件路径

至少 5 篇。一篇一篇来，我会说"下一篇"。
```

#### 逐篇分析（对每一篇）

```
分析第 1/5 篇...

📊 风格指纹：

段落特征：
- 平均段落长度：X 句
- 最长/最短段：X/Y 句
- 独句成段频率：每 N 段 1 次

开头模式：故事切入 / 观点先行 / 场景描写 / 设问开篇

句式特征：
- 平均句长：X 字
- 问句频率：每 N 字 1 次
- 感叹号使用：克制 / 频繁 / 从不

词汇指纹：
- 高频口语词：[列出 3-6 个]
- AI 套话：无 / 有（"首先其次""综上所述"等）

加粗模式：
- 密度：每 N 字 1 处
- 加粗内容：观点(XX%) / 数字(XX%) / 其他(XX%)

结尾模式：总结收束 / 留白 / 反问 / 行动呼吁 / 回环呼应

结构信号：
- 小标题风格：数字序号 / 符号引导 / 纯文字
- 转场方式：口语过渡 / 标题硬切
```

#### 5 篇汇总

```
📊 5 篇风格汇总

| 维度 | 模式 | 覆盖 | 置信度 |
|------|------|------|--------|
| 开头 | 故事切入 | 5/5 | ⭐⭐⭐ |
| 段落 | 短段落 | 4/5 | ⭐⭐⭐ |
| 句式 | 中短句为主 | 5/5 | ⭐⭐⭐ |
| 结尾 | 留白(3) / 呼应收尾(2) | — | ⭐⭐ |
| 加粗 | 核心观点主导 | 4/5 | ⭐⭐ |
| 口语词 | "说实话""说白了"高频 | 3/5 | ⭐⭐ |

推导风格：**接地气的科技分享者**——善用故事切入，短段落快节奏，敢下判断，结尾留余味。
```

如果某维度 ≤2/5 一致 → 标"不固定"，提示 AI 写稿时询问。

#### 写入 style_guide.md

```markdown
# 风格指南

> 初始化时从 {N} 篇文章分析提取。后续每次改稿自动学习追加。

## 角色定位
{推导风格}

## 写作指纹

| 维度 | 模式 | 来源 |
|------|------|------|
| 开头 | {模式} | {N}/总数 篇 |
| 段落 | {模式} | {N}/总数 篇 |
| ...

## 绝对禁区
<!-- AI 从你的文章中自动识别 -->
{高频 AI 套话自动加入禁区}

## 推荐口语化词组
{从文章中提取的高频口语词}

## 格式偏好
- 小标题风格：{提取结果}
- 加粗习惯：{提取结果}
- 段落长度：{提取结果}
- 结尾方式：{提取结果}

## 改稿历史观察
<!-- 后续每次改稿自动追加，不影响初始分析 -->
（暂无）
```

### 6C · 跳过

直接创建 `style_guide.md` 空模板（所有字段留空），后续自动学习填充。

### 6.1 创建项目脚手架

无论选 A/B/C，在 Phase 5 完成后，先创建项目目录结构：

```bash
mkdir -p outputs
```

并在 `outputs/` 下创建说明文件：

```markdown
# 产出目录

每篇文章生成在 `outputs/{标题}_{YYYY-MM-DD}/` 下。

完整目录结构：

outputs/{标题}_{YYYY-MM-DD}/
├── metadata.json              ← 视频元信息
├── transcript_raw.txt         ← Whisper 原始转录
├── transcript_corrected.txt   ← LLM 纠错后文案
└── article/
    ├── draft.md               ← AI 初稿
    ├── final.md               ← 终稿
    ├── output.html            ← 排版 HTML
    ├── output-preview.html    ← 手机预览
    ├── illustrations/         ← 正文配图
    └── cover/                 ← 封面图片
```

### 6.2 创建 WORKFLOW.md

无论选 A/B/C，都创建 `WORKFLOW.md`：

```markdown
# WeChatPost 工作流

> 从飞书多维表格到公众号发布的 7 步流水线。
> 说命令词即可触发。说"一条龙"一键到底。

## 🚀 命令速查

| 你说 | 做什么 |
|------|--------|
| "处理视频" | 读飞书→下载→转录→纠错 |
| "写文章" | 逐字稿→公众号初稿 |
| "配图" | shot list→API生图→本地PNG |
| "做封面" | 三维分析→40模板→HTML预览 |
| "排版" | Markdown→公众号HTML |
| "推送" | 推送到公众号草稿箱（需微信凭证） |
| "已发布 https://..." | 发布链接回写飞书 |
| "看板" | 查看全流程进度 |
| "一条龙" | 1→7 全自动 |

## 📋 流水线

```
飞书表格(待处理)          产出目录              子 skill
     │                     │                     │
     ├─1─→ outputs/{标题}_{日期}/     wechatpost-skill (转录)
     │      ├─ transcript_raw.txt
     │      ├─ transcript_corrected.txt
     │      └─ article/
     │          ├─ draft.md   ←2── wechatpost-write
     │          ├─ final.md
     │          ├─ illustrations/ ←3── wechatpost-illustrate
     │          ├─ cover/        ←4── wechatpost-cover
     │          ├─ output.html   ←5── wechatpost-format
     │          ├─ output-preview.html
     │          │                     │
     │          ├─6── wechatpost-push（推送草稿箱）
     │          │                     │
     │          └─7── wechatpost-publish（飞书登记）
```

## 🔧 环境

| 组件 | 检查 |
|------|------|
| Python | `python --version` |
| ffmpeg | `ffmpeg -version` |
| whisper | `python -c "import whisper"` |
| yt-dlp | `yt-dlp --version` |
| lark-cli | `lark-cli auth status` |
| Node.js | `node --version` |
| puppeteer | `cd cover-templates && npm install` |
| 微信推送 | `grep WECHAT_APPID .env`（可选） |

## 🆘 常见问题

| 问题 | 解决 |
|------|------|
| ffmpeg 找不到 | 传 `--ffmpeg` 绝对路径给 transcribe.py |
| 抖音下载失败 | 自动用 parse-video-py 免cookie |
| 转录质量差 | 正常，LLM纠错会修复 |
| 配图跳过 | .env 中 ILLUSTRATE_ENABLED=false |
| lark-cli 过期 | `lark-cli auth login --recommend` |
| 封面截图失败 | `cd cover-templates && npm install` 安装 Node 依赖 |
| 推送失败 | 检查 WECHAT_APPID/SECRET + IP 白名单 |
| 不知道到哪了 | 说"看板" |
```

---

## Phase 7 · 完成

```
🎉 WeChatPost 初始化完成！

环境：Python ✅  ffmpeg ✅  Whisper ✅  yt-dlp ✅  lark-cli ✅  Node.js ✅  puppeteer ✅
微信推送：已配置 / 已跳过
ASR：本地 Whisper tiny
配图：已配置 / 已跳过
风格：{口头描述 / 5篇文章 / 默认}
表格：视频链接（N条记录）

📌 下一步：
- "处理视频" → 开始转录
- "推送" → 排版后推送到公众号草稿箱
- "看板" → 查看进度
- "一条龙" → 一键到底
- 飞书表格链接：https://qj4oqxacrb.feishu.cn/base/ROfJb313faU478s3oXDcKjbknUc
```
