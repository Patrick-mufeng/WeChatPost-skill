# 19 · Retro Terminal · 复古终端

```yaml
name: "复古终端"
name_en: "RetroTerminal"
keywords: [终端, CRT, 荧光绿, 命令行, 扫描线, 80s]
best_for: [编程教程, 黑客文化, CLI工具, 复古科技]
emotional_tone: "冷峻"

palette:
  bg: "#0a0a0a"
  surface: "#0d0d0d"
  primary: "#00ff41"
  accent: "#00cc33"
  text: "#b3ffb3"
  muted: "#1a6b1a"

fonts:
  heading: "'VT323', 'Courier New', 'PingFang SC', monospace"
  body: "'VT323', 'Courier New', 'PingFang SC', monospace"

layout_2_35: "left-column"
layout_1_1: "top-down"

core_rules:
  - "全部使用荧光绿单色系，模拟老式 CRT 终端"
  - "背景纯黑，文字全是绿色，不同深浅区分层级"
  - "必须有 CRT 扫描线（repeating-linear-gradient 暗横条）"
  - "必须有闪烁的光标（█ 字符 animation: blink）"
  - "标题前加 $ 或 > 提示符"
  - "边缘使用 vignette 暗角效果（radial-gradient 从中心透明到边缘黑）"

negative_rules:
  - "禁止使用除绿色系以外的任何颜色"
  - "禁止使用衬线或手写字体"
  - "禁止圆角——终端窗口是直角的"
  - "禁止渐变（荧光绿是纯色，不是渐变）"
  - "禁止现代 UI 元素（卡片、阴影、模糊）"

variants:
  - name: "琥珀版"
    diff: "primary 改为 #ffb000，模拟琥珀色单色显示器"
    use_when: "复古工业/控制系统主题"
  - name: "白字版"
    diff: "primary 改为 #ffffff，模拟高对比度黑白显示器"
    use_when: "严肃/专业 CLI 内容"
  - name: "矩阵版"
    diff: "背景加入垂直降落的绿色字符流（类似 Matrix 代码雨）"
    use_when: "Matrix 风格/黑客主题"

css_snippets:
  keyframes: |
    @keyframes blink {
      0%, 49% { opacity: 1; }
      50%, 100% { opacity: 0; }
    }
  effects: |
    .crt-scanlines {
      background: repeating-linear-gradient(
        0deg, transparent, transparent 2px, rgba(0,255,65,0.03) 2px, rgba(0,255,65,0.03) 4px
      );
      pointer-events: none;
    }
    .crt-vignette {
      background: radial-gradient(ellipse at center, transparent 60%, rgba(0,0,0,0.6) 100%);
      pointer-events: none;
    }
    .cursor-blink::after {
      content: '█';
      animation: blink 1s step-end infinite;
      color: #00ff41;
    }
  patterns: |
    .prompt::before {
      content: '$ ';
      color: #00ff41;
    }
    .comment { color: #1a6b1a; } /* muted green for secondary info */
```
