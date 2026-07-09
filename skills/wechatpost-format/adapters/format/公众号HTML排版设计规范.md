<!--
============================================================================
微信公众号 HTML 排版设计规范 (DESIGN.md)
Version: 1.1
基于 4 篇真实公众号文章源码逆向分析 + 实际粘贴兼容性验证
适用：AI Agent 生成公众号兼容 HTML
============================================================================
-->

# 微信公众号 HTML 排版设计规范

## 概述

本规范定义了微信公众号文章 HTML 的完整语法规则。基于对 135 编辑器、秀米编辑器产出的真实公众号文章源码的逆向分析，以及实际粘贴到公众号后台的兼容性验证，确保 AI 按照此规范生成的 HTML 能够完整保留样式。

---

## 兼容性风险说明

### 风险等级

| 等级 | 含义 |
|------|------|
| ✅ **安全** | 在公众号编辑器中经过验证，可完整保留 |
| ⚠️ **有风险** | 部分场景下可能被公众号编辑器过滤，建议备选方案 |
| ❌ **不兼容** | 公众号编辑器不识别，会被直接丢弃 |

### ⚠️ 高风险属性（易被公众号编辑器过滤）

```diff
- background: linear-gradient(...)   ← 渐变色最容易被丢弃
- box-shadow                          ← 阴影经常丢失
- text-shadow                         ← 文字阴影可能丢失
- opacity                             ← 透明度可能丢失
- transform: rotate/skew/translate    ← 变形几乎都会被丢弃
- gap (flex 容器上的间距)              ← 部分 X5 内核不支持
- <svg> 和 <foreignObject>            ← SVG 经常被编辑器过滤
- background-image: url(...)          ← 外部图片链接不加载
- !important                          ← 粘贴时可能被剥离
```

### 安全替代原则

```
高风险写法                → 安全替代
──────────────────────────────────────────
background: linear-gradient(...) → background-color: 纯色
gap: 20px                 → 子元素 margin: 0 10px
box-shadow                → border + 层级叠加（效果弱化需接受）
transform                 → 不使用变形，用结构实现
opacity                   → 用颜色 alpha 通道替代
<svg>                     → 纯 HTML + emoji 替代
```

---

## 第一部分：HTML 标签规则

### 1.1 唯一允许的容器标签：`<section>`

```
✅ <section style="...">内容</section>
❌ <div>        — 公众号不识别
❌ <article>    — 公众号不识别
❌ <header>     — 公众号不识别
❌ <footer>     — 公众号不识别
❌ <nav>        — 公众号不识别
❌ <main>       — 公众号不识别
❌ <aside>      — 公众号不识别
```

**规则**：所有块级布局必须使用 `<section>`。嵌套深度无限制（源码中常见 10+ 层嵌套）。

### 1.2 行内标签

| 标签 | 用途 | 示例 |
|------|------|------|
| `<p>` | 段落（margin 必须清零） | `<p style="margin:0px">` |
| `<span>` | 行内文字样式 | `<span style="color:#xxx">` |
| `<strong>` | 加粗 | `<strong>文字</strong>` |
| `<em>` | 斜体 | `<em>文字</em>` |
| `<br>` | 换行 | `<br>`（不要用自闭合 `<br/>`，某些编辑器不兼容） |

### 1.3 媒体标签

| 标签 | 用途 | 兼容性 |
|------|------|--------|
| `<img>` | 图片（必须带 draggable="false"） | ✅ |
| ❌ `<svg>` | SVG 装饰 / 绝对定位容器 | ⚠️ 编辑器经常过滤，不建议使用 |
| ❌ `<foreignObject>` | SVG 内嵌 HTML | ❌ 不兼容 |

### 1.4 禁止使用的标签

