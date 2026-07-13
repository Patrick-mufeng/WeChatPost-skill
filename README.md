# WeChatPost — 视频转公众号全流程 / Video to WeChat Article Pipeline

> 🎯 **一条龙：飞书表格 → 视频转录 → AI 写稿 → AI 配图 → 封面设计 → AI 排版 → 推送 → 飞书登记**
> *One-click pipeline: Feishu table → transcription → AI writing → illustration → cover → formatting → push → publish*

WeChatPost 是一套 AI Agent 驱动的公众号内容生产流水线。把视频链接扔进飞书表格，说一句「一条龙」，8 个阶段自动串联，产出可直接发布到微信公众号的完整图文。

*WeChatPost is an AI agent-driven content production pipeline. Drop a video link into a Feishu table, say "一条龙" (one dragon), and 8 stages execute automatically — producing a complete WeChat Official Account article ready for publishing.*

---

### ✨ 不只是排版——是 AI 原创设计

**拒绝审美疲劳。拒绝千篇一律。**

传统排版工具让你在固定模板里填空。WeChatPost 不同——它让 AI **理解 6 套设计语言的气质内核**，然后为你的每一篇文章**从零原创排版**。同一套"极简蓝"主题，技术教程和深度观点产出的视觉完全不同。AI 自主决定章节标题用左竖条还是编号卡片、引用块用大引号还是渐变底色、分割线用省略号还是细横线——**每篇文章都是独一无二的设计作品**。

还觉得不够？选 **C 模式**：AI 完全抛开预设主题，根据你的文章内容和情绪，自主定义色彩、气质、节奏和全部组件形态，产出一套只属于这一篇文章的视觉方案。

> **不是套模板。不是换颜色。是 AI 理解你的文章后，为它量身定制排版。**

---

## 安装 / Installation

### 方式一：一行安装（推荐）

```bash
zcode skill install https://github.com/Patrick-mufeng/WeChatPost-skill
```

### 方式二：复制项目让 AI 安装

```bash
# 1. 克隆或下载本项目到本地
git clone https://github.com/Patrick-mufeng/WeChatPost-skill.git

# 2. 将整个 WeChatPost-skill 文件夹复制到你的项目根目录

# 3. 在你的项目中对 AI 说：
```

> 请帮我安装 WeChatPost-skill，skill 文件在项目根目录的 `WeChatPost-skill/skills/` 下

AI 会自动将 skill 部署到对应的 skills 目录并完成接入。

### 方式三：手动安装

```bash
git clone https://github.com/Patrick-mufeng/WeChatPost-skill.git
cd WeChatPost-skill

# ZCode
cp -r skills/* .agents/skills/

# Claude Code
cp -r skills/* ~/.claude/skills/
```

### 安装后 / After Install

在项目目录下说「初始化」，按照引导完成环境配置：

*Say "初始化" (initialize) in your project directory to set up:*

```
初始化
```

---

## 目录 / Contents

