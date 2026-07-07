---
name: wechatpost-format
description: "Format Markdown articles to WeChat-compatible HTML. Use when the user says 排版, format, 转HTML, 转公众号, or 公众号排版. Converts final.md to clean HTML following WeChat's strict compatibility rules (section/p/span, no div/h1-h6)."
---

# wechatpost-format — Markdown → 公众号 HTML

> 将 Markdown 终稿转为微信公众号兼容 HTML。零外部依赖，AI 直接生成。

## 微信公众号兼容性规则（强制）

公众号编辑器只识别有限标签。违反以下规则会被过滤或样式丢失：

### 标签白名单

| 标签 | 用途 | 说明 |
|------|------|------|
| `<section>` | 唯一块级容器 | ✅ 允许，禁用 `<div>` |
| `<p>` | 段落 | ✅ 允许，**margin 必须清零**：`margin:0px` |
| `<span>` | 行内样式 | ✅ 允许 |
| `<strong>` | 加粗 | ✅ 允许 |
| `<em>` | 斜体 | ✅ 允许 |
| `<br>` | 换行 | ✅ 允许 |
| `<img>` | 图片 | ✅ 允许 |
| `<h1~h6>` | 标题 | ❌ **禁用**——用 `<p>` + 字号模拟 |
| `<div>` | 容器 | ❌ **禁用**——用 `<section>` |
| `<style>` | 样式 | ❌ **禁用**——全部内联 |

### CSS 安全/风险清单

| 属性 | 状态 |
|------|------|
| `color`, `font-size`, `font-weight`, `line-height`, `letter-spacing` | ✅ 安全 |
| `text-align`, `margin`, `padding`, `border`, `border-radius` | ✅ 安全 |
| `background-color` (纯色) | ✅ 安全 |
| `width`, `max-width`, `height` | ✅ 安全 |
| `box-shadow` | ⚠️ 有风险，接受丢失 |
| `background: linear-gradient(...)` | ❌ 最易被过滤 |
| `background-image: url(...)` | ❌ 外部图片不加载 |
| `transform`, `opacity` | ❌ 大概率丢失 |
| `gap` (flex) | ⚠️ 用 margin 替代 |
| `!important` | ❌ 粘贴时剥离 |

### 正文排版默认参数

```
字号：14px
行高：1.85
颜色：#333（正文）/ #555（辅助）/ #888（最淡）
段落间距：8px（p 的 margin-bottom）
两端缩进：0
```

---

## Workflow

```
用户: "排版"
  ↓
Phase 0: 读 final.md + 检查前置
  ↓
Phase 1: 选择排版主题
  ↓
Phase 2: 生成 output.html
  ↓
Phase 3: 生成 output-preview.html
  ↓
Phase 4: 自检 + 交付
```

---

## Phase 0 · 读取 + 前置检查

1. 读 `outputs/{标题}_{日期}/article/final.md`
2. 提取 frontmatter（title/summary）
3. 跳过「标题候选」「简介」段，取最后一个 `---` 之后的正文
4. 检查封面是否做了 → 没做提示先"做封面"
5. 检查配图是否做了 → 没做可选跳过

---

## Phase 1 · 选择主题

```
🎨 选择排版风格：

1. 极简白 — 纯白底+黑色字+蓝色强调，清爽干净
2. 暖纸墨 — 暖灰底+深棕字+细横线分隔，杂志阅读感
3. 暗夜模式 — 深黑底+浅灰字+青色强调，科技感
4. 自定义 — 你来描述想要的排版感觉

选哪个？
```

按用户选择，确定：
- 背景色 / 正文色 / 强调色 / 辅助色
- 标题字号 / 加粗方式
- 分隔线样式
- 引用块样式

---

## Phase 2 · 生成 output.html

### 格式转换规则

