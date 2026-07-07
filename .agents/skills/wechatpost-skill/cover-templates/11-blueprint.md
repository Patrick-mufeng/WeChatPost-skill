# 11 · Blueprint · 工程蓝图

```yaml
name: "工程蓝图"
name_en: "Blueprint"
keywords: [蓝图, 工程, 网格, 青色, 图纸, 技术]
best_for: [技术教程, 开发者文档, 系统架构, 开源项目]
emotional_tone: "冷峻"

palette:
  bg: "#0d1b3e"
  surface: "rgba(255,255,255,0.03)"
  primary: "#4da8da"
  accent: "#ffffff"
  text: "#c8ddf0"
  muted: "#5a7a9a"

fonts:
  heading: "'IBM Plex Sans', 'Inter', 'PingFang SC', sans-serif"
  body: "'IBM Plex Mono', 'JetBrains Mono', 'PingFang SC', monospace"

layout_2_35: "split"
layout_1_1: "framed"

core_rules:
  - "背景深蓝，覆盖白色网格线（类似工程蓝图纸），线间距 30-50px"
  - "所有文字和线条使用白色或浅蓝（primary），模拟蓝图白线"
  - "右侧或底部必须有工程标注：使用 monospace 的规格列表"
  - "标题字体用粗体无衬线，正文用等宽"
  - "边框和分割线全部使用 1px solid primary"
  - "必须有一个类似图纸编号的标记（如 REV-01 / SPEC-A3）"

negative_rules:
  - "禁止使用暖色——蓝图只有蓝+白"
  - "禁止使用圆角——工程图纸是直的"
  - "禁止使用渐变填充"
  - "禁止使用阴影效果——线条要干净利落"

variants:
  - name: "白图版"
    diff: "bg 改为 #f0f4f8, primary 改为 #1a56db，白底蓝线"
    use_when: "需要更明亮、更现代的图纸感"
  - name: "暗夜工程版"
    diff: "bg 改为 #020812，降低网格亮度，增强对比"
    use_when: "神秘/机密/黑客项目"

css_snippets:
  keyframes: |
    /* 蓝图不使用动画 */
  effects: |
    .blueprint-grid {
      background-image:
        linear-gradient(rgba(77,168,218,0.15) 1px, transparent 1px),
        linear-gradient(90deg, rgba(77,168,218,0.15) 1px, transparent 1px);
      background-size: 40px 40px;
    }
    .spec-label {
      font-family: monospace;
      color: #4da8da;
      letter-spacing: 1px;
    }
  patterns: |
    .crosshair {
      position: absolute;
      width: 12px; height: 12px;
      border: 1px solid rgba(77,168,218,0.5);
      border-radius: 50%;
    }
    .crosshair::before, .crosshair::after {
      content: ''; position: absolute;
      background: rgba(77,168,218,0.5);
    }
    .crosshair::before { width: 1px; height: 100%; left: 50%; transform: translateX(-50%); }
    .crosshair::after { height: 1px; width: 100%; top: 50%; transform: translateY(-50%); }
```