```
❌ <div>        — 用 <section> 替代
❌ <table>      — 用 flex 替代
❌ <ul> <ol>    — 用 <section> + <p> 替代
❌ <h1>~<h6>    — 用 <section> + font-size 替代
❌ <blockquote> — 用 <section> + border-left 替代
❌ <a>          — 公众号不支持外链
❌ <style>      — 必须 100% 内联样式
❌ <link>       — 禁止外部 CSS
❌ <svg>        — 公众号编辑器会过滤，用 emoji 替代
```

---


## 正文排版规则

### 正文段落默认样式

正文段落必须遵循以下默认值：

| 属性 | 值 | 说明 |
|------|-----|------|
| `font-size` | `14px` | 正文字号基准，不得小于 12px |
| `line-height` | `1.85` | 正文行高 |
| `letter-spacing` | `0.3px` | 正文间距 |
| `color` | `#333` ~ `#555` | 正文色 |
| `padding` | `0 8px` | **两端间距 8px**，左右内边距统一 |
| `margin` | `0` | `<p>` 标签 margin 归零 |
| `box-sizing` | `border-box` | 强制 |
| `max-width` | `100% !important` | 强制 |

> 两端间距 8px 适用于正文容器的左右 padding。如果使用外层 `<section>` 包裹正文，则在外层设置 `padding: 0 8px`。

---
## 第二部分：强制 CSS 规则

### 2.1 每个元素必须携带的三个属性

```css
box-sizing: border-box;
max-width: 100% !important;
```

**无例外**。这是公众号渲染引擎的硬性要求。

> ⚠️ `!important` 在粘贴过程中可能被编辑器剥离。如果发现样式丢失，检查粘贴后的 HTML 源码中 `!important` 是否还在。如已丢失，需要在公众号后台手动补回。

### 2.2 `<p>` 标签强制初始化

```css
p {
    margin: 0px;
    padding: 0px;
    box-sizing: border-box;
}
```

### 2.3 所有 CSS 必须内联

```
✅ <section style="display:flex;padding:10px;...">
❌ <style>.class { ... }</style>
❌ <section class="xxx">
```

---

## 第三部分：CSS 属性兼容性白名单

以下属性经过公众号编辑器实际粘贴验证。

### 风险标记说明

| 符号 | 含义 |
|------|------|
| ✅ | 安全，可放心使用 |
| ⚠️ | 有风险，确认效果后再用 |
| ❌ | 不兼容，建议避开 |

### 3.1 布局

| 兼容性 | 属性 | 常用值 | 说明 |
|--------|------|--------|------|
| ✅ | `display` | `flex`, `inline-block`, `block` | flex 是主力 |
| ✅ | `flex-flow` | `row`, `column`, `row nowrap` | |
| ✅ | `flex` | `0 0 auto`, `0 0 90%` | 避免复杂小数比例 |
| ✅ | `flex-shrink` | `0` | |
| ✅ | `justify-content` | `center`, `flex-start`, `space-between` | |
| ✅ | `align-items` | `center`, `flex-start` | |
| ⚠️ | `gap` | 任意值 | ⚠️ 部分 X5 内核不支持 flex gap。**安全替代**：改用子元素 `margin` |
| ❌ | `grid` | 任意值 | ❌ 公众号不识别 CSS Grid |
| ❌ | `grid-template-*` | 任意值 | ❌ |

### 3.2 盒模型

| 兼容性 | 属性 | 说明 |
|--------|------|------|
| ✅ | `width` | 百分比或 px |
| ✅ | `height` | 百分比、px、`auto` |
| ✅ | `max-width` | **必须** `100% !important` |
| ✅ | `min-width` | 百分比，常用 |
| ✅ | `min-height` | 百分比或 px |
| ✅ | `padding` | 四向或分向 |
| ✅ | `margin` | 支持负值 |
| ✅ | `box-sizing` | **强制** `border-box` |

### 3.3 文字

