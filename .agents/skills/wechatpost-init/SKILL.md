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
Phase 1: 环境检查（Python/ffmpeg/whisper/yt-dlp/lark-cli）
  ↓
Phase 2: API 配置（云雾+beeimg+开关）
  ↓
Phase 3: ASR 引擎选择（Whisper/火山）
  ↓
Phase 4: 飞书表格验证
  ↓
Phase 5: 风格设定（口头描述/提供文章/跳过） + 创建项目文件
  ↓
Phase 6: 完成提示
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
python --version         2>&1
ffmpeg -version          2>&1 | head -1
python -c "import whisper; print('whisper OK')" 2>&1
yt-dlp --version         2>&1
python -c "import httpx; print('httpx OK')" 2>&1
lark-cli auth status     2>&1
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

全部通过 ✅
```

缺什么自动尝试安装，或给出具体命令：

| 缺失 | Windows | macOS | Linux |
|------|---------|-------|-------|
| Python | https://python.org 下载安装 | `brew install python` | `sudo apt install python3` |
| ffmpeg | `winget install Gyan.FFmpeg` | `brew install ffmpeg` | `sudo apt install ffmpeg` |
| Python 包 | `pip install -r requirements.txt` | 同上 | 同上 |
| lark-cli | `npm install -g @larksuite/cli` | 同上 | 同上 |

> `requirements.txt` 和安装脚本在 `wechatpost-skill/` 下，包含所有 Python 依赖。
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

# ── 图床 API（beeimg）── 配图上传获取公开URL ──
# 登录：https://www.beeimg.cn 获取 Bearer Token
BEEIMG_TOKEN=your-bearer-token-here
BEEIMG_BASE_URL=https://www.beeimg.cn

# ── 配图开关 ──
# true=启用配图（需填上面两组Key） false=跳过配图阶段
ILLUSTRATE_ENABLED=false
EOF
```

### 2.3 引导用户

```
⚙️ 配图功能需要两组 API：

① 云雾 API（gpt-image-2 生图）
   注册：https://yunwu.ai/register?aff=zM1f
   → 复制 API Key 填入 .env 的 YUNWU_API_KEY=

② beeimg 图床（图片上传）
   登录：https://www.beeimg.cn
   → 后台 → API Token → 复制填入 BEEIMG_TOKEN=

现在怎么做？
A) 我去注册，填好 Key 后说"配置完成"
B) 先跳过配图（ILLUSTRATE_ENABLED=false），后面可重新初始化
```

选 B → `.env` 已创建，`ILLUSTRATE_ENABLED=false`。后续配图阶段检测到此值自动跳过。

### 2.4 已有 .env → 验证

```
📋 API 配置
  □ YUNWU_API_KEY：已配置 ✅ / 未填写 ⚠️
  □ BEEIMG_TOKEN：已配置 ✅ / 未填写 ⚠️
  □ ILLUSTRATE_ENABLED：true / false
```

---

## Phase 3 · ASR 引擎选择

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

## Phase 4 · 飞书表格验证

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

## Phase 5 · 风格设定 + 创建项目文件

### 5.0 询问风格模式

```
✏️ 风格设定——让 AI 写得像你

A) 口头描述 — 简单说说你的风格偏好
B) 提供文章 — 5 篇以上你写过的文章，AI 分析后自动提取风格
C) 先跳过 — 用默认风格，后续每次改稿 AI 自动学习

选哪个？
```

### 5A · 口头描述

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

### 5B · 提供文章分析（≥5 篇）

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

### 5C · 跳过

直接创建 `style_guide.md` 空模板（所有字段留空），后续自动学习填充。

### 5.1 创建 WORKFLOW.md

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
| "配图" | shot list→API生图→图床 |
| "做封面" | 三维分析→40模板→HTML预览 |
| "排版" | Markdown→公众号HTML |
| "已发布 https://..." | 发布链接回写飞书 |
| "看板" | 查看全流程进度 |
| "一条龙" | 1→6 全自动 |

## 📋 流水线

```
飞书表格(待处理)          产出目录              子 skill
     │                     │                     │
     ├─1─→ outputs/{标题}_{日期}/     wechatpost-skill (转录)
     │      ├─ transcript_raw.txt
     │      ├─ transcript_corrected
     │      └─ article/
     │          ├─ draft.md   ←2── wechatpost-write
     │          ├─ final.md
     │          ├─ illustrations/ ←3── wechatpost-illustrate
     │          ├─ cover/        ←4── wechatpost-cover
     │          └─ output.html   ←5── wechatpost-format
     │                                │
     └─6──────────────────────────────┘  wechatpost-publish
```

## 🔧 环境

| 组件 | 检查 |
|------|------|
| Python | `python --version` |
| ffmpeg | `ffmpeg -version` |
| whisper | `python -c "import whisper"` |
| yt-dlp | `yt-dlp --version` |
| lark-cli | `lark-cli auth status` |

## 🆘 常见问题

| 问题 | 解决 |
|------|------|
| ffmpeg 找不到 | 传 `--ffmpeg` 绝对路径给 transcribe.py |
| 抖音下载失败 | 自动用 parse-video-py 免cookie |
| 转录质量差 | 正常，LLM纠错会修复 |
| 配图跳过 | .env 中 ILLUSTRATE_ENABLED=false |
| lark-cli 过期 | `lark-cli auth login --recommend` |
| 不知道到哪了 | 说"看板" |
```

---

## Phase 6 · 完成

```
🎉 WeChatPost 初始化完成！

环境：Python ✅  ffmpeg ✅  Whisper ✅  yt-dlp ✅  lark-cli ✅
ASR：本地 Whisper tiny
配图：已配置 / 已跳过
风格：{口头描述 / 5篇文章 / 默认}
表格：视频链接（N条记录）

📌 下一步：
- "处理视频" → 开始转录
- "看板" → 查看进度
- "一条龙" → 一键到底
- 飞书表格链接：https://qj4oqxacrb.feishu.cn/base/ROfJb313faU478s3oXDcKjbknUc
```
