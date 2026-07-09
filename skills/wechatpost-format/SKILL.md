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
Phase 1: 排版方式选择（A预设 / B描述 / C AI自主）
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

## Phase 1 · 排版方式选择

先让用户选择排版方式：

```
🎨 排版方式：

A. 预设主题 — 3 套排版模板可选
B. 自己描述 — 你来描述想要的排版风格
C. AI 自主设计 — 不套预设，根据设计规范全新创作

选 A / B / C？
```

### A. 预设主题

```
🎨 选择排版风格：

1. 极简白 — 纯白底+黑色字+蓝色强调，清爽干净
2. 暖纸墨 — 暖灰底+深棕字+细横线分隔，杂志阅读感
3. 暗夜模式 — 深黑底+浅灰字+青色强调，科技感

选 1/2/3？
```

**主题色板**：

| 主题 | 背景色 | 正文色 | 强调色 | 辅助色 | 浅色背景 |
|------|--------|--------|--------|--------|----------|
| 1. 极简白 | `#ffffff` | `#333333` | `#2563eb` | `#666666` | `#f5f7fa` |
| 2. 暖纸墨 | `#fdfaf4` | `#4a3728` | `#b8532a` | `#8b7355` | `#f7f0e6` |
| 3. 暗夜模式 | `#1a1a2e` | `#d0d0d0` | `#00d4aa` | `#888888` | `#252540` |

按用户选择，确定：
- 背景色 / 正文色 / 强调色 / 辅助色 / 浅色背景
- 标题字号 / 加粗方式
- 分隔线样式
- 引用块样式

### B. 自己描述

```
💬 说说你想要的排版感觉：
（例："浅米色底，深咖色字，像读纸书" / "白色底但标题用大红色，段落间距大一点"）
```

收到描述后，根据描述确定配色和排版参数，仍需遵守微信公众号兼容性规则（标签白名单、CSS 安全清单）。

### C. AI 自主设计

不套预设主题、不让用户描述，AI 根据文章内容自主设计排版：

**约束**：
- 不套用 3 套预设主题
- 遵守微信公众号兼容性规则（只用 section/p/span/strong/em/img/br，CSS 全部内联）
- 遵守正文排版默认参数（字号 14px、行高 1.85、颜色 #333）
- 目标：**有设计感** — 配色有辨识度、层级清晰、引用块/分隔线/小标题有风格化处理
- 给出设计理念一句话（如"用暖橙强调色 + 宽段落间距营造呼吸感"）

直接进入 Phase 2，无需用户进一步确认。

---

## Phase 2 · 生成 output.html

> ⚠️ **开始生成前，必须先回顾本文件的「微信公众号兼容性规则」和「正文排版默认参数」两节，确认设计约束后再动笔。**

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

- 封面图片引用：`cover/cover-2x35.png`（相对于 article/ 目录）
- 配图引用：`illustrations/01-xxx.png`（图床 URL，由 illustrate 阶段写入 final.md）
- 保存到：`outputs/{标题}_{日期}/article/output.html`

### 配图处理

配图由 `wechatpost-illustrate` 阶段上传到 beeimg 图床，URL 已写入 final.md。排版时直接用图床 URL：

```html
<img src="https://www.beeimg.cn/xxxx/xxx.png" alt="{主题}" style="max-width:100%;border-radius:4px;margin:16px 0">
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
            <div class="empty-state">
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

// 接收排版生成的 HTML 内容
(function(){
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

下一步：打开 output-preview.html 预览 → 复制 HTML → 粘贴公众号后台 → 上传封面 cover/cover-2x35.png
```

---

## Key Rules

1. **先读规范再动手**——生成 HTML 前必须回顾微信公众号兼容性规则和排版默认参数
2. **只用 `<section>/<p>/<span>/<strong>/<em>/<img>/<br>`**——其余标签禁用
3. **所有 CSS 内联**——无 `<style>` 标签
4. **不做渐变/阴影/变形**——会被过滤
5. **margin 清零**——所有 `<p>` 设 `margin:0`，段落间用 `margin-bottom:8px`
6. **配图用图床 URL**——`<img>` 引用 beeimg 公开链接
7. **字号 14px 起**——公众号最小可读字号
