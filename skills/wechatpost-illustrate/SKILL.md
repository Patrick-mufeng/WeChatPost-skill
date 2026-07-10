---
name: wechatpost-illustrate
description: "Generate inline illustrations for WeChat public account articles via API (Mitu/云雾). Use when the user says 配图, 插图, 做插图, illustrate, or 正文配图. Analyzes final.md, creates a shot list, generates images via gpt-image-2 as local PNGs. Images are uploaded to WeChat CDN automatically during the push phase."
---

# wechatpost-illustrate — 正文配图

> API 生图：shot list → 觅图客户端 → 云雾 API → gpt-image-2 → 本地 PNG（推送时自动上传微信 CDN）。

## 资源位置

- 脚本：本 skill 目录下 `scripts/`（`mitu_client.py`, `mitu_generate.py`）
- 参考文件：`references/`（`style-dna.md`, `xiaoni-ip.md`, `prompt-template.md`, `qa-checklist.md`, `composition-patterns.md`）
- API 配置：项目根目录 `.env`（`YUNWU_API_KEY`）

## 前置依赖

Python 3.9+ + `httpx` + API 配置。

### 首次使用引导

配图功能需要两组 API：

**① 生图 API（云雾）**：
1. 注册：https://yunwu.ai/register?aff=zM1f
2. 获取 API Key → 在项目根目录 `.env` 中填入：
```env
YUNWU_API_KEY=sk-你的Key
YUNWU_BASE_URL=https://yunwu.ai/
```

---

## Workflow

```
用户: "配图"
  ↓
Phase 0: API Key 检查
  ↓
Phase 1: 读 final.md → 分析文章
  ↓
Phase 2: 出配图策略（shot list，4-8 张）
  ↓
Phase 3: 用户确认策略
  ↓
Phase 4: 逐张生成 PNG（本地保存）
  ↓
Phase 5: 写入终稿（在 final.md 插入本地图片路径）
  ↓
Phase 6: 交付汇总
  ↓
Phase 7: 自检
```

---

## Phase 0 · 配图开关 + API Key 检查

首先检查 `.env` 中 `ILLUSTRATE_ENABLED` 的值。若为 `false` → 输出提示并优雅退出：

```
⏭️ 配图已跳过（ILLUSTRATE_ENABLED=false）

在初始化时选择了跳过配图。如需开启，修改 .env 中 ILLUSTRATE_ENABLED=true 后重新说"配图"。
```

若未设置或为 `true`，继续检查 `YUNWU_API_KEY`。未配置 → 显示注册引导 → 用户填好后重新说"配图"。

---

## Phase 1 · 读取文章

从 `outputs/{标题}_{日期}/article/final.md` 读取正文（跳过 frontmatter）。

提炼：核心观点、认知转折点、适合用图解释的内容。

### 配色分析

根据文章情绪基调选择色板（参考 `references/style-dna.md` 颜色章节）：

| 文章情绪 | 色板 |
|----------|------|
| 数据多、逻辑链、技术术语 | **冷峻** · 蓝灰调 |
| 个人故事、情感表达、生活场景 | **温暖** · 暖调 |
| 观点鲜明、号召行动、对比冲突 | **激昂** · 对比调 |
| 幽默、自嘲、年轻化语言 | **轻松** · 明亮调 |
| 权威引用、深度分析、正式语气 | **严肃** · 大地调 |

在 shot list 开头标注选定的色板名称，供后续 prompt 构建使用。

---

## Phase 2 · 配图策略（shot list）

输出 4-8 张配图计划。参考 `references/style-dna.md` 和 `references/xiaoni-ip.md`：

```
## 配图策略

配色：{色板名称}（如 冷峻·蓝灰调）

| # | 位置 | 主题 | 结构类型 | 小霓动作 |
|---|------|------|----------|----------|
| 1 | 第X段后 | xxx | 概念隐喻 | xxx |
| 2 | ... | ... | ... | ... |

### 图 1：{主题}
- 核心意思：...
- 结构类型：概念隐喻
- 小霓动作：...
- 建议元素：...
- 中文标注词：...
```

