# 22 · Bauhaus · 包豪斯

```yaml
name: "包豪斯"
name_en: "Bauhaus"
keywords: [包豪斯, 三原色, 几何, 功能主义, 现代主义]
best_for: [设计理论, 艺术评论, 教育内容, 现代品牌]
emotional_tone: "冷峻"

palette:
  bg: "#f8f6f0"
  surface: "#ffffff"
  primary: "#e63946"
  accent: "#1d3557"
  text: "#111111"
  muted: "#777777"

fonts:
  heading: "'Futura', 'Jost', 'PingFang SC', sans-serif"
  body: "'Futura', 'Jost', 'PingFang SC', sans-serif"

layout_2_35: "asymmetric-right"
layout_1_1: "centered"

core_rules:
  - "配色使用三原色（红黄蓝）+ 黑白灰，不添加其他色相"
  - "标题使用几何无衬线（Futura / Jost），字母圆润几何化"
  - "装饰使用基本几何形：圆形、方形、三角形，纯色平涂"
  - "几何装饰作为背景元素散布，不干扰文字"
  - "排版严格网格对齐，所有元素有清晰的几何关系"
  - "留白充足，功能主义：每个元素都有存在的理由"

negative_rules:
  - "禁止使用渐变色——全部纯色平涂"
  - "禁止使用衬线字体"
  - "禁止使用阴影或发光效果"
  - "禁止装饰性曲线——只使用直线和基础几何"
  - "禁止超过 5 种颜色（红黄蓝黑白）"

variants:
  - name: "暗底版"
    diff: "bg 改为 #1a1a1a, text 改为 #eee，几何色不变"
    use_when: "深色主题/现代简约品牌"
  - name: "不对称版"
    diff: "全部元素左对齐并偏向一侧，另一侧仅放一个大几何形"
    use_when: "更激进的设计表达"

css_snippets:
  keyframes: |
    /* 包豪斯不使用动画 — 形式追随功能 */
  effects: |
    .bauhaus-shape {
      position: absolute;
      opacity: 0.7;
      pointer-events: none;
    }
    .bauhaus-circle {
      width: 80px; height: 80px;
      border-radius: 50%;
      background: #e63946;
    }
    .bauhaus-square {
      width: 70px; height: 70px;
      background: #1d3557;
    }
    .bauhaus-triangle {
      width: 0; height: 0;
      border-left: 40px solid transparent;
      border-right: 40px solid transparent;
      border-bottom: 70px solid #f4d03f;
    }
  patterns: |
    .geometric-bar {
      height: 4px;
      width: 60px;
      background: #111;
    }
```