| 兼容性 | 属性 | 取值范围 | 说明 |
|--------|------|---------|------|
| ✅ | `font-size` | `3px` ~ `51px` | 正文以 14px 为基准 |
| ✅ | `line-height` | `1` ~ `3` | 正文建议 1.85。**避免 `line-height:0`**，可能导致文字重叠 |
| ✅ | `letter-spacing` | `0px` ~ `5px` | |
| ✅ | `text-align` | `center`, `justify`, `left` | |
| ✅ | `color` | hex / rgb | ✅ 推荐使用 hex（如 `#333`），`rgba()` 部分情况会被转换 |
| ✅ | `font-weight` | `bold`, `600`, `700` | |
| ✅ | `vertical-align` | `middle`, `top` | 消除行内间隙 |
| ⚠️ | `text-shadow` | 任意值 | ⚠️ 公众号编辑器可能过滤，仅在简单场景有效 |
| ❌ | `opacity` | 任意值 | ❌ 经常被丢弃。**替代**：用 `rgba(0,0,0,0.x)` 替代 |
| ✅ | `font-family` | 系统字体栈 | 建议：`-apple-system,'PingFang SC','Microsoft YaHei',sans-serif` |

### 3.4 背景

| 兼容性 | 属性 | 说明 |
|--------|------|------|
| ✅ | `background-color` | **推荐！** 这是最安全的背景方式 |
| ⚠️ | `background` | 简写属性。如果内容包含 `linear-gradient` 则被过滤的风险很高 |
| ❌ | `background: linear-gradient(...)` | ❌ **最常见的不兼容原因**。粘贴到公众号后台后渐变色几乎都会被丢弃。**替代**：使用纯色 `background-color` |
| ❌ | `background-image` | ❌ 外部图片 URL 不加载 |

### 3.5 边框

| 兼容性 | 属性 | 说明 |
|--------|------|------|
| ✅ | `border` | `1px solid #xxx` |
| ✅ | `border-left/right/top/bottom` | 单侧边框 |
| ✅ | `border-radius` | 圆角支持良好 |
| ⚠️ | `box-shadow` | ⚠️ 阴影可能丢失，**替代**：用 `border` 叠加模拟 |

### 3.6 特效

| 兼容性 | 属性 | 说明 |
|--------|------|------|
| ⚠️ | `text-shadow` | ⚠️ 文字阴影可能被过滤 |
| ❌ | `transform` | ❌ `rotate/skew/translate` 均不兼容 |
| ❌ | `opacity` | ❌ 不兼容。**替代**：用 `rgba(#xxx, alpha)` |
| ✅ | `z-index` | `1` ~ `7` 支持 |

---

## 第四部分：安全布局模式

### 4.1 Flex 行布局（推荐）

```html
<!-- ✅ 安全：外层 display:flex，子元素用 margin 替代 gap -->
<section style="display:flex;flex-flow:row;justify-content:center;box-sizing:border-box;max-width:100%!important">
  <section style="margin:0 5px;box-sizing:border-box;max-width:100%!important">元素1</section>
  <section style="margin:0 5px;box-sizing:border-box;max-width:100%!important">元素2</section>
</section>
```

### 4.2 Flex 列布局

```html
<section style="display:flex;flex-flow:column;align-items:center;box-sizing:border-box;max-width:100%!important">
  <section style="margin:6px 0;box-sizing:border-box;max-width:100%!important">上</section>
  <section style="margin:6px 0;box-sizing:border-box;max-width:100%!important">下</section>
</section>
```

### 4.3 图片容器

```html
<section style="text-align:center;margin:12px 0;box-sizing:border-box;max-width:100%!important">
  <img src="https://..." draggable="false" style="width:100%;border-radius:8px;box-sizing:border-box;max-width:100%!important;vertical-align:middle">
</section>
```

---

## 第五部分：颜色系统

### 5.1 安全取色方式

```
✅ background-color: #f5f5f5         ← hex，最安全
✅ background-color: rgb(245,245,245) ← rgb，安全
⚠️ background-color: rgba(0,0,0,0.05) ← rgba，部分场景兼容
❌ background: linear-gradient(...)   ← 渐变色，不兼容
```

