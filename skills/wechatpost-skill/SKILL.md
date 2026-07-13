---
name: wechatpost-skill
description: "Use when processing video links into WeChat public account articles, end to end. Use when the user mentions 视频转公众号, 视频转文章, WeChatPost, or wants to turn video content into published WeChat articles. Covers: video download → transcription → writing → illustration → cover design → formatting."
---

# WeChatPost — 视频转公众号全流程

> 🎯 **一条龙：飞书表格 → 视频转录 → AI写稿 → 配图 → 封面 → 排版 → 推送 → 飞书登记**
>
> 主路由控制全流程，子 skill 独立干活。转录脚本在 `scripts/` 下，写作/配图/封面/排版/推送各路由到 `skills/wechatpost-*/`。

---

## 架构

```
wechatpost-skill/
├── SKILL.md                     ← 你在这里（主路由 + 总协议）
├── scripts/
│   ├── transcribe.py            ← 视频转录脚本
│   └── vendor/parse_video_py/   ← URL 解析器
├── cover-templates/             ← 40套封面模板 + 设计规范
├── shared-references/
│   └── writing-principles.md    ← 写作原则（五种原型 + 四层去AI味）
└── （子 skill 独立部署在 .agents/skills/ 下：
      wechatpost-write / wechatpost-illustrate / wechatpost-cover
      wechatpost-format / wechatpost-push / wechatpost-publish / wechatpost-status）
```

---

## 路由表

| 用户说 | 路由到 | 前置条件 |
|--------|--------|----------|
| "初始化" / "init" / "首次使用" / "开始使用" / "配置" | `wechatpost-init` | 无（这是入口，其他 skill 的前置） |
| "处理视频" / "转录" / "视频转文案" | **主路由自己处理** | 飞书表格有 待处理 记录 |
| "写文章" / "写初稿" / "write" / "出稿" | `wechatpost-write` | `transcript_corrected.txt` 存在 |
| "修改好了" / "改好了" / "定稿" / "保存终稿" | `wechatpost-write`（Phase 8 另存 final.md） | `draft.md` 存在 |
| "配图" / "插图" / "做插图" / "illustrate" / "正文配图" | `wechatpost-illustrate` | `final.md` 存在 |
| "做封面" / "封面" / "cover" / "公众号封面" / "设计封面" | `wechatpost-cover` | 有终稿 |
| "排版" / "format" / "转HTML" / "转公众号" / "公众号排版" | `wechatpost-format` | `final.md` 存在（封面建议先做，非强制） |
| "推送" / "push" / "推到公众号" / "推送到公众号" | `wechatpost-push` | `output.html` + `cover-combined.png` 存在 |
| "已发布" / "发布登记" / "publish" / "发布链接" / "发出去了" | `wechatpost-publish` | 排版完成 |
| "看板" / "状态" / "status" / "进度" / "到哪了" / "今天干什么" | `wechatpost-status` | 任意时刻 |
| "一条龙" / "全部做完" / "全流程" | 主路由串联：转录→写稿→配图→封面→排版→推送→登记 | 飞书表格有待处理记录 |

---

## 用户项目布局

```
WeChatPost-skill/
├── rubric_notes.md                  # 评分标准
├── style_guide.md                   # 个人风格指南
├── outputs/                         # 产出目录
│   └── {标题}_{YYYY-MM-DD}/          # 每篇文章一个文件夹
│       ├── metadata.json            # 视频元信息
│       ├── transcript_raw.txt       # Whisper 原始输出
│       ├── transcript_corrected.txt # LLM 纠错后文案
│       └── article/                 # 🆕 写作产出
│           ├── draft.md             # AI 初稿（含标题候选+简介）
│           ├── final.md             # 终稿（去 AI 味后）
│           ├── output.html          # 排版 HTML（公众号粘贴用）
│           ├── output-preview.html  # 手机预览 + 一键复制
│           ├── illustrations/       # 正文配图
│           │   ├── shot-list.md     # 配图分镜计划
│           │   └── 01-{主题}.png
│           ├── cover/               # 封面
│           │   ├── preview.html     # 双版预览
│           │   ├── cover-2x35.png
│           │   ├── cover-1x1.png
│           │   └── cover-combined.png # 并排预览
└── .agents/skills/                  # Skill 安装目录
```

