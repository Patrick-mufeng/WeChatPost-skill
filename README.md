# WeChatPost — 视频转公众号全流程 / Video to WeChat Article Pipeline

> 🎯 **一条龙：飞书表格 → 视频转录 → AI 写稿 → 配图 → 封面 → 排版 → 推送 → 飞书登记**
> *One-click pipeline: Feishu table → transcription → AI writing → illustration → cover → formatting → push → publish*

WeChatPost 是一套 AI Agent 驱动的公众号内容生产流水线。把视频链接扔进飞书表格，说一句「一条龙」，8 个阶段自动串联，产出可直接发布到微信公众号的完整图文。

*WeChatPost is an AI agent-driven content production pipeline. Drop a video link into a Feishu table, say "一条龙" (one dragon), and 8 stages execute automatically — producing a complete WeChat Official Account article ready for publishing.*

---

## 安装 / Installation

### GitHub 安装（推荐） / GitHub Install (Recommended)

```bash
# ZCode
zcode skill install https://github.com/Patrick-mufeng/WeChatPost-skill

# Claude Code
claude mcp add https://github.com/Patrick-mufeng/WeChatPost-skill
```

### 手动安装 / Manual Install

```bash
git clone https://github.com/Patrick-mufeng/WeChatPost-skill.git
cd WeChatPost-skill

# ZCode
cp -r skills/* .agents/skills/

# Claude Code
cp -r skills/* ~/.claude/skills/

# Other AI tools
# Point your tool's skill directory to skills/
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
  - [⑥ wechatpost-format — Markdown 排版](#-wechatpost-format--markdown-排版)
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
| **AI 配图** | 基于文章内容自动生成 4–8 张配图，平涂线稿画风 + 固定 IP 角色"小霓" |
| **40 套封面模板** | 瑞士极简、赛博霓虹、东方水墨… 三维分析（情绪/领域/调性）自动推荐 |
| **公众号排版** | Markdown → 微信公众号兼容 HTML，手机预览 + 一键复制 |
| **推送到草稿箱** | 通过微信官方 API 直接推送图文到公众号草稿箱（可选） |
| **飞书表格管理** | 视频链接、状态流转、发布记录全部在飞书多维表格中追踪 |

---

## 项目架构 / Architecture

```
WeChatPost-skill/
│
├── README.md                          ← 你在读这个
├── .env                               ← API 密钥（不入 git）
├── style_guide.md                     ← 个人风格指南
├── WORKFLOW.md                        ← 工作流速查（初始化时生成）
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
│   │   │   ├── package.json           ← Node 依赖（puppeteer + canvas）
│   │   │   └── 01-swiss-minimal.md … 40-de-stijl.md
│   │   └── shared-references/
│   │       └── writing-principles.md   ← 写作原则（5 原型 + 6 公式 + 4 层去 AI 味）
│   │
│   ├── wechatpost-init/               ← ① 初始化
│   ├── wechatpost-write/              ← ③ 写稿
│   ├── wechatpost-illustrate/         ← ④ 配图
│   │   ├── scripts/                   ← 生图 + 图床上传脚本
│   │   └── references/                ← 风格 DNA / IP 设定 / Prompt 模板
│   ├── wechatpost-cover/              ← ⑤ 封面
│   ├── wechatpost-format/             ← ⑥ 排版
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
            │   ├── uploaded-keys.json
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
    读 final.md → 配色分析 → shot list → API 生图 → beeimg 图床 → 插入 final.md
    产出: illustrations/*.png + uploaded-keys.json
    │
⑤  封面 (wechatpost-cover)
    A/B/C 三选一 → 三维分析 → 模板/AI 设计 → 预览 HTML → screenshot.js 渲染 PNG
    产出: cover/preview.html + cover-*.png
    │
⑥  排版 (wechatpost-format)
    A/B/C 三选一 → Markdown → 公众号兼容 HTML → 手机预览 + 一键复制
    产出: output.html + output-preview.html
    │
⑦  推送 (wechatpost-push)【可选】
    读 output.html + cover-combined.png → 微信 API → 草稿箱
    产出: media_id（写回飞书备注）
    │
⑧  发布登记 (wechatpost-publish)
    确认发布链接 → 飞书写回 → 删除 beeimg 图床图片
    状态: 已完成
```

---

## 各 Skill 详解 / Skill Details

### ① wechatpost-init — 项目初始化

**触发词**：`初始化` / `init` / `首次使用` / `开始使用` / `配置`

首次使用必跑。7 个阶段：

| 阶段 | 内容 |
|------|------|
| Phase 1 | 环境检查：Python / ffmpeg / Whisper / yt-dlp / httpx / lark-cli / Node.js / puppeteer / canvas / 微信凭证（可选） |
| Phase 2 | API 配置：云雾 API（AI 生图）+ beeimg 图床（图片上传）|
| Phase 3 | 公众号推送配置：询问是否启用，引导获取 APPID/APPSECRET，验证凭证 |
| Phase 4 | ASR 引擎选择：本地 Whisper（推荐）/ 火山引擎 ASR |
| Phase 5 | 飞书表格验证：测试连接，检查字段与记录数 |
| Phase 6 | 风格设定：口头描述 / 提供 5 篇文章 AI 分析 / 跳过（默认风格） |
| Phase 7 | 完成提示 + 创建 `style_guide.md` 和 `WORKFLOW.md` |

---

### ② 转录（主路由）— 视频下载与转文字

**触发词**：`处理视频` / `转录` / `视频转文案`

5 步流程：

| 步骤 | 操作 |
|------|------|
| Step 1 | 从飞书表格读取「待处理」记录 |
| Step 2 | 标记记录为「处理中」 |
| Step 3 | 下载视频 + Whisper 转录（自动选解析器：抖音/B 站/小红书 → parse-video-py；YouTube/海外 → yt-dlp） |
| Step 4 | LLM 纠错（修复同音错字、专有名词、合并碎片句，不改风格） |
| Step 5 | 更新飞书表格（标题/作者/时长/平台/文案/字数/状态 → 已转录） |

**支持的平台**：抖音、B 站、小红书、快手、YouTube、Twitter、微博、优酷、腾讯视频、Instagram 等 30+ 平台。

**双路径架构**：

| 路径 | 平台 | 方式 | 需要 Cookie？ |
|------|------|------|--------------|
| parse-video-py | 抖音/B 站/小红书/快手 | httpx 直链下载 | 不需要 |
| yt-dlp | YouTube/海外 | yt-dlp 下载 | 可选 |

---

### ③ wechatpost-write — AI 写稿

**触发词**：`写文章` / `写初稿` / `write` / `出稿`

7 Phase 流程：

| Phase | 内容 |
|-------|------|
| Phase 0 | 定位输入文件（`transcript_corrected.txt` + `metadata.json`） |
| Phase 1 | 内容分析：类型识别（测评/工具/教程/观点/故事）+ 核心主题 + 结构节点 |
| Phase 2 | 结构规划：开头钩子 → 3-5 板块 → 收尾，预计字数 |
| Phase 3 | 写初稿：像聊天不像报告，知识"聊着聊着掏出来"，保留原视频个性 |
| Phase 4 | 四层去 AI 味自检：L1 硬规则扫描 → L2 风格一致 → L3 内容质量 → L4 活人感 |
| Phase 5 | 标题生成：6 套公式各生 1-2 个 → 4 道滤网 → 五维评分 → 输出 Top 5 |
| Phase 6 | 落盘：`draft.md`（含 frontmatter + 标题候选 + 简介 + 正文） |
| Phase 7 | 自检 + 输出 |

**6 套标题公式**：

| 公式 | 骨架 | 示例 |
|------|------|------|
| 数字清单型 | 数字 + 角度 + 价值点 | "Claude Code 的 3 个隐藏用法，第 2 个太省事了" |
| 对比冲突型 | A vs B + 结论暗示 | "用 Whisper 转录 vs 人工听写，差距不止 10 倍" |
| 结果导向型 | 人群 + 收益 + 方式 | "想做视频转文章？这份全流程指南请收好" |
| 场景共鸣型 | 当你在...时，其实... | "每次改稿改到凌晨，其实你缺的不是时间" |
| 反常识型 | 你以为...其实... | "为什么越懂 AI 的人，越不急着用 AI 写文章？" |
| 工具模板型 | 我把...整理出来了 | "我把视频转录→发公众号的全流程整理成了模板" |

**五维评分**：钩力(30%) + 清晰度(25%) + 情绪值(20%) + 关键词(15%) + 差异化(10%)

**四道质量滤网**：≤30 字 / 不编造数据 / 禁用过度情绪词 / 对象+场景+收益

**五种文章原型**：测评型 / 工具型 / 教程型 / 观点型 / 故事型

---

### ④ wechatpost-illustrate — 正文配图

**触发词**：`配图` / `插图` / `做插图` / `illustrate` / `正文配图`

7 Phase 流程：

| Phase | 内容 |
|-------|------|
| Phase 0 | API Key 检查（`YUNWU_API_KEY` + `BEEIMG_TOKEN`） |
| Phase 1 | 读 `final.md` → 提炼核心观点 + 配色分析（5 套情绪色板选一） |
| Phase 2 | 出 shot list（4-8 张配图计划，标注色板） |
| Phase 3 | 用户确认 shot list |
| Phase 4 | 逐张生图（云雾 API → gpt-image-2）→ 上传 beeimg 图床 |
| Phase 5 | 将图床 URL 插入 `final.md` |
| Phase 6 | 交付汇总 |
| Phase 7 | 自检 |

**IP 角色 — 小霓**：

赛博风格女性操作员，固定造型与配色：

| 部位 | 色号 | 说明 |
|------|------|------|
| 头发 | `#2c3e6b` 深藏蓝 | 几何波波头，平涂 |
| 皮肤 | `#f5efe6` 瓷白 | 平涂 |
| 眼 | 白色圆点 | IP 识别核心 |
| 工装/马甲 | `#8a9b8e` 灰绿 | 极简 oversize |
| 护目镜/耳机 | `#b0b0b0` 银灰 | 推到额头上或挂在颈间 |

**画风**：白底 + 黑色手绘线稿 + 扁平色块平涂（填色本风格）。无渐变、无阴影、无纹理。

**5 套情绪色板**（用于非小霓元素的上色）：

| 情绪 | 色板 | 主色 | 辅色 | 底色 |
|------|------|------|------|------|
| 冷峻 | 蓝灰调 | `#7fa3b3` | `#c4d7e0` | `#e8f0f4` |
| 温暖 | 暖调 | `#e8c4a2` | `#f0dcc8` | `#faf0e6` |
| 激昂 | 对比调 | `#d4786e` | `#e8b4a8` | `#f5e0dc` |
| 轻松 | 明亮调 | `#c4d4a0` | `#e0e8c8` | `#f2f6e8` |
| 严肃 | 大地调 | `#b8a89a` | `#d4c8bc` | `#ede5df` |

**所需 API**：
- 云雾 API（gpt-image-2 生图）— `YUNWU_API_KEY`
- beeimg 图床（Lsky Pro API）— `BEEIMG_TOKEN`

---

### ⑤ wechatpost-cover — 封面设计

**触发词**：`做封面` / `封面` / `cover` / `公众号封面` / `设计封面`

6 Phase 流程：

| Phase | 内容 |
|-------|------|
| Phase 0 | 读 `final.md` |
| Phase 1 | 三维分析：情绪调性（冷峻/温暖/激昂/轻松/严肃）+ 内容领域（科技/商业/生活/教育/娱乐/人文） |
| Phase 2 | 设计方式选择：A 推荐模板 / B 自己描述 / C AI 自主设计 |
| Phase 3 | 提取封面文案（主标题 ≤15 字 + 描述 ≤30 字 + 3-5 标签） |
| Phase 4 | 生成预览 HTML（2.35:1 + 1:1 双版）→ screenshot.js 渲染 PNG |
| Phase 5 | 改稿循环（最多 3 轮） |
| Phase 6 | 自检 |

**A/B/C 三选一设计方式**：

| 选项 | 说明 |
|------|------|
| A. 推荐模板 | 从 40 套模板中按情绪+领域推荐 3 个，支持"换一批" |
| B. 自己描述 | 用户自由描述风格（如"黑白极简，大字标题，不要装饰"） |
| C. AI 自主设计 | 不套模板，根据设计规范全新创作，要求有设计感 |

**40 套封面模板**：

| 情绪 | 模板 |
|------|------|
| 冷峻 | 瑞士极简 · 赛博霓虹 · 玻璃态 · 粗野主义 · 全息未来 · 工程蓝图 · 复古终端 · 霓虹黑色 · 包豪斯 · 液态金属 · 故障艺术 · 混凝土粗野 · 视幻艺术 · 风格派 |
| 温暖 | 柔光暖调 · 水彩渲染 · 植物标本 · 洛可可 |
| 激昂 | 暗金奢华 · 装饰艺术 · 朋克拼贴 · 维多利亚 · 彩绘玻璃 · 构成主义 · 蒸汽朋克 |
| 轻松 | 孟菲斯 · 蒸汽波 · 波普艺术 · 迷幻 60s · 水磨石 · 迈阿密热浪 · 像素艺术 · 千禧美学 |
| 严肃 | 社论杂志 · 东方水墨 · 星座星图 · 侘寂美学 · 报纸印刷 · 折纸艺术 · 浮世绘 |

**设计规范**：60-30-10 配色法则、≤4 色、对比度 ≥ 4.5:1、标题 ≥ 48px、留白 ≥ 35%。

---

### ⑥ wechatpost-format — Markdown 排版

**触发词**：`排版` / `format` / `转HTML` / `转公众号` / `公众号排版`

4 Phase 流程：

| Phase | 内容 |
|-------|------|
| Phase 0 | 读 `final.md` + 前置检查（封面/配图状态） |
| Phase 1 | 排版方式选择：A 预设主题 / B 自己描述 / C AI 自主设计 |
| Phase 2 | 生成 `output.html`（公众号兼容 HTML） |
| Phase 3 | 生成 `output-preview.html`（手机预览 + 一键复制） |
| Phase 4 | 自检 + 交付 |

**3 套预设排版主题**：

| 主题 | 背景 | 正文 | 强调 | 辅助 | 风格 |
|------|------|------|------|------|------|
| 极简白 | `#fff` | `#333` | `#2563eb` | `#666` | 清爽干净，蓝色强调 |
| 暖纸墨 | `#fdfaf4` | `#4a3728` | `#b8532a` | `#8b7355` | 杂志阅读感，细横线分隔 |
| 暗夜模式 | `#1a1a2e` | `#d0d0d0` | `#00d4aa` | `#888` | 科技感，青色强调 |

**微信公众号兼容性规则**：

- 仅用 7 个标签：`<section>` / `<p>` / `<span>` / `<strong>` / `<em>` / `<img>` / `<br>`
- 禁用 `<div>` / `<h1~h6>` / `<style>`
- 所有 CSS 内联，无渐变/阴影/变形
- 正文默认参数：字号 14px / 行高 1.85 / 颜色 #333

**预览页面**：暗色主题双栏设计。左栏 HTML 源码编辑，右栏 iPhone 模拟器渲染。支持宽度切换（375/390/414）、拖拽 .html 加载、一键复制（ClipboardItem API + execCommand fallback）。

---

### ⑦ wechatpost-push — 推送到公众号草稿箱

**触发词**：`推送` / `push` / `推到公众号` / `推送到公众号`

4 Phase 流程：

| Phase | 内容 |
|-------|------|
| Phase 0 | 检查微信凭证（`.env` 中 `WECHAT_APPID` + `WECHAT_APPSECRET`） |
| Phase 1 | 确认推送（标题/作者/封面预览） |
| Phase 2 | 执行推送：换 access_token → 上传封面素材 → 创建草稿 |
| Phase 3 | 回写飞书（草稿 media_id 写入备注） |
| Phase 4 | 自检 |

**要求**：
- 使用 `cover-combined.png` 作为封面图（2.35:1 + 1:1 并排拼接图）
- 元数据（标题/作者/摘要）从 `final.md` 的 YAML frontmatter 读取
- 仅入草稿箱，不自动群发
- 推送脚本 `wechat_push.py` 纯标准库实现（urllib + json），零外部依赖

**无凭证时**：自动跳过推送，提示用户手动粘贴 HTML 到公众号后台。

**微信 API 错误码速查**：

| errcode | 含义 | 处理 |
|---------|------|------|
| 40013 | AppID 错误 | 检查 `.env` 中 WECHAT_APPID |
| 40125 | AppSecret 错误 | 检查 `.env` 中 WECHAT_APPSECRET |
| 40164 | IP 未加白名单 | 公众号后台 → 基本配置 → IP 白名单 |

---

### ⑧ wechatpost-publish — 发布登记与清理

**触发词**：`已发布` / `发布登记` / `publish` / `发布链接` / `发出去了`

4 Phase 流程：

| Phase | 内容 |
|-------|------|
| Phase 0 | 确认发布信息（链接 + 时间） |
| Phase 1 | 回写飞书表格（发布链接/时间/状态 → 已发布+已完成） |
| Phase 2 | 删除 beeimg 图床图片（微信已自行托管，本地 PNG 保留） |
| Phase 3 | 确认交付 |
| Phase 4 | 自检（飞书记录 + beeimg 清理） |

---

### 📊 wechatpost-status — 进度看板

**触发词**：`看板` / `状态` / `status` / `进度` / `到哪了` / `今天干什么`

读取飞书表格，按状态分类展示所有文章进度。输出示例：

```
📊 WeChatPost 看板

待处理: 3 篇
处理中: 1 篇
已转录: 2 篇
已写稿: 1 篇
已完成: 12 篇
```

---

## 命令速查 / Command Reference

| 你说 | 做什么 |
|------|--------|
| `初始化` | 首次使用，配置环境和 API |
| `处理视频` | 读飞书 → 下载 → 转录 → 纠错 |
| `写文章` | 逐字稿 → 公众号初稿（含 5 个标题候选） |
| `配图` | shot list → API 生图 → 图床 |
| `做封面` | 三维分析 → 模板/AI 设计 → HTML 预览 → PNG |
| `排版` | Markdown → 公众号兼容 HTML → 手机预览 |
| `推送` | 推送到公众号草稿箱（需微信凭证） |
| `已发布 https://...` | 飞书登记 + 图床清理 |
| `看板` | 查看全流程进度 |
| `一条龙` | 转录 → 写稿 → 配图 → 封面 → 排版 → 推送 → 登记（全自动） |

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
    ├── output.html            ← 排版 HTML（公众号粘贴用）
    ├── output-preview.html    ← 手机预览 + 一键复制
    ├── illustrations/
    │   ├── shot-list.md       ← 配图分镜计划
    │   ├── uploaded-keys.json ← 图床上传记录
    │   └── 01-{主题}.png      ← 本地 PNG（中间产物）
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
| `BEEIMG_TOKEN` | 配图上传图床（beeimg） | https://www.beeimg.cn 后台获取 |
| `WECHAT_APPID` | 公众号草稿箱推送（可选） | 公众号后台 → 设置与开发 → 基本配置 |
| `WECHAT_APPSECRET` | 同上 | 同上 |
| 飞书多维表格 | 任务队列与状态追踪 | 项目内置 Base Token |

### `.env` 文件模板 / .env Template

```env
# ── 生图 API（云雾）──
YUNWU_API_KEY=sk-your-api-key-here
YUNWU_BASE_URL=https://yunwu.ai/

# ── 图床 API（beeimg）──
BEEIMG_TOKEN=your-bearer-token-here
BEEIMG_BASE_URL=https://www.beeimg.cn

# ── 配图开关 ──
ILLUSTRATE_ENABLED=false

# ── 微信公众号 API（可选）──
WECHAT_APPID=wx1234567890
WECHAT_APPSECRET=your-appsecret-here
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

### 排版：公众号优先

严格遵守微信公众号兼容性规则，只用 7 个标签，CSS 全部内联。

### 自检文化

每个子 Skill 完成后必须**重新读取产出文件**，逐项验证，不依赖记忆。失败 → 重写 → re-read → 仍不通过 → 输出 `❌ 自检失败`。

---

## 常见问题 / FAQ

| 问题 | 解决 |
|------|------|
| ffmpeg 找不到 | 传 `--ffmpeg` 绝对路径给 transcribe.py |
| 抖音下载 403 | 直链过期，重新解析即可 |
| 转录质量差 | 正常现象，LLM 纠错会自动修复 |
| 配图跳过 | `.env` 中 `ILLUSTRATE_ENABLED=false`，改为 `true` |
| lark-cli 过期 | `lark-cli auth login --recommend` |
| 封面截图失败 | `cd cover-templates && npm install` 安装 puppeteer + canvas |
| 推送失败 | 检查 `WECHAT_APPID`/`WECHAT_APPSECRET` 配置 + IP 白名单 |
| 推送报错 40164 | 公众号后台 → 基本配置 → 将本机出口 IP 加入白名单 |
| 不知道到哪了 | 说「看板」 |
| 想一键到底 | 说「一条龙」 |

---

## License

MIT
