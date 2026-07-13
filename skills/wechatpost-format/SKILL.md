---
name: wechatpost-format
description: "Format Markdown articles to WeChat-compatible HTML. Use when the user says 排版, format, 转HTML, 转公众号, or 公众号排版. Features 6 preset design languages + AI full creative mode. AI reads design language, then creates original layout per article."
---

# wechatpost-format — Markdown → 公众号 HTML

> 将 Markdown 终稿转为微信公众号兼容 HTML。**6 套设计语言 + AI 原创设计**，每篇文章排版独一无二。
>
> 旧模式：AI 读规则 → 按模板转换。新模式：AI 读设计语言 → 理解气质 → 为当前文章原创设计。

## 前置阅读（强制，逐文件依次读取，不可跳过）

> ⚠️ **以下 4 个规范文件是生成合规 HTML 的唯一规则来源。SKILL.md 不再提供行内摘要——你必须完整读取每个文件，读完一个再读下一个。不可并行读取，不可跳读。**

```
按顺序依次读取：

1. references/spec-01-tags.md     — 标签规则与强制 CSS（~110行）
2. references/spec-02-css.md      — CSS 属性完整白名单（~165行）
3. references/spec-03-components.md — 布局模式与组件配方（~410行）
4. references/spec-04-design.md   — 色彩系统与设计指南（~365行）
```

### 自检：确认已完整读取（读完 4 个文件后必做）

读完 4 个规范文件后，向用户报告以下自检结果，确认没有遗漏：

```
📋 设计规范阅读自检：

spec-01-tags.md  ✅ 已读
  → 7 个可用标签：section / p / span / strong / em / img / br
  → 强制属性：box-sizing:border-box + max-width:100%!important
  → <span leaf=""> 包裹铁律已确认

spec-02-css.md   ✅ 已读
  → 5 个最危险的禁用 CSS：position:absolute / animation / calc() / var() / @media
  → flex 是主力布局，grid 仅用于 SVG 绝对定位

spec-03-components.md ✅ 已读
  → 4 种安全布局模式：Flex行/列/左右分栏/Grid叠加
  → 15 个组件模板 + 3 种代码块变体已过目

spec-04-design.md ✅ 已读
  → 颜色值格式：仅 #hex / rgb() / rgba()
  → Do's 清单 8 条 + Don'ts 清单 10 条已确认
  → 头部卡片 4 必须项 + 尾部卡片 3 必须项已确认
```

**如果任何一项无法确认，说明没有完整读取——回到对应文件重新读。**

---

## 微信公众号兼容性规则（核心摘要，设计时对照检查）

> 以下为快速对照表。完整规则见上面 4 个 spec 文件——已读过则此处仅用于生成时逐项对照。

### 标签白名单（仅 7 个）

| 标签 | 用途 | 铁律 |
|------|------|------|
| `<section>` | 唯一块级容器 | 替代 div |
| `<p>` | 段落 | `margin:0px` 强制 |
| `<span>` | 行内文字 | 必须 `<span leaf="">` |
| `<strong>` | 加粗 | |
| `<em>` | 斜体 | |
| `<br>` | 换行 | `<br/>` |
| `<img>` | 图片 | `draggable="false"` |

禁用：div / h1-h6 / table / ul / ol / a / style / link

### 每条元素必带

```css
box-sizing: border-box;
max-width: 100% !important;
```

### 正文默认参数

```
字号:14px  行高:1.85  段落间距:8px  letter-spacing:0.3px

---

## Workflow

```
用户: "排版"
  ↓
Phase 0: 读 final.md + 分析文章情绪/结构
  ↓
Phase 1: 排版方式选择（A 6套预设 / B 自己描述 / C AI 全原创设计）
  ↓
Phase 2: 读主题设计语言 → 分析文章内容 → 原创设计 → 生成 HTML
  ↓
Phase 3: 生成 output-preview.html
  ↓
Phase 4: 脚本校验 + 交付
```

---

## Phase 0 · 读取 + 内容分析

1. 读 `outputs/{标题}_{日期}/article/final.md`
2. 提取 frontmatter（title/summary）
3. 跳过「标题候选」「简介」段，取最后一个 `---` 之后的正文
4. **分析文章内容**（这是后续设计决策的基础）：
   - 判定文章类型：教程/盘点/观点/访谈/数据/随笔/案例（可复合，取主导类型）
   - 感知文章情绪：冷静分析/激情论证/温暖叙事/权威报告/轻松分享
   - 识别结构特征：是否有代码块、是否有大量数据、是否有金句/引用、图片密度
5. 检查封面是否做了 → 没做给出提示，但不强制
6. 检查配图是否做了 → 没做可选跳过

---

## Phase 1 · 排版方式选择

```
🎨 排版方式：