### 5.2 颜色层级规范

| 层级 | 用途 | 色值范围 |
|------|------|---------|
| 主色 | 标题、强调 | 饱和色，如 `#c44`, `#2d6db5` |
| 辅色 | 背景、标签 | 浅色，如 `#f0f4ff`, `#faf8f5` |
| 正文色 | 正文文字 | `#333` ~ `#555` |
| 弱色 | 辅助文字、注释 | `#999` ~ `#bbb` |

---

## 第六部分：排版组件

### 6.1 标题行

```html
<section style="display:flex;flex-flow:row;align-items:center;justify-content:center;margin:18px 0 14px;box-sizing:border-box;max-width:100%!important">
  <section style="width:100%;height:1px;background-color:#ddd;box-sizing:border-box;max-width:100%!important"></section>
  <section style="font-size:15px;font-weight:bold;color:#333;white-space:nowrap;margin:0 14px;box-sizing:border-box;max-width:100%!important">标题文字</section>
  <section style="width:100%;height:1px;background-color:#ddd;box-sizing:border-box;max-width:100%!important"></section>
</section>
```

### 6.2 标题栏（带装饰线）

```html
<section style="display:flex;flex-flow:row;align-items:center;margin:12px 0 8px;box-sizing:border-box;max-width:100%!important">
  <section style="width:4px;height:18px;background-color:主色;border-radius:2px;flex-shrink:0;box-sizing:border-box;max-width:100%!important"></section>
  <section style="font-size:17px;font-weight:bold;color:#333;margin:0 0 0 10px;box-sizing:border-box;max-width:100%!important">标题</section>
</section>
```

### 6.3 引用块

```html
<section style="margin:14px 0;padding:14px 16px;background-color:#f7f8fa;border-left:4px solid 主色;border-radius:4px;box-sizing:border-box;max-width:100%!important">
  <p style="font-size:14px;color:#555;line-height:1.8;margin:0;box-sizing:border-box">引用文字内容</p>
</section>
```

### 6.4 图文卡片

```html
<section style="margin:16px 0;padding:18px 16px;background-color:#faf8f5;border-radius:8px;box-sizing:border-box;max-width:100%!important">
  <p style="font-size:15px;font-weight:bold;color:#333;margin:0 0 6px;box-sizing:border-box">小标题</p>
  <p style="font-size:14px;color:#555;line-height:1.85;margin:0;box-sizing:border-box">正文内容...</p>
</section>
```

### 6.5 分割线

```html
<section style="margin:20px 0;text-align:center;box-sizing:border-box;max-width:100%!important">
  <section style="display:inline-block;width:60px;height:1px;background-color:#ddd;box-sizing:border-box;max-width:100%!important"></section>
</section>
```

或者带装饰：
```html
<section style="margin:20px 0;text-align:center;box-sizing:border-box;max-width:100%!important">
  <span style="font-size:12px;color:#ccc;letter-spacing:8px">• • •</span>
</section>
```

---

## 第七部分：头尾卡片（Header / Footer Cards）

### 7.1 头部卡片 — 纯色背景（✅ 安全）

```html
<section style="width:100%;padding:30px 20px;text-align:center;background-color:#f7f2ea;box-sizing:border-box;max-width:100%!important">
  <p style="font-size:22px;font-weight:bold;color:#333;margin:0 0 8px;letter-spacing:2px;box-sizing:border-box">标题</p>
  <p style="font-size:12px;color:#999;margin:0;letter-spacing:1px;box-sizing:border-box">副标题或摘要</p>
</section>
```

> ❌ **避免**使用 `background: linear-gradient(...)`，公众号编辑器会丢弃渐变色。
> ✅ **安全替代**：使用纯色 `background-color` + 文字颜色层次来营造设计感。

### 7.2 头部卡片 — 带左右装饰