---

## 自检标准（全局）

每个子 skill 完成操作后，必须执行自检——**重新读取产出文件，逐项验证，不依赖记忆**。

| 子 skill | 自检内容 |
|----------|----------|
| 转录（主路由） | re-read transcript_corrected.txt ≥ 500 字节 + 飞书状态已更新 |
| `wechatpost-write` | re-read draft.md ≥ 500字节 + 含标题候选 + 含正文 |
| `wechatpost-illustrate` | re-read shot-list.md + 每张 PNG 存在 + final.md 有引用 |
| `wechatpost-cover` | re-read preview.html + 双版预览 + CSS 内联 |
| `wechatpost-format` | re-read output.html ≥ 1000字节 + 跑 `validate_gzh_html.py` 确认 0 ERROR / 0 WARNING + `<span leaf="">` 包裹完整 |
| `wechatpost-push` | re-read 推送结果：media_id 非空 + 飞书备注已写入 |
| `wechatpost-publish` | re-read 飞书记录：发布链接/时间/状态 全部写入 |

**失败处理**：缺失 → 立即重写 → re-read 确认 → 仍不通过 → 输出 `❌ 自检失败，请手动检查`。

---

## 飞书表格配置

| Key | Value |
|-----|-------|
| Base Token | `ROfJb313faU478s3oXDcKjbknUc` |
| Table | `视频链接` (`tblKkOBWDtAgarcT`) |

### 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| 标题 | 文本 | 自动提取 |
| 链接 | 文本 | 视频链接（输入） |
| 平台 | 单选 | 自动检测（抖音/B站/小红书/油管/其他平台） |
| 状态 | 单选 | 待处理→处理中→已转录→已写稿→已排版→已完成 |
| 作者 | 文本 | 自动提取 |
| 视频时长 | 文本 | 自动提取 |
| 文案 | 文本 | 纠错后文案 |
| 文案字数 | 数字 | 自动计算 |
| 备注 | 文本 | 错误日志 |
| 发布链接 | 文本 | 公众号文章链接 |
| 发布时间 | 文本 | 发布时间 |
| 发布状态 | 单选 | 未发布/已发布/已登记 |

---

## 主路由工作流

### 处理流程（转录阶段，主路由自己处理）

参见下方「转录工作流」段，与之前一致：读取待处理 → 下载转录 → 纠错 → 更新状态为「已转录」→ 产出到 `outputs/`。

完成后自动提示下一步：

```
✅ 转录完成：outputs/{标题}_{日期}/

下一步：
- "写文章" → 将文案改写成公众号初稿
- "一条龙" → 自动串联写稿→配图→封面→排版→推送→登记
```

---

## 转录工作流

### Prerequisites

```bash
ffmpeg -version                        # MUST be on PATH
python -c "import whisper; print('whisper OK')"
python -c "import httpx; print('httpx OK')"
lark-cli auth status
```

### Step 1: 读取待处理记录

```bash
lark-cli base +record-list \
  --base-token ROfJb313faU478s3oXDcKjbknUc \
  --table-id tblKkOBWDtAgarcT \
  --as user
```

筛选 `状态 == "待处理"`。

### Step 2: 标记处理中

```bash
lark-cli base +record-batch-update \
  --base-token ROfJb313faU478s3oXDcKjbknUc \
  --table-id tblKkOBWDtAgarcT \
  --as user \
  --json '{"record_id_list":["<id>"],"patch":{"状态":"处理中"}}'
```

### Step 3: 下载 + 转录

从 skill 目录运行：

```powershell
python scripts/transcribe.py \
  --url "<video_url>" \
  --model tiny \
  --ffmpeg "<absolute-path-to-ffmpeg>" \
  --output-dir "./outputs" \
  --json
```