A. 预设主题 — 6 套精选设计语言可选
B. 自己描述 — 你来描述想要的排版风格
C. AI 全原创 — 不套预设，AI 根据文章内容自主设计整套视觉方案

选 A / B / C？
```

### A. 预设主题

**必须先读取 `references/theme-index.md`**，按以下策略推荐：

1. 根据 Phase 0 分析的文章类型/情绪，从 6 套主题中选最契合的 1 个标"推荐"+ 2 个备选
2. 展示给用户一步确认：

```
🎨 选择设计语言：

1. 极简蓝（推荐）— 克制·理性·呼吸感，适合技术教程
2. 暖纸墨 — 温度·杂志感·细线分隔，适合深度观点
3. 暗夜青 — 科技·终端美学，适合数据报告
4. 森语绿 — 自然·侘寂·大留白，适合随笔
5. 绯红编 — 编辑风骨·红白张力，适合作品评测
6. 墨金雅 — 墨色·金饰·经典比例，适合人物特稿

选 1-6？
```

**题材→主题契合参考**（theme-index.md 的权威映射）：

| 题材 | 推荐主题 | 理由 |
|------|---------|------|
| 技术教程 / 工具测评 / 知识整理 | 极简蓝 | 克制理性，蓝色锚点引导阅读路径 |
| 观点分析 / 深度思考 / 人文 | 暖纸墨 | 杂志翻阅感，细线分隔营造阅读节奏 |
| 开发技术 / 数据报告 / 产品深潜 | 暗夜青 | 终端美学，数据在暗底上更有冲击力 |
| 随笔 / 生活方式 / 个人反思 | 森语绿 | 大留白给文字呼吸空间 |
| 深度评测 / 行业分析 / 案例复盘 | 绯红编 | 编辑风骨，结构感强化论证逻辑 |
| 人物访谈 / 品牌叙事 / 高端内容 | 墨金雅 | 墨色金饰，经典比例提升内容重量 |

**全自动模式**（用户说"直接排 / 一键 / 不用问"）→ 不提问，自动选默认主题（极简蓝），交付时说明选择理由。

### B. 自己描述

```
💬 说说你想要的排版感觉：
（例："浅米色底，深咖色字，像读纸书" / "白色底但标题用大红色，段落间距大一点"）
```

收到描述后，AI 自行定义设计变量（主色/底色/气质/节奏），仍需：
- 遵守微信公众号兼容性规则（design-spec.md 的平台约束）
- 遵守正文排版默认参数（字号 14px、行高 1.85）
- 给出设计理念一句话

### C. AI 全原创设计

**不套任何预设主题**，AI 根据文章内容自主设计整套视觉方案：

1. **分析文章基因**：文章类型 + 情绪调性 + 内容特征（代码多？数据多？金句多？）
2. **定义设计变量**：自选主色/底色/气质关键词/节奏策略
3. **设计每个组件**：从零创作，不参考预设主题
4. **硬约束**（不可突破）：
   - 遵守 design-spec.md 的平台约束（标签白名单、CSS 安全清单）
   - 遵守正文排版默认参数（字号 14px、行高 1.85）
   - 所有中文文字 `<span leaf="">` 包裹
   - 颜色对比度 ≥ 4.5:1
5. **软约束**（可突破但需有理由）：60-30-10 配色比例、主色出现 ≤5 处
6. **交付时**：给这套临时方案命名（如"冰岛蓝调"），说明设计理念。用户满意可建议登记为常驻主题

直接进入 Phase 2，无需用户进一步确认。

---

## Phase 2 · 原创设计 → 生成 output.html

> ⚠️ **核心思路**：这是**设计创作**而非模板填充。AI 理解设计语言后，为当前文章进行独一无二的排版设计。
>
> **开始前必读**（前置阅读章节中已读完 4 个 spec 文件，此处仅补充设计语言文件）：
> 1. **选 A（预设主题）** → 读取对应 `references/theme-{标识}.md`（设计变量+设计原则+组件设计模式+设计策略），同时读取 `references/common-components.md`（代码块/图片/分割线通用参考）
> 2. **选 B（自己描述）** → 读取 `references/common-components.md`，设计变量从用户描述推导
> 3. **选 C（AI 全原创）** → 读取 `references/common-components.md`，设计变量完全自主定义
> 4. **平台约束** → 前置阅读已读完 spec-01~04，生成时对照 SKILL.md 中的核心摘要逐项检查

### 设计流程（每步都是创作，不是复制）

```
读设计语言 → 理解气质内核
      ↓
分析文章结构 → 识别设计机会（哪里需要锚点/哪里需要节奏打断/哪里需要呼吸）
      ↓
设计每个组件 → 根据文章内容原创形态（组件设计模式是灵感，不是模板）
      ↓