---

## Phase 3 · 用户确认

展示 shot list。用户可增删改、"直接生成"。确认后保存到 `illustrations/shot-list.md`。

---

## Phase 4 · 逐张生成（本地保存）

> ⚠️ **硬性约束：必须一张一张生成，禁止并行/同时调用生图 API。**
> 
> API 并发压力 + rate limit 风险 = 不允许同时发起多个生图请求。必须等当前这张图完全生成并保存到本地后，再开始下一张。
> 
> 违规行为：把多张图的 `mitu_generate.py` 命令一次性发出、用 `&` 或并行 tool calls 同时调用。
> 
> 正确做法：`python scripts/mitu_generate.py ...` → 等待完成 → 确认 PNG 文件存在 → 再发下一张的命令。
> 
> **即使 shot list 有 4-8 张图，也必须串行，一张一张来。**

### 4.1 构建 prompt

每张图按 `references/prompt-template.md` 构建英文 prompt。必须包含：
- 16:9 horizontal Chinese article illustration
- Pure white background, black hand-drawn line art with flat color fills（填色本风格平涂）
- 小霓 IP（固定配色：头发 #2c3e6b、皮肤 #f5efe6、工装 #8a9b8e、护目镜 #b0b0b0）
- 其余元素按 Phase 1 选定的情绪色板平涂上色
- 大量留白（≥35%）

### 4.2 调用生图 API（串行，一张一张来）

```bash
# ⚠️ 一条一条执行，上一张确认保存后再发下一条
python scripts/mitu_generate.py "<英文prompt>" \
  -r 16:9 --mp 1 \
  -o "outputs/{标题}_{日期}/article/illustrations/" \
  --output-name "{序号}-{主题}.png"
```

**每张图的完整流程**：发 API → 等待返回 → 确认 PNG 文件 > 5000 字节 → 再开始下一张。

失败→指数退避重试（3s→9s→27s），最多 2 次。当前这张重试耗尽仍失败 → 标记为失败 → 继续下一张（不要卡住整个流程）。

> 图片仅保存到本地。推送阶段 `wechat_push.py` 会自动通过微信 `/cgi-bin/media/uploadimg` API 上传图片并替换 HTML 中的本地路径为微信 CDN URL。

---

## Phase 5 · 写入终稿

在 final.md 对应位置插入本地图片路径：

```markdown
![{主题}](illustrations/{序号}-{主题}.png)
```

> 排版和推送阶段会自动处理：排版时保留相对路径，推送时 `wechat_push.py` 自动上传到微信 CDN 并替换 URL。

---

## Phase 6 · 交付汇总

```
✅ 配图完成

| # | 文件 | 位置 | 状态 |
|---|------|------|------|
| 1 | 01-xxx.png | 第X段后 | ✅ |
| 2 | 02-xxx.png | 第X段后 | ⚠️ 生成失败 |

保存路径：outputs/{标题}_{日期}/article/illustrations/
下一步："做封面"（图片将在推送时自动上传微信 CDN）
```

---

## Phase 7 · 自检 — 逐项重读验证

| # | 目标 | 读什么 | 通过条件 |
|---|------|--------|----------|
| 1 | shot-list | `illustrations/shot-list.md` | 文件存在，含完整表格 |
| 2 | PNG 文件 | `illustrations/01-*.png` 等 | 每张图存在，字节 > 5000 |
| 3 | final.md | `article/final.md` | 已插入图片引用 |

```
📋 自检 Phase 7:
  □ shot-list.md → ✅
  □ 01-xxx.png → {N} KB ✅
  □ final.md 图片引用 → ✅

✅ 配图自检全部通过
```

失败：缺失 → 重写 → re-read → 仍不通过 → ❌