```html
<section style="display:flex;flex-flow:row;align-items:center;justify-content:center;padding:24px 16px;background-color:#faf8f5;box-sizing:border-box;max-width:100%!important">
  <section style="width:24px;height:2px;background-color:主色;box-sizing:border-box;max-width:100%!important"></section>
  <section style="margin:0 14px;text-align:center;box-sizing:border-box;max-width:100%!important">
    <p style="font-size:20px;font-weight:bold;color:#333;margin:0 0 4px;box-sizing:border-box">标题</p>
    <p style="font-size:11px;color:#999;margin:0;box-sizing:border-box">副标题</p>
  </section>
  <section style="width:24px;height:2px;background-color:主色;box-sizing:border-box;max-width:100%!important"></section>
</section>
```

### 7.3 尾部卡片

```html
<section style="margin:28px 0 20px;padding:20px 16px;text-align:center;background-color:#faf8f5;border-radius:8px;box-sizing:border-box;max-width:100%!important">
  <p style="font-size:14px;font-weight:bold;color:#333;margin:0 0 4px;box-sizing:border-box">如果觉得有收获</p>
  <p style="font-size:12px;color:#999;margin:0 0 14px;box-sizing:border-box">点赞 · 在看 · 转发，让更多人看到</p>
  <section style="display:flex;flex-flow:row;justify-content:center;box-sizing:border-box;max-width:100%!important">
    <section style="padding:8px 16px;margin:0 4px;background-color:主色;color:#fff;font-size:12px;font-weight:600;border-radius:6px;box-sizing:border-box;max-width:100%!important">👍 点赞</section>
    <section style="padding:8px 16px;margin:0 4px;background-color:强调色;color:#fff;font-size:12px;font-weight:600;border-radius:6px;box-sizing:border-box;max-width:100%!important">👀 在看</section>
    <section style="padding:8px 16px;margin:0 4px;background-color:金色;color:深色;font-size:12px;font-weight:600;border-radius:6px;box-sizing:border-box;max-width:100%!important">↗ 转发</section>
  </section>
</section>
```

### 7.4 极简尾部

```html
<section style="margin:24px 0 20px;padding:18px 16px;text-align:center;border-top:1px solid #eee;box-sizing:border-box;max-width:100%!important">
  <p style="font-size:11px;color:#bbb;margin:0;letter-spacing:0.5px;box-sizing:border-box">— END —</p>
</section>
```

---

## 第八部分：按钮与交互元素

### 8.1 文字按钮（✅ 安全）

```html
<section style="display:flex;flex-flow:row;justify-content:center;box-sizing:border-box;max-width:100%!important">
  <p style="font-size:12px;color:#999;margin:0 10px;letter-spacing:1px;box-sizing:border-box">👍 点赞</p>
  <p style="font-size:12px;color:#999;margin:0 10px;letter-spacing:1px;box-sizing:border-box">👀 在看</p>
  <p style="font-size:12px;color:#999;margin:0 10px;letter-spacing:1px;box-sizing:border-box">↗ 转发</p>
</section>
```

### 8.2 标签按钮（✅ 安全）

```html
<section style="display:flex;flex-flow:row;justify-content:center;box-sizing:border-box;max-width:100%!important">
  <section style="padding:6px 16px;margin:0 4px;background-color:主色;color:#fff;font-size:11px;font-weight:600;border-radius:20px;box-sizing:border-box;max-width:100%!important">👍 点赞</section>
  <section style="padding:6px 16px;margin:0 4px;background-color:强调色;color:#fff;font-size:11px;font-weight:600;border-radius:20px;box-sizing:border-box;max-width:100%!important">👀 在看</section>
  <section style="padding:6px 16px;margin:0 4px;background-color:#c8882e;color:#fff;font-size:11px;font-weight:600;border-radius:20px;box-sizing:border-box;max-width:100%!important">↗ 转发</section>
</section>
```

---

## 第九部分：公众号粘贴注意事项

### 9.1 粘贴后必检清单

粘贴到公众号后台后，务必检查以下项目：