按文章骨架装配 → 全局容器 + 头部卡 + 章节序列 + 尾部卡
      ↓
逐段标注关键词下划线 → 每段 1-3 处
      ↓
检查视觉节奏 → 锚点≤5处 / 段落疏密有致 / 无连续长段落
```

### 关键设计决策

| 决策点 | 依据 | 自由度 |
|--------|------|--------|
| 代码块深色/浅色 | 主题底色深浅 → 暗底用深色代码块，亮底可用浅色 | 自由选择 |
| 章节标题形态 | 主题设计模式 + 章节数量 → 多章节可用编号卡片，少章节可用左竖条 | 自由演绎 |
| 引用块风格 | 主题气质 + 引用内容长度 → 长引用用左竖条，短金句可居中大字 | 自由选择 |
| 分割线样式 | 主题气质 → 极简用点、温暖用线、科技用符号 | 自由创造 |
| 首段处理 | 文章类型 → 故事型可首字放大，教程型直接进入 | 自由决定 |
| 图片圆角/阴影 | 主题气质 → 圆角 4-12px 范围，阴影 0-8px 深度 | 微调范围 |

### 平台铁律（不可突破）

- 所有中文文字节点 `<span leaf="">文字</span>` 包裹
- 仅用 `<section>/<p>/<span>/<strong>/<em>/<img>/<br>`
- 禁 `<div>/<h1~h6>/<style>/<table>/<a>`
- 所有 CSS 内联，`box-sizing:border-box;` + `max-width:100%!important;` 每个元素必带
- 正文 14px / 行高 1.85 / 段落间距 8px
- position/float/grid/animation/@media/var()/calc() 禁用

### 输出文件

保存到 `outputs/{标题}_{日期}/article/output.html`

结构：全局容器 `<section>` 包裹全文 + 头部信息卡 + 正文（章节标题+段落+引用+代码+图片）+ 尾部互动卡

### 配图处理

配图由 `wechatpost-illustrate` 阶段生成为本地 PNG，路径已写入 final.md。排版时使用本地相对路径：

```html
<img src="illustrations/01-xxx.png" alt="{主题}" style="max-width:100%;border-radius:4px;margin:16px 0">
```


---

## Phase 3 · 生成 output-preview.html

生成手机预览版，单文件零外部依赖：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>WeChatPost · 排版预览</title>
<style>
  :root{
    --bg:#0f0f14; --panel:#16161d; --panel2:#1c1c24;
    --text:#e4e4e7; --dim:#6b6b75; --accent:#f43f5e;
    --border:#252530; --green:#07c160;
    --font-sys:'PingFang SC','Microsoft YaHei',-apple-system,sans-serif;
    --font-mono:'JetBrains Mono','Cascadia Code','SF Mono',monospace;
  }
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{height:100%;overflow:hidden}
  body{
    font-family:var(--font-sys);background:var(--bg);color:var(--text);
    display:flex;flex-direction:column;-webkit-font-smoothing:antialiased;
  }

  /* ===== Top Bar ===== */
  .topbar{
    flex-shrink:0;display:flex;align-items:center;justify-content:space-between;
    padding:8px 20px;height:44px;border-bottom:1px solid var(--border);
    background:rgba(22,22,29,.85);backdrop-filter:blur(16px);
    -webkit-backdrop-filter:blur(16px);z-index:50;
  }
  .topbar-left{display:flex;align-items:center;gap:16px;}
  .logo{font-size:14px;font-weight:800;letter-spacing:.5px;user-select:none;white-space:nowrap;}
  .logo span{color:var(--accent);}
  .topbar-right{display:flex;align-items:center;gap:12px;}

  .width-switch{display:flex;gap:1px;background:var(--panel2);border-radius:6px;padding:2px;border:1px solid var(--border);}
  .width-switch button{
    padding:4px 10px;border:none;background:transparent;font-size:10px;
    font-family:var(--font-sys);cursor:pointer;color:var(--dim);border-radius:4px;
    transition:all .18s;font-weight:500;white-space:nowrap;
  }
  .width-switch button.active{background:var(--accent);color:#fff;font-weight:700;}

  .copy-btn{
    padding:6px 16px;border:none;border-radius:6px;
    background:var(--green);color:#fff;
    font-size:11px;font-weight:700;font-family:var(--font-sys);
    letter-spacing:.4px;cursor:pointer;
    box-shadow:0 2px 10px rgba(7,193,96,.25);
    transition:all .2s;white-space:nowrap;
  }
  .copy-btn:hover{background:#06ad51;box-shadow:0 4px 16px rgba(7,193,96,.4);transform:translateY(-1px);}
  .copy-btn:active{transform:translateY(0);}
  .copy-btn:disabled{background:#333;cursor:not-allowed;box-shadow:none;color:#666;}
  .copy-status{font-size:10px;color:#22c55e;letter-spacing:.3px;transition:all .3s;}

  /* ===== Main ===== */
  .main{flex:1;display:flex;gap:0;min-height:0;}

  /* ===== Left Panel ===== */
  .panel-input{flex:1;background:var(--panel);display:flex;flex-direction:column;overflow:hidden;border-right:1px solid var(--border);min-width:0;}
  .panel-input .head{flex-shrink:0;padding:8px 16px;height:40px;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;background:var(--panel2);}
  .panel-input .head .label{font-size:10px;font-weight:700;letter-spacing:2px;color:var(--dim);text-transform:uppercase;}
  .head-actions{display:flex;gap:6px;align-items:center;}
  .btn{padding:5px 10px;border:1px solid var(--border);border-radius:4px;background:var(--panel);color:var(--dim);font-size:10px;font-family:var(--font-sys);cursor:pointer;transition:all .18s;font-weight:500;white-space:nowrap;}
  .btn:hover{border-color:var(--accent);color:var(--accent);background:rgba(244,63,94,.05);}
  .panel-input textarea{flex:1;width:100%;border:none;outline:none;resize:none;font-family:var(--font-mono);font-size:11px;line-height:1.75;color:#c4c4cc;padding:14px 16px;background:transparent;tab-size:2;}
  .panel-input textarea::placeholder{color:#484850;font-family:var(--font-sys);font-size:12px;}

  /* ===== Right Panel ===== */
  .panel-preview{
    flex:0 0 520px;display:flex;flex-direction:column;align-items:center;
    justify-content:center;gap:0;padding:16px 20px;position:relative;
    background:radial-gradient(ellipse 60% 35% at 50% 45%,rgba(244,63,94,.03) 0%,transparent 70%),
               radial-gradient(ellipse at center,rgba(22,22,28,.95) 0%,var(--bg) 70%);
  }

  .phone-scene{
    flex:1;display:flex;align-items:center;justify-content:center;
    width:100%;min-height:0;
    filter:drop-shadow(0 20px 50px rgba(0,0,0,.45))
           drop-shadow(0 6px 12px rgba(0,0,0,.25));
    transition:filter .4s;
  }
  .phone-scene:hover{
    filter:drop-shadow(0 28px 60px rgba(0,0,0,.55))
           drop-shadow(0 10px 20px rgba(0,0,0,.35))
           drop-shadow(0 0 40px rgba(244,63,94,.03));
  }

  .phone{
    position:relative;display:flex;flex-direction:column;
    width:390px;height:100%;border-radius:44px;padding:5px;
    background:linear-gradient(180deg,rgba(255,255,255,.16) 0%,rgba(255,255,255,.04) 3%,transparent 8%,rgba(0,0,0,.02) 80%,rgba(0,0,0,.06) 93%,rgba(255,255,255,.02) 97%,rgba(255,255,255,.04) 100%),
               linear-gradient(90deg,rgba(255,255,255,.06) 0%,rgba(255,255,255,.01) 5%,transparent 10%,transparent 88%,rgba(0,0,0,.04) 95%,rgba(0,0,0,.06) 98%,rgba(255,255,255,.03) 100%),
               linear-gradient(175deg,#c4beb4 0%,#cec8be 3%,#c6c0b6 8%,#b4aea4 18%,#a6a096 30%,#9c968e 45%,#a09a92 55%,#aea89e 68%,#bab4aa 82%,#c2bcb2 92%,#beb8ae 100%);
    box-shadow:inset 0 1px 0 rgba(255,255,255,.05),inset 0 -1px 0 rgba(0,0,0,.12),0 0 0 .5px rgba(0,0,0,.2);
  }

  .screen{
    flex:1;display:flex;flex-direction:column;
    background:#fff;border-radius:39px;overflow:hidden;
    position:relative;z-index:1;
  }
  .screen::after{
    content:'';position:absolute;inset:0;pointer-events:none;z-index:3;border-radius:39px;
    background:linear-gradient(155deg,rgba(255,255,255,.12) 0%,rgba(255,255,255,.03) 3%,transparent 8%,transparent 55%,rgba(255,255,255,.01) 80%,rgba(255,255,255,.02) 100%),
               linear-gradient(0deg,rgba(0,0,0,.01) 0%,transparent 30%);
  }

  .dynamic-island{
    position:absolute;z-index:10;top:10px;left:50%;transform:translateX(-50%);
    width:120px;height:34px;background:#000;border-radius:20px;
    box-shadow:0 0 0 .5px rgba(120,120,130,.2);
  }
  .speaker-slit{position:absolute;z-index:9;top:4px;left:50%;transform:translateX(-50%);width:50px;height:2px;background:#1a1a1a;border-radius:1px;opacity:.7;}

  .statusbar{
    flex-shrink:0;z-index:5;padding:12px 26px 4px;
    font-size:10.5px;font-weight:600;color:#1a1a1a;
    display:flex;justify-content:space-between;
    font-family:-apple-system,'SF Pro Text',sans-serif;
  }

  .content{
    flex:1;overflow-y:auto;overflow-x:hidden;
    padding:0;position:relative;z-index:2;min-height:0;
    -webkit-overflow-scrolling:touch;scroll-behavior:smooth;
  }
  .content::-webkit-scrollbar{width:3px;}
  .content::-webkit-scrollbar-track{background:transparent;}
  .content::-webkit-scrollbar-thumb{background:rgba(0,0,0,.08);border-radius:2px;}

  .scroll-fade{
    position:absolute;bottom:0;left:0;right:0;z-index:6;
    height:28px;pointer-events:none;
    background:linear-gradient(0deg,rgba(255,255,255,.9) 0%,transparent 100%);
    opacity:0;transition:opacity .3s;
  }
  .scroll-fade.on{opacity:1;}

  .homebar{
    flex-shrink:0;height:18px;z-index:5;
    display:flex;align-items:flex-start;justify-content:center;
  }
  .homebar::after{content:'';width:134px;height:4px;background:#1a1a1a;border-radius:2px;opacity:.12;}

  /* Side buttons */
  .sbtn{
    position:absolute;pointer-events:none;z-index:0;
    background:linear-gradient(180deg,rgba(255,255,255,.12) 0%,#c0bab0 15%,#aea89e 40%,#9e9890 60%,#b6b0a6 85%,rgba(255,255,255,.06) 100%);
    box-shadow:inset 0 1px 0 rgba(255,255,255,.08),0 1px 3px rgba(0,0,0,.3),0 0 0 .5px rgba(0,0,0,.18);
  }

  .empty-state{
    display:flex;flex-direction:column;align-items:center;
    justify-content:center;height:100%;text-align:center;
    padding:50px 30px;user-select:none;
  }
  .empty-state .ph-icon{width:56px;height:56px;border-radius:14px;background:rgba(0,0,0,.025);display:flex;align-items:center;justify-content:center;margin-bottom:20px;animation:pulse 2.5s ease-in-out infinite;}
  @keyframes pulse{0%,100%{transform:scale(1);opacity:.4;}50%{transform:scale(1.06);opacity:.7;}}
  .empty-state .ph-icon svg{width:26px;height:26px;color:#bbb;}
  .empty-state h3{font-size:14px;font-weight:600;color:#666;margin:0 0 6px;}
  .empty-state p{font-size:11px;color:#aaa;line-height:1.8;margin:0;max-width:240px;}

  .toast{position:fixed;bottom:32px;left:50%;transform:translateX(-50%) translateY(12px);padding:10px 26px;background:#1f1f28;color:#fff;font-size:13px;letter-spacing:.3px;border-radius:8px;border:1px solid var(--border);box-shadow:0 10px 32px rgba(0,0,0,.55);opacity:0;pointer-events:none;transition:all .28s;z-index:100;}
  .toast.show{opacity:1;transform:translateX(-50%) translateY(0);}

  @media(max-width:860px){
    body{overflow:auto;}
    .main{flex-direction:column;}
    .panel-input{min-height:260px;border-right:none;border-bottom:1px solid var(--border);}
    .panel-input textarea{min-height:160px;}
    .panel-preview{flex:0 0 auto;padding:12px;min-height:500px;}
    .topbar{padding:6px 12px;height:auto;flex-wrap:wrap;gap:8px;}
  }
</style>
</head>
<body>

<!-- Top Bar -->
<div class="topbar">
  <div class="topbar-left">
    <div class="logo">WeChatPost · <span>排版预览</span></div>
    <div class="width-switch" id="widthSwitch">
      <button data-w="375">375</button>
      <button data-w="390" class="active">390</button>
      <button data-w="414">414</button>
    </div>
  </div>
  <div class="topbar-right">
    <span class="copy-status" id="copyStatus"></span>
    <button class="copy-btn" id="btnCopy" disabled>📋 复制到公众号</button>
  </div>
</div>

<div class="main">

  <!-- Left: HTML Source -->
  <div class="panel-input">
    <div class="head">
      <span class="label">HTML 源码</span>
      <div class="head-actions">
        <button class="btn" id="btnFormat">格式化</button>
        <button class="btn" id="btnClear">清空</button>
      </div>
    </div>
    <textarea id="htmlSource" placeholder="在此粘贴 AI 排版生成的 HTML……&#10;&#10;Ctrl+V 粘贴 · Ctrl+Enter 复制 · 拖拽 .html 文件加载"></textarea>
  </div>

  <!-- Right: Phone Preview -->
  <div class="panel-preview">
    <div class="phone-scene">
      <div class="phone">
        <div class="sbtn" style="right:-3px;top:145px;width:3px;height:56px;border-radius:2px;"></div>
        <div class="sbtn" style="left:-3px;top:136px;width:3px;height:38px;border-radius:2px;"></div>
        <div class="sbtn" style="left:-3px;top:184px;width:3px;height:38px;border-radius:2px;"></div>
        <div class="screen">
          <div class="speaker-slit"></div>
          <div class="dynamic-island"></div>
          <div class="statusbar"><span id="timeLabel">9:41</span><span style="font-size:9px">▮▮▮▮ &nbsp;⋮⋮⋮⋮</span></div>
	  <div class="content" id="content">
	    <div class="empty-state" id="emptyState">
	      <div class="ph-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="5" y="2" width="14" height="20" rx="2"/><line x1="12" y1="18" x2="12" y2="18.01" stroke-width="2.5"/></svg></div>
	      <h3>准备预览</h3>
	      <p>在左侧面板粘贴公众号 HTML<br/>或拖拽 .html 文件至此</p>
	    </div>
	  </div>
          <div class="scroll-fade" id="scrollFade"></div>
          <div class="homebar"></div>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<!-- 排版 HTML 数据注入点（AI 生成时替换此处内容） -->
<script id="article-data" type="text/x-template"></script>

<script>
const htmlSource = document.getElementById('htmlSource');
const contentEl  = document.getElementById('content');
const scrollFade = document.getElementById('scrollFade');
const btnCopy    = document.getElementById('btnCopy');
const copyStatus = document.getElementById('copyStatus');
const timeLabel  = document.getElementById('timeLabel');
const toastEl    = document.getElementById('toast');

let currentWidth = 390;

/* ===== Width Switching ===== */
function applyWidth(w) {
  currentWidth = w;
  renderContent();
}
document.getElementById('widthSwitch').addEventListener('click', function(e){
  var b = e.target.closest('button');
  if (!b) return;
  var w = parseInt(b.dataset.w);
  if (w === currentWidth) return;
  this.querySelectorAll('button').forEach(function(x){ x.classList.remove('active'); });
  b.classList.add('active');
  applyWidth(w);
});

/* ===== Format HTML ===== */
function formatHTML(html) {
  html = html.trim();
  var result = '', indent = 0, i = 0, len = html.length;
  while (i < len) {
    if (html[i] === '<') {
      if (html[i+1] === '/') {
        indent = Math.max(0, indent - 1);
        result += '\n' + '  '.repeat(indent);
        var j = i; while (j < len && html[j] !== '>') j++;
        result += html.substring(i, j+1); i = j + 1;
      } else if (/^<(img|br|input|hr|meta|link)[\s>]/i.test(html.substring(i))) {
        result += '\n' + '  '.repeat(indent);
        var j = i; while (j < len && html[j] !== '>') j++;
        result += html.substring(i, j+1); i = j + 1;
      } else {
        result += '\n' + '  '.repeat(indent);
        var j = i; while (j < len && html[j] !== '>') j++;
        var tag = html.substring(i, j+1);
        result += tag; i = j + 1;
        if (!/^<(span|strong|em|br|img)\b/i.test(tag) && !/\/>$/.test(tag)) indent++;
      }
    } else {
      var j = i; while (j < len && html[j] !== '<') j++;
      var txt = html.substring(i, j);
      if (txt.trim()) result += txt;
      i = j;
    }
  }
  return result.trim();
}
document.getElementById('btnFormat').addEventListener('click', function(){
  if (!htmlSource.value.trim()) return;
  htmlSource.value = formatHTML(htmlSource.value);
  showToast('HTML 已格式化 ✓');
});
document.getElementById('btnClear').addEventListener('click', function(){
  htmlSource.value = ''; renderContent(); showToast('已清空');
});

/* ===== Render ===== */
function renderContent(){
  var h = htmlSource.value.trim();
  if (h) {
    h = h.replace(/(max-width:\s*)\d+(px)/g, '$1'+currentWidth+'$2');
    if (!/max-width/.test(h)) {
      h = h.replace(/^(<section\s[^>]*style=")/, '$1max-width:'+currentWidth+'px;');
    }
    contentEl.innerHTML = h;
  } else {
    contentEl.innerHTML = '<div class="empty-state"><div class="ph-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="5" y="2" width="14" height="20" rx="2"/><line x1="12" y1="18" x2="12" y2="18.01" stroke-width="2.5"/></svg></div><h3>准备预览</h3><p>在左侧面板粘贴公众号 HTML<br/>或拖拽 .html 文件至此</p></div>';
  }
  btnCopy.disabled = !h;
  copyStatus.textContent = '';
  scrollFade.classList.remove('on');
  requestAnimationFrame(updateScrollFade);
}
function updateScrollFade(){
  var has = contentEl.scrollHeight > contentEl.clientHeight + 2;
  var atBottom = contentEl.scrollTop + contentEl.clientHeight >= contentEl.scrollHeight - 8;
  scrollFade.classList.toggle('on', has && !atBottom);
}
htmlSource.addEventListener('input', renderContent);
contentEl.addEventListener('scroll', updateScrollFade);

/* ===== Drag & Drop ===== */
document.addEventListener('dragover', function(e){ e.preventDefault(); });
document.addEventListener('drop', function(e){
  e.preventDefault();
  var file = e.dataTransfer.files[0];
  if (!file) return;
  if (file.name.endsWith('.html') || file.name.endsWith('.htm') || file.type === 'text/html') {
    var reader = new FileReader();
    reader.onload = function(ev){ htmlSource.value = ev.target.result; renderContent(); showToast('已加载: ' + file.name); };
    reader.readAsText(file);
  } else { showToast('请拖入 .html 文件'); }
});

/* ===== Copy to WeChat (ClipboardItem API + fallback) ===== */
function copyToWechat(){
  var h = htmlSource.value.trim();
  if (!h) { showToast('请先粘贴 HTML 内容'); return; }
  // 包裹白色背景层，避免微信编辑器默认黑底
  var raw = '<section style="background:#fff;box-sizing:border-box;max-width:100%!important;padding:0 6px">'+h+'</section>';
  // ClipboardItem API（HTTPS/localhost）
  if (window.isSecureContext && navigator.clipboard && navigator.clipboard.write) {
    try {
      var htmlBlob = new Blob([raw], {type:'text/html'});
      var textBlob = new Blob([h.replace(/<[^>]+>/g,' ')], {type:'text/plain'});
      navigator.clipboard.write([new ClipboardItem({'text/html':htmlBlob,'text/plain':textBlob})]).then(function(){
        copyStatus.textContent = '✓ 已复制';
        showToast('已复制到剪贴板 · Ctrl+V 粘贴到公众号后台');
        setTimeout(function(){ copyStatus.textContent = ''; }, 3000);
      }, function(){ execCommandFallback(raw); });
      return;
    } catch(e){ execCommandFallback(raw); }
  }
  execCommandFallback(raw);
}
function execCommandFallback(raw){
  var tmp = document.createElement('div');
  tmp.contentEditable = 'true';
  tmp.style.cssText = 'position:fixed;left:-9999px;top:-999px;width:375px;height:auto;';
  tmp.innerHTML = raw;
  document.body.appendChild(tmp);
  var range = document.createRange(); range.selectNodeContents(tmp);
  var sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(range);
  var handler = function(e){
    try{ e.clipboardData.setData('text/html', raw); }catch(ex){}
    document.removeEventListener('copy', handler, true);
  };
  document.addEventListener('copy', handler, true);
  var ok = false;
  try{ ok = document.execCommand('copy'); }catch(ex){ ok = false; }
  sel.removeAllRanges(); document.body.removeChild(tmp);
  document.removeEventListener('copy', handler, true);
  if (ok) {
    copyStatus.textContent = '✓ 已复制';
    showToast('已复制到剪贴板 · Ctrl+V 粘贴到公众号后台');
    setTimeout(function(){ copyStatus.textContent = ''; }, 3000);
  } else {
    showToast('复制失败，请手动全选后 Ctrl+C');
  }
}
btnCopy.addEventListener('click', copyToWechat);
document.addEventListener('keydown', function(e){
  if ((e.ctrlKey||e.metaKey) && e.key === 'Enter'){ e.preventDefault(); if (!btnCopy.disabled) copyToWechat(); }
});

// Paste detection
document.addEventListener('paste', function(e){
  if (e.target.tagName === 'TEXTAREA' || e.target.tagName === 'INPUT') return;
  var h = (e.clipboardData.getData('text/html') || e.clipboardData.getData('text/plain'));
  if (h && /<section/i.test(h)) { e.preventDefault(); htmlSource.value = h; renderContent(); showToast('已识别 HTML · 预览已更新'); }
});

function showToast(msg){ toastEl.textContent = msg; toastEl.classList.add('show'); setTimeout(function(){ toastEl.classList.remove('show'); }, 2500); }
function updateTime(){ var d = new Date(); timeLabel.textContent = d.getHours().toString().padStart(2,'0')+':'+d.getMinutes().toString().padStart(2,'0'); }
setInterval(updateTime, 30000); updateTime();

// 自动加载排版生成的 HTML 内容（从内嵌 <script> 标签读取）
(function(){
  var el = document.getElementById('article-data');
  if (el && el.textContent && el.textContent.trim()) {
    htmlSource.value = el.textContent.trim();
    renderContent();
  }
  // 兼容旧版 window.name 机制（保留作为 fallback）
  if (window.name && window.name.indexOf('WECHATPOST_HTML:') === 0) {
    var html = decodeURIComponent(window.name.slice('WECHATPOST_HTML:'.length));
    window.name = '';
    if (html && html.trim()) { htmlSource.value = html; renderContent(); }
  }
})();
</script>
</body>
</html>
```