- [核心能力](#核心能力)
- [项目架构](#项目架构)
- [完整工作流](#完整工作流)
- [各 Skill 详解](#各-skill-详解)
  - [① wechatpost-init — 项目初始化](#-wechatpost-init--项目初始化)
  - [② 转录（主路由）— 视频下载与转文字](#-转录主路由--视频下载与转文字)
  - [③ wechatpost-write — AI 写稿](#-wechatpost-write--ai-写稿)
  - [④ wechatpost-illustrate — 正文配图](#-wechatpost-illustrate--正文配图)
  - [⑤ wechatpost-cover — 封面设计](#-wechatpost-cover--封面设计)
  - [⑥ wechatpost-format — AI 原创排版](#-wechatpost-format--ai-原创排版)
  - [⑦ wechatpost-push — 推送到公众号草稿箱](#-wechatpost-push--推送到公众号草稿箱)
  - [⑧ wechatpost-publish — 发布登记与清理](#-wechatpost-publish--发布登记与清理)
  - [📊 wechatpost-status — 进度看板](#-wechatpost-status--进度看板)
- [命令速查](#命令速查)
- [产出目录结构](#产出目录结构)
- [环境配置](#环境配置)
- [依赖清单](#依赖清单)
- [设计哲学](#设计哲学)
- [常见问题](#常见问题)

---

## 核心能力 / Core Capabilities

| 能力 | 说明 |
|------|------|
| **多平台视频下载** | 支持 30+ 平台（抖音/B 站/小红书/YouTube/Twitter…），自动识别 URL |
| **Whisper 语音转录** | 本地 Whisper 模型将视频语音转为文字，LLM 自动纠错 |
| **AI 写稿** | 6 套标题公式 + 四层去 AI 味自检，输出带评分的标题候选和公众号初稿 |
| **AI 配图** | 基于文章内容自动生成 4–8 张配图，平涂线稿画风 + 固定 IP 角色"小霓"，推送时自动上传微信 CDN |
| **40 套封面模板** | 瑞士极简、赛博霓虹、东方水墨… 三维分析（情绪/领域/调性）自动推荐 |
| **AI 原创排版** | **6 套设计语言 × AI 自主创作**——每篇文章排版独一无二，拒绝审美疲劳。C 模式可完全抛开预设，AI 为单篇文章量身定制视觉方案 |
| **推送到草稿箱** | 通过微信官方 API 直接推送图文到公众号草稿箱（可选） |
| **飞书表格管理** | 视频链接、状态流转、发布记录全部在飞书多维表格中追踪 |

---

## 项目架构 / Architecture

```
WeChatPost-skill/
│
├── README.md                          ← 你在读这个
├── LICENSE                            ← AGPL-3.0
├── style_guide.md                     ← 个人风格指南
│
├── skills/                            ← Skill 目录（AI 工具从此加载）
│   ├── wechatpost-skill/              ← 主路由 + 总协议
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   ├── transcribe.py          ← 视频下载 + Whisper 转录
│   │   │   └── vendor/parse_video_py/ ← 30+ 平台 URL 解析器
│   │   ├── cover-templates/           ← 40 套封面模板
│   │   │   ├── design-principles.md
│   │   │   ├── preview-shell.html
│   │   │   ├── screenshot.js          ← 封面 HTML → PNG 渲染
│   │   │   ├── package.json           ← Node 依赖（puppeteer）
│   │   │   └── 01-swiss-minimal.md … 40-de-stijl.md
│   │   └── shared-references/
│   │       └── writing-principles.md   ← 写作原则（5 原型 + 6 公式 + 4 层去 AI 味）
│   │
│   ├── wechatpost-init/               ← ① 初始化
│   ├── wechatpost-write/              ← ③ 写稿
│   ├── wechatpost-illustrate/         ← ④ 配图
│   │   ├── scripts/                   ← 生图脚本（mitu）
│   │   └── references/                ← 风格 DNA / IP 设定 / Prompt 模板
│   ├── wechatpost-cover/              ← ⑤ 封面
│   ├── wechatpost-format/             ← ⑥ AI 原创排版
│   │   ├── references/
│   │   │   ├── design-spec.md          ← 平台底层规范（1057 行宪法）
│   │   │   ├── theme-index.md          ← 6 套主题注册表
│   │   │   ├── common-components.md    ← 通用组件设计参考
│   │   │   └── theme-*.md              ← 6 套设计语言文件
│   │   └── scripts/
│   │       └── validate_gzh_html.py    ← HTML 合规校验
│   ├── wechatpost-push/               ← ⑦ 推送
│   │   └── scripts/wechat_push.py     ← 微信 API 推送脚本
│   ├── wechatpost-publish/            ← ⑧ 发布登记
│   └── wechatpost-status/             ← 📊 看板
│
└── outputs/                           ← 产出目录
    └── {标题}_{YYYY-MM-DD}/
        ├── metadata.json
        ├── transcript_raw.txt
        ├── transcript_corrected.txt
        └── article/
            ├── draft.md
            ├── final.md
            ├── output.html
            ├── output-preview.html
            ├── illustrations/
            │   ├── shot-list.md
            │   └── 01-{主题}.png
            └── cover/
                ├── preview.html
                ├── cover-2x35.png
                ├── cover-1x1.png
                └── cover-combined.png
```

---

## 完整工作流 / Complete Workflow

```
飞书表格（待处理）
    │
①  初始化 (wechatpost-init)
    环境检查 → API 配置 → 推送配置（可选）→ ASR 引擎 → 飞书验证 → 风格设定
    │
②  转录 (主路由)
    读飞书 → 标记"处理中" → 下载视频 → Whisper 转录 → LLM 纠错 → 写回飞书
    产出: transcript_corrected.txt
    │
③  写稿 (wechatpost-write)
    分析文案 → 确定原型 → 规划结构 → 写初稿 → 四层去 AI 味 → 6 公式生成 5 标题
    产出: draft.md → final.md（用户编辑后）
    │
④  配图 (wechatpost-illustrate)
    读 final.md → 配色分析 → shot list → API 生图 → 本地 PNG → 插入 final.md
    产出: illustrations/*.png
    │
⑤  封面 (wechatpost-cover)
    A/B/C 三选一 → 三维分析 → 模板/AI 设计 → 预览 HTML → screenshot.js 渲染 PNG
    产出: cover/preview.html + cover-*.png
    │
⑥  AI 原创排版 (wechatpost-format)
    分析文章基因 → A/B/C 三选一 → 读设计语言 → AI 理解气质 → 为本文原创设计
    → 生成 output.html → 脚本校验 → 交付
    产出: output.html + output-preview.html
    │
⑦  推送 (wechatpost-push)【可选】
    读 output.html + cover-combined.png → 上传图片到微信 CDN → 微信 API → 草稿箱
    产出: media_id（写回飞书备注）
    │
⑧  发布登记 (wechatpost-publish)
    确认发布链接 → 飞书写回
    状态: 已完成
```

---

## 各 Skill 详解 / Skill Details

### ① wechatpost-init — 项目初始化

**触发词**：`初始化` / `init` / `首次使用` / `开始使用` / `配置`

首次使用必跑。7 个阶段：环境检查 → API 配置 → 公众号推送配置 → ASR 引擎选择 → 飞书表格验证 → 风格设定 → 创建 `style_guide.md`。

**特点**：一次配置，全流程复用。自动检测缺失依赖并引导安装。

---

### ② 转录（主路由）— 视频下载与转文字

**触发词**：`处理视频` / `转录` / `视频转文案`

5 步流程：读飞书待处理 → 标记处理中 → 下载视频 + Whisper 转录 → LLM 纠错 → 写回飞书。

**特点**：
- 支持 30+ 平台（抖音/B 站/小红书/YouTube/Twitter…），自动识别 URL
- 双路径架构：parse-video-py（国内平台，免 cookie）+ yt-dlp（海外平台）
- LLM 纠错修复同音错字、专有名词，不改写风格

---

### ③ wechatpost-write — AI 写稿

**触发词**：`写文章` / `写初稿` / `write` / `出稿`

7 Phase 流程：定位输入 → 内容分析 → 结构规划 → 写初稿 → 四层去 AI 味 → 标题生成 → 落盘。

**特点**：
- 5 种文章原型（测评/工具/教程/观点/故事），自动识别
- 6 套标题公式（数字清单/对比冲突/结果导向/场景共鸣/反常识/工具模板）
- 五维评分 + 四道质量滤网，输出 Top 5 标题候选
- 四层去 AI 味自检：硬规则 → 风格一致 → 内容质量 → 活人感

---

### ④ wechatpost-illustrate — 正文配图

**触发词**：`配图` / `插图` / `做插图` / `illustrate` / `正文配图`

7 Phase 流程：开关检查 → 读文章配色分析 → shot list → 用户确认 → 逐张生图 → 插入 final.md → 交付。

**特点**：
- 固定 IP 角色"小霓"：赛博风格女性操作员，深藏蓝头发 + 瓷白皮肤 + 白色圆点眼
- 填色本画风：白底 + 黑色手绘线稿 + 扁平色块平涂（无渐变/无阴影/无纹理）
- 5 套情绪色板（冷峻蓝灰/温暖暖调/激昂对比/轻松明亮/严肃大地）
- 自动配色分析，根据文章情绪匹配色板

---

### ⑤ wechatpost-cover — 封面设计

**触发词**：`做封面` / `封面` / `cover` / `公众号封面` / `设计封面`

6 Phase 流程：读终稿 → 三维分析（情绪/领域/调性）→ A/B/C 设计 → 提取文案 → 生成预览 HTML + 渲染 PNG → 改稿循环 → 自检。

**特点**：
- **40 套封面模板**：覆盖 5 种情绪（冷峻/温暖/激昂/轻松/严肃），从瑞士极简到赛博霓虹到东方水墨
- A 推荐模板 / B 自己描述 / C AI 自主设计，三选一
- 双版封面输出：2.35:1（公众号首图）+ 1:1（朋友圈分享）+ 并排拼接图
- 设计规范：60-30-10 配色法则、≤4 色、对比度 ≥ 4.5:1

---

### ⑥ wechatpost-format — AI 原创排版

**触发词**：`排版` / `format` / `转HTML` / `转公众号` / `公众号排版`

5 Phase 流程：分析文章基因 → A/B/C 三选一 → 读设计语言原创设计 → 生成 output.html + 预览页 → 脚本校验交付。

**特点——这才是核心**：

- 🎨 **6 套设计语言**，不是 6 套模板：

| 主题 | 主色 | 气质 | 一句话 |
|------|------|------|--------|
| 极简蓝 | `#2563eb` | 克制·理性·呼吸感 | 蓝色锚点引导阅读路径，灰阶承担 95% 层级 |
| 暖纸墨 | `#b8532a` | 温度·杂志感·细线分隔 | 翻杂志的仪式感，细横线是视觉骨架 |
| 暗夜青 | `#00d4aa` | 科技·终端美学·霓虹克制 | 终端命令行人格，青色信号灯在暗底闪烁 |
| 森语绿 | `#4a7c59` | 自然·侘寂·大留白 | 留白本身就是设计，主色仅占 1% 像素 |
| 绯红编 | `#c1292e` | 编辑风骨·红白张力 | 报刊编辑的红色标记笔，全文红色 ≤5 处 |
| 墨金雅 | `#1e1f23`+`#c9a96e` | 墨色·金饰·经典比例 | 精装书质感，金色配额预算制 |

- ✨ **AI 理解设计语言后原创设计**——同主题不同文章视觉完全不同。AI 自主决定：章节标题形态、引用块风格、分割线样式、代码块深浅、图片圆角阴影… 每篇文章独一无二
- 🎯 **C 模式全原创**：完全抛开预设，AI 为单篇文章量身定制色彩/气质/节奏/全部组件，可命名登记为常驻主题
- 🔒 **三层文件体系**：design-spec.md（宪法·平台约束）+ theme-*.md（法律·设计语言）+ common-components.md（法规·通用参考）
- 🛡️ **确定性脚本校验**：`validate_gzh_html.py` 检查标签合规 + `<span leaf="">` 包裹 + 半角标点，0 ERROR 才交付
- 📱 **iPhone 模拟器预览**：暗色双栏界面，实时渲染，一键复制到公众号

---

### ⑦ wechatpost-push — 推送到公众号草稿箱

**触发词**：`推送` / `push` / `推到公众号` / `推送到公众号`

4 Phase 流程：检查微信凭证 → 确认推送 → 换 token + 上传封面 + 创建草稿 → 回写飞书。

**特点**：
- 纯标准库实现（urllib + json），零外部依赖
- 仅入草稿箱，不自动群发
- 无凭证时自动跳过，提示手动粘贴 HTML

---

### ⑧ wechatpost-publish — 发布登记与清理

**触发词**：`已发布` / `发布登记` / `publish` / `发布链接` / `发出去了`

4 Phase 流程：确认发布信息（链接+时间）→ 回写飞书 → 确认交付 → 自检。

**特点**：将公众号发布链接、发布时间、发布状态全部写回飞书，完成闭环追踪。

---

### 📊 wechatpost-status — 进度看板

**触发词**：`看板` / `状态` / `status` / `进度` / `到哪了` / `今天干什么`

3 Phase 流程：验证飞书连接 → 读取全部记录 → 渲染看板（汇总 + 每条详情 + 进度条 + 下一步操作提示）。

**特点**：
- 可视化全流程进度：待处理/处理中/已转录/已写稿/已排版/已完成 一目了然
- 断点续跑友好：中断后回来看板，知道从哪继续

---

## 命令速查 / Command Reference

| 你说 | 做什么 |
|------|--------|
| `初始化` | 首次使用，配置环境和 API |
| `处理视频` | 读飞书 → 下载 → 转录 → 纠错 |
| `写文章` | 逐字稿 → 公众号初稿（含 5 个标题候选） |
| `改好了` / `定稿` | 将 draft.md 另存为 final.md |
| `配图` | shot list → API 生图 → 本地 PNG（推送时自动上传微信 CDN） |
| `做封面` | 三维分析 → 模板/AI 设计 → HTML 预览 → PNG |
| `排版` | 分析文章 → 选设计语言 → AI 原创排版 → HTML → 校验 |
| `推送` | 推送到公众号草稿箱（需微信凭证） |
| `已发布 https://...` | 飞书登记 |
| `看板` | 查看全流程进度 |
| `一条龙` | 转录 → 写稿 → 配图 → 封面 → **AI 原创排版** → 推送 → 登记（全自动） |

**一条龙失败策略**：
- 致命失败（转录/写稿）→ 标记当前文章失败，继续处理队列中下一篇
- 非致命失败（配图/封面/排版）→ 跳过该阶段，继续后续流程

**断点续跑**：会话中断后重新说「一条龙」，Agent 自动检测各阶段产出文件从断点处继续。也可用单独命令恢复。

---

## 产出目录结构 / Output Directory Structure

```
outputs/{标题}_{YYYY-MM-DD}/
├── metadata.json              ← 视频元信息（标题/作者/时长/平台）
├── transcript_raw.txt         ← Whisper 原始转录
├── transcript_corrected.txt   ← LLM 纠错后文案
└── article/
    ├── draft.md               ← AI 初稿（含标题候选 + 简介 + 正文）
    ├── final.md               ← 终稿（用户编辑后）
    ├── output.html            ← AI 原创排版 HTML（公众号粘贴用）
    ├── output-preview.html    ← 手机预览 + 一键复制
    ├── illustrations/
    │   ├── shot-list.md       ← 配图分镜计划
    │   └── 01-{主题}.png      ← 本地 PNG（推送时自动上传微信 CDN）
    └── cover/
        ├── preview.html       ← 双版封面预览
        ├── cover-2x35.png     ← 公众号首图（2.35:1）
        ├── cover-1x1.png      ← 朋友圈分享（1:1）
        └── cover-combined.png ← 并排拼接（推送用）
```

---

## 环境配置 / Environment Setup

### 必需的 API / 工具 / Required APIs & Tools

| 配置项 | 用途 | 获取方式 |
|--------|------|----------|
| `YUNWU_API_KEY` | AI 配图生图（云雾 API） | https://yunwu.ai/register?aff=zM1f |
| `WECHAT_APPID` | 公众号草稿箱推送（可选） | 公众号后台 → 设置与开发 → 基本配置 |
| `WECHAT_APPSECRET` | 同上 | 同上 |
| 飞书多维表格 | 任务队列与状态追踪 | 项目内置 Base Token |

### `.env` 文件模板 / .env Template

```env
# ── 生图 API（云雾）──
YUNWU_API_KEY=sk-your-api-key-here
YUNWU_BASE_URL=https://yunwu.ai/

# ── 配图开关 ──
ILLUSTRATE_ENABLED=true

# ── 微信公众号 API（可选）──
WECHAT_APPID=wx1234567890
WECHAT_APPSECRET=your-appsecret-here
WECHAT_AUTHOR=你的作者名
```

---

## 依赖清单 / Dependencies

### Python（转录 + 配图）

| 包 | 用途 |
|----|------|
| `openai-whisper` | 语音转录 |
| `yt-dlp` | 海外平台视频下载 |
| `httpx` | HTTP 客户端（API 调用） |
| `aiohttp` | 异步 HTTP |
| `pyyaml` | YAML 解析 |

安装：`pip install -r requirements.txt`

### Node.js（封面截图）

| 包 | 用途 |
|----|------|
| `puppeteer` | 浏览器截图 + 图片合并 |

安装：`cd cover-templates && npm install`

### 系统工具

| 工具 | 用途 |
|------|------|
| `ffmpeg` | 视频音频提取 |
| `lark-cli` | 飞书多维表格操作 |

---

## 设计哲学 / Design Philosophy

### 写作：克制但高点击

标题不夸大、不标题党，但必须让读者产生"想看"的冲动。6 套公式确保覆盖不同的点击诱因，4 道滤网守住底线。

### 配图：填色本风格

黑色手绘线稿 + 扁平色块平涂。小霓 IP 固定配色保持品牌一致性，其余元素根据文章情绪自动选色板。

### 封面：模板 + 自由

40 套模板覆盖 5 种情绪调性 × 6 个内容领域，同时支持用户自由描述或 AI 自主创作。

### 排版：AI 原创设计——不是套模板

这是 WeChatPost 排版与所有其他公众号排版工具的根本区别：

- **不是模板填充**——AI 理解 6 套设计语言的气质内核，为每篇文章从零原创排版
- **不是换颜色**——同一主题下，技术教程和深度观点产出的视觉完全不同
- **不是千篇一律**——AI 自主决定每个组件的形态、比例、节奏。每篇文章独一无二
- **C 模式完全释放**——抛开所有预设，AI 为单篇文章量身定制视觉方案
- **脚本兜底**——`validate_gzh_html.py` 确定性校验，平台合规不靠 AI "自觉"
- **三层文件体系**——宪法（平台约束）→ 法律（设计语言）→ 法规（通用参考），层层约束但层层自由

### 自检文化

每个子 Skill 完成后必须**重新读取产出文件**，逐项验证，不依赖记忆。排版阶段额外通过确定性脚本校验。失败 → 重写 → re-read → 仍不通过 → 输出 `❌ 自检失败`。

---

## 常见问题 / FAQ

| 问题 | 解决 |
|------|------|
| ffmpeg 找不到 | 传 `--ffmpeg` 绝对路径给 transcribe.py |
| 抖音下载 403 | 直链过期，重新解析即可 |
| 转录质量差 | 正常现象，LLM 纠错会自动修复 |
| 配图跳过 | `.env` 中 `ILLUSTRATE_ENABLED=false`，改为 `true` |
| lark-cli 过期 | `lark-cli auth login --recommend` |
| 封面截图失败 | `cd cover-templates && npm install` 安装 puppeteer |
| 推送失败 | 检查 `WECHAT_APPID`/`WECHAT_APPSECRET` 配置 + IP 白名单 |
| 推送报错 40164 | 公众号后台 → 基本配置 → 将本机出口 IP 加入白名单 |
| 排版粘贴后样式丢失 | 已通过 `<span leaf="">` 包裹 + 脚本校验解决 |
| 排版千篇一律 | 不会——AI 为每篇文章原创设计，同主题不同文章视觉不同 |
| 不知道到哪了 | 说「看板」 |
| 想一键到底 | 说「一条龙」 |

---

## License

**AGPL-3.0 © 2026 Patrick**

本项目采用 **GNU AGPL-3.0** 协议，要点：

1. **必须署名** — 保留版权声明
2. **衍生品必须开源** — 任何修改版本、Fork、二次分发，必须以 AGPL-3.0（或兼容协议）公开发布，提供完整源代码
3. **网络服务也要开源** — 即使只是把修改版本部署成 SaaS / Web 服务给别人用而不分发代码，也要公开源代码（这是 AGPL 区别于 GPL 的核心）
4. **不允许闭源、专有化、仅付费分发**

完整条款见 [LICENSE](LICENSE)。
