# 09 · Brutalist Raw · 粗野主义

```yaml
name: "粗野主义"
name_en: "BrutalistRaw"
keywords: [等宽, 工业, 反精致, 极简, 无废话]
best_for: [技术批判, 独立博客, 极客内容, 社会评论]
emotional_tone: "冷峻"

palette:
  bg: "#f4f4f0"
  surface: "#e8e8e4"
  primary: "#111111"
  accent: "#ff4d4d"
  text: "#1a1a1a"
  muted: "#666666"

fonts:
  heading: "'JetBrains Mono', 'IBM Plex Mono', 'PingFang SC', monospace"
  body: "'JetBrains Mono', 'IBM Plex Mono', 'PingFang SC', monospace"

layout_2_35: "left-column"
layout_1_1: "top-down"

core_rules:
  - "全部使用等宽字体——包括标题和正文"
  - "标题前加 # 或 { 前缀，模仿代码或标记语言"
  - "使用 box-shadow 而非 border-radius 创建硬边卡片"
  - "色彩极简：黑/白/灰 + 单一强调色（红色）"
  - "排版像代码块：左对齐，层级用缩进而不是字号变化"
  - "装饰元素：终端光标 █、括号、竖线"

negative_rules:
  - "禁止使用任何圆角"
  - "禁止使用衬线或手写字体"
  - "禁止使用渐变或阴影柔化"
  - "禁止超过 3 种颜色"
  - "禁止装饰性图案——你的装饰就是文字本身"

variants:
  - name: "暗底终端版"
    diff: "bg 改为 #0d0d0d, text 改为 #00ff41, 模仿绿屏终端"
    use_when: "黑客/底层/硬核技术内容"
  - name: "黄底黑字版"
    diff: "bg 改为 #ffff00, text 改为 #000, accent 保持 #ff4d4d"
    use_when: "警示/批判/引起注意的内容"

css_snippets:
  keyframes: |
    @keyframes blinkCursor {
      0%, 100% { opacity: 1; }
      50% { opacity: 0; }
    }
  effects: |
    .cursor::after {
      content: '█';
      animation: blinkCursor 1s step-end infinite;
      color: var(--accent);
    }
    .brutal-box {
      border: 2px solid #111;
      box-shadow: 6px 6px 0 #111;
      background: #fff;
    }
  patterns: |
    .hash-line {
      color: #999;
      font-family: monospace;
    }
    .bracket { color: var(--accent); font-weight: 700; }
```