保存到：`outputs/{标题}_{日期}/article/output-preview.html`

### ⚠️ 注入排版 HTML（强制）

**写入 output-preview.html 时，必须将 Phase 2 生成的 `output.html` 完整内容注入到预览页面中**，让用户打开文件即可看到排版效果，无需手动粘贴。

具体操作：

1. **读取** Phase 2 生成的 `outputs/{标题}_{日期}/article/output.html`
2. 在 output-preview.html 模板中，找到：
   ```html
   <script id="article-data" type="text/x-template"></script>
   ```
3. 将该标签的内容替换为 `output.html` 的**原始 HTML**（不需要转义，放在 `<script type="text/x-template">` 内不会被渲染）
4. 写入文件后，页面 JS 会自动读取该标签内容并注入 textarea + 渲染预览

**注入示例**：
```html
<script id="article-data" type="text/x-template"><section style="max-width:677px;margin:0 auto;...">...正文内容...</section></script>
```

> 注意：如果 HTML 内容中包含 `</script>` 字符串，需替换为 `<\/script>` 防止提前闭合。

---

## Phase 4 · 校验 + 交付

### 4.1 脚本校验（强制）

生成 `output.html` 后，**必须运行校验脚本**，ERROR 清零才算完成：

```bash
python <skill-root>/skills/wechatpost-format/scripts/validate_gzh_html.py <outputs/{标题}_{日期}/article/output.html 的绝对路径>
```