自动选择下载路径：
- 抖音/B站/小红书/快手 → parse-video-py（免cookie）
- YouTube/海外 → yt-dlp 兜底

产出 `outputs/{标题}_{日期}/` 含 `metadata.json` + `transcript_raw.txt` + `transcript_corrected.txt`（待填）。

### Step 4: LLM 纠错

用当前模型修正 Whisper 错误：
- 修复同音错字：`等于`→`抖音`, `度么太`→`多模态`
- 修复专有名词、数字冲突
- 合并碎片句子
- **不改写风格**，只修错字

覆盖 `transcript_corrected.txt`。

### Step 5: 更新表格

```bash
lark-cli base +record-batch-update \
  --base-token ROfJb313faU478s3oXDcKjbknUc \
  --table-id tblKkOBWDtAgarcT \
  --as user \
  --json '{"record_id_list":["<id>"],"patch":{"标题":"<title>","作者":"<author>","视频时长":"<duration>","平台":"<platform>","文案":"<corrected>","文案字数":<n>,"状态":"已转录"}}'
```

`平台` 由 transcribe.py 自动从 URL 检测：抖音/B站/小红书/油管/其他平台。无需用户手动填写。

### 双路径架构

| 路径 | 平台 | 方式 | Cookie |
|------|------|------|--------|
| parse-video-py | 抖音/B站/小红书/快手 | httpx直链下载 | 不需要 |
| yt-dlp | YouTube/海外 | yt-dlp下载 | 可选 |

### 常见问题

| 错误 | 解决 |
|------|------|
| `[WinError 2] ffmpeg not found` | ffmpeg 不在 PATH。传 `--ffmpeg` 绝对路径 |
| Douyin 403 | 直链过期，重新跑（解析和下载在同一进程，罕见） |
| yt-dlp cookies needed | 用 `--cookies-from-browser chrome` |

---

## 一条龙全流程

当用户说"一条龙"时，按顺序执行：

```
读取待处理 → 转录 → 写初稿 → 配图 → 封面 → 排版 → 推送 → 发布登记 → 更新状态
```

每个阶段完成后自动进入下一阶段。失败处理分为两类：

- **致命失败**（转录失败/写稿失败）：当前文章标记失败，记录到飞书备注，继续处理队列中的下一篇。
- **非致命失败**（配图失败/封面失败/排版失败）：输出警告，跳过该阶段继续后续流程（如配图失败→跳过配图，继续封面和排版）。失败信息记录到飞书备注。

推送阶段如有凭证问题，提示用户手动操作（打开 output-preview.html → 复制 HTML → 粘贴公众号后台）。

详细流程见各子 skill：
- 写初稿：`skills/wechatpost-write/SKILL.md`
- 配图：`skills/wechatpost-illustrate/SKILL.md`
- 封面：`skills/wechatpost-cover/SKILL.md`
- 排版：`skills/wechatpost-format/SKILL.md`
- 推送：`skills/wechatpost-push/SKILL.md`
- 发布登记：`skills/wechatpost-publish/SKILL.md`
- 看板：`skills/wechatpost-status/SKILL.md`

---

## 状态码

```
待处理 → 处理中 → 已转录 → 已写稿 → 已排版 → 已完成
```

配图/封面阶段不单独对应飞书状态值，统一在排版完成后更新为「已排版」，推送+发布登记完成后更新为「已完成」。

### 断点续跑

如果流程中断（会话结束/网络断开），重新说"一条龙"即可继续。Agent 会自动检测每个阶段的产出文件：

```
outputs/{标题}_{日期}/
  ├── transcript_corrected.txt  → 转录 ✅ → 跳到写稿
  ├── article/final.md          → 写稿 ✅ → 跳到配图
  ├── article/illustrations/    → 配图 ✅ → 跳到封面
  ├── article/cover/            → 封面 ✅ → 跳到排版
  ├── article/output.html       → 排版 ✅ → 跳到推送
  └── （推送/登记检查飞书状态）
```

也可以用单独命令从任意阶段恢复：`写文章` / `配图` / `做封面` / `排版` / `推送` / `已发布`。