| Markdown | HTML |
|----------|------|
| `# 标题` | `<p style="font-size:22px;font-weight:bold;margin:24px 0 12px;color:{强调色}">` |
| `## 标题` | `<p style="font-size:18px;font-weight:bold;margin:20px 0 10px;color:{强调色}">` |
| `**加粗**` | `<strong>加粗</strong>` |
| `*斜体*` | `<em>斜体</em>` |
| `- 列表` | `<p style="margin:4px 0 4px 16px">· 列表项</p>` |
| `> 引用` | `<section style="border-left:3px solid {强调色};padding:8px 12px;margin:12px 0;background:{浅色背景}"><p style="margin:0;color:{辅助色}">` |
| `![alt](path)` | `<img src="{path}" alt="{alt}" style="max-width:100%;border-radius:4px;margin:16px 0">` |
| `---` | `<section style="text-align:center;margin:24px 0"><span style="color:{浅色};letter-spacing:8px">···</span></section>` |
| 空行 | `<p style="margin:0">&nbsp;</p>` |

### 输出文件结构

```html
<section style="max-width:677px;margin:0 auto;padding:0;font-family:-apple-system,BlinkMacSystemFont,PingFang SC,Microsoft YaHei,sans-serif;font-size:14px;line-height:1.85;color:{正文色};background:{背景色}">

  <!-- 正文内容 -->

</section>
```

### 路径规则

- 封面图片引用：`../cover/cover-2x35.png`（相对于 article/ 目录）
- 配图引用：`illustrations/01-xxx.png`（图床 URL，由 illustrate 阶段写入 final.md）
- 保存到：`outputs/{标题}_{日期}/article/output.html`

### 配图处理

配图由 `wechatpost-illustrate` 阶段上传到 beeimg 图床，URL 已写入 final.md。排版时直接用图床 URL：

```html
<img src="https://www.beeimg.cn/xxxx/xxx.png" alt="{主题}" style="max-width:100%;border-radius:4px;margin:16px 0">
```


---

## Phase 3 · 生成 output-preview.html

生成手机预览版：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>预览 - {标题}</title>
<style>
  body { background:#f0f0f0; display:flex; justify-content:center; padding:20px; }
  .phone-frame { width:375px; min-height:667px; background:white; border-radius:20px; padding:20px 16px; box-shadow:0 0 30px rgba(0,0,0,0.15); }
  .copy-btn { position:fixed; top:10px; right:10px; background:#07c160; color:white; border:none; padding:10px 20px; border-radius:20px; cursor:pointer; z-index:100; font-size:14px; }
</style>
</head>
<body>
<button class="copy-btn" onclick="navigator.clipboard.writeText(document.getElementById('content').innerHTML);this.textContent='已复制!'">📋 复制到公众号</button>
<div class="phone-frame">
  <div id="content">
    <!-- output.html 的完整内容 -->
  </div>
</div>
</body>
</html>
```

保存到：`outputs/{标题}_{日期}/article/output-preview.html`

---

## Phase 4 · 自检 + 交付

重读 output.html 验证：

- [ ] 文件存在，字节 > 1000
- [ ] 无 `<div>`、`<h1~h6>`、`<style>` 标签
- [ ] 所有样式内联
- [ ] `![alt](path)` 已转为 `<img>` 标签，引用图床 URL
- [ ] 封面图路径正确

```
✅ 排版完成：outputs/{标题}_{日期}/article/
  ├── output.html          ← 公众号粘贴用
  └── output-preview.html  ← 手机预览 + 一键复制

下一步：打开 -preview.html 预览 → 复制 HTML → 粘贴公众号后台
```

---

## Key Rules

1. **只用 `<section>/<p>/<span>/<strong>/<em>/<img>/<br>`**——其余标签禁用
2. **所有 CSS 内联**——无 `<style>` 标签
3. **不做渐变/阴影/变形**——会被过滤
4. **margin 清零**——所有 `<p>` 设 `margin:0`，段落间用 `margin-bottom:8px`
5. **配图用图床 URL**——`<img>` 引用 beeimg 公开链接
6. **字号 14px 起**——公众号最小可读字号