脚本确定性检查以下内容：

| 检查项 | 级别 | 说明 |
|--------|------|------|
| `<style>` / `<script>` / `<div>` / `<link>` 标签 | ERROR | 会被公众号过滤 |
| `class` / `id` 属性 | ERROR | 会被剥离 |
| `position:fixed/absolute/sticky` / `float` | ERROR | 不被支持 |
| `display:grid` / `@media` / `@keyframes` | ERROR | 不被支持 |
| CSS 变量 `var(--x)` | ERROR | 不被支持 |
| `<span leaf="">` 包裹率 | ERROR/WARNING | **中文文本未被包裹 → 粘贴后样式丢失** |
| 半角标点 / 英文引号 | WARNING | 应改为中文全角 |

**失败处理**：ERROR → 回到 Phase 2 修复 → 重新生成 → 重新校验；WARNING 同样修复到 0 再交付。

### 4.2 自检清单（辅助）

重读 output.html 补充验证：

- [ ] 文件存在，字节 > 1000
- [ ] 无 `<div>`、`<h1~h6>`、`<style>` 标签
- [ ] 所有样式内联
- [ ] `![alt](path)` 已转为 `<img>` 标签，引用本地路径
- [ ] 封面图路径正确
- [ ] **所有中文文字节点已 `<span leaf="">` 包裹**