| # | 检查项 | 如果丢失怎么办 |
|---|--------|--------------|
| 1 | `!important` 是否还在 | 手动在公众号后台补加 |
| 2 | 背景色是否正确 | 检查 `background-color`，渐变丢失是正常的 |
| 3 | 圆角 `border-radius` 是否保留 | 通常没问题 |
| 4 | 图片是否显示 | 公众号图片必须上传到素材库，外部链接不显示 |
| 5 | 间距是否错乱 | `margin` 通常正常，`gap` 可能丢失 |

### 9.2 已知不兼容模式

```
模式                          → 结果
────────────────────────────────────────────
background: linear-gradient   → 渐变色丢失，变成纯色或白色背景
box-shadow                    → 阴影消失
text-shadow                   → 文字阴影消失
transform: rotate/skew        → 变形消失
opacity: 0.5                  → 透明度被忽略
gap: 20px                     → 在某些 X5 版本中丢失
<svg>...</svg>                → SVG 被编辑器过滤
!important                    → 粘贴时被编辑器剥除
font-size: 0                  → 文字消失
line-height: 0                → 文字重叠
```

### 9.3 最佳实践

1. **先试纯色**：设计时优先用 `background-color` + 边框，验证通过后再尝试添加渐变等效果
2. **保留基本结构**：确保去除特效后内容仍然可读
3. **粘贴后用"预览"检查**：在公众号后台发送预览到手机，检查真实效果
4. **不要依赖阴影**：如果设计需要层次感，用 `border` 叠加或颜色深浅来实现

---

## 附录：快速参考卡片

```
┌─ 布局 ─────────────────────────────────────┐
│ display: flex | inline-block | block       │
│ flex-flow: row | column                     │
│ flex: 0 0 auto | 0 0 90%                   │
│ justify-content: center | flex-start        │
│ align-items: center | flex-start            │
│ ⚠️ gap → 改用子元素 margin                  │
│ ❌ grid → 不受支持                          │
├─ 盒模型 ───────────────────────────────────┤
│ box-sizing: border-box  ← 强制              │
│ max-width: 100% !important  ← 强制          │
│ width/height: % | px | max-content         │
│ padding/margin: px | % | auto              │
│ overflow: hidden | visible                 │
├─ 文字 ─────────────────────────────────────┤
│ font-size: 9-51px (基准14px)               │
│ 两端间距 │ 8px (正文容器左右内边距) │
│ line-height: 1.5-2.5 (正文1.85)            │
│ letter-spacing: 0-5px (正文0.3)            │
│ text-align: center | justify | left        │
│ color: #hex (推荐) | rgb()                 │
│ ⚠️ rgba() 可能被转换                       │
├─ 背景 ─────────────────────────────────────┤
│ ✅ background-color: 安全                    │
│ ❌ background: linear-gradient → 不兼容     │
│ ❌ background-image: url → 不加载           │
├─ 边框 ─────────────────────────────────────┤
│ border: 1px solid #xxx                     │
│ border-left/right/top/bottom               │
│ border-radius: px | % | 99px              │
│ ⚠️ box-shadow → 可能丢失                   │
├─ 特效 ─────────────────────────────────────┤
│ ❌ transform → 不兼容                       │
│ ❌ opacity → 不兼容，用 rgba 替代           │
│ ❌ <svg> → 不兼容                          │
│ ✅ z-index: 1-7 支持                       │
└────────────────────────────────────────────┘
```

## 附录 B：设计原则

### 安全 > 花哨
在公众号排版中，**能稳定显示**比"在截图中好看"更重要。优先使用经过验证的安全属性。

### 纯色优先
用 `background-color` + 颜色层次来创造视觉区分，而不是依赖渐变和阴影。

### 粘贴即验证
每次生成排版后，实际粘贴到公众号后台看一下效果。如果某个效果丢失，调整方案。

### 渐进增强
先保证纯色版本完整可读，再尝试添加渐变、阴影等增强效果（知道它们可能丢失）。