```
✅ 排版完成：outputs/{标题}_{日期}/article/
  ├── output.html          ← 公众号粘贴用
  └── output-preview.html  ← 手机预览 + 一键复制

下一步：打开 output-preview.html 预览 → 复制 HTML → 粘贴公众号后台 → 上传封面 cover/cover-2x35.png
```

---

## Key Rules

1. **先读设计语言再动手**——选 A 必须读主题设计语言文件+common-components；选 B/C 至少读 common-components+design-spec
2. **设计创作 > 模板填充**——主题文件提供设计原则和灵感参考，AI 根据每篇文章内容原创演绎
3. **只用 `<section>/<p>/<span>/<strong>/<em>/<img>/<br>`**——其余标签禁用
4. **所有中文文字节点用 `<span leaf="">文字</span>` 包裹**——否则粘贴后样式大面积丢失
5. **所有 CSS 内联**——无 `<style>` 标签
6. **每个元素必带 `box-sizing:border-box;` + `max-width:100%!important;`**
7. **margin 清零**——所有 `<p>` 设 `margin:0`，段落间用 `margin-bottom:8px`
8. **配图用本地相对路径**——`<img>` 引用 `illustrations/` 下的本地 PNG
9. **字号 14px 起**——公众号最小可读字号，行高 1.85
10. **必须跑 `validate_gzh_html.py` 校验**——ERROR 清零才交付，半角标点 WARNING 同样清零
11. **每篇文章排版必须不同**——即使同主题，不同文章应有不同的视觉演绎
