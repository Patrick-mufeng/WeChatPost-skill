# 25 · Origami · 折纸艺术

```yaml
name: "折纸艺术"
name_en: "Origami"
keywords: [折纸, 几何, 光影, 纸质感, 日式, 精确]
best_for: [极简设计, 日式美学, 手工/DIY, 精确内容]
emotional_tone: "严肃"

palette:
  bg: "#f5f0e8"
  surface: "#ffffff"
  primary: "#2c3e50"
  accent: "#e07a3d"
  text: "#1a1a2e"
  muted: "#7a8a9a"

fonts:
  heading: "'Raleway', 'Noto Sans SC', 'PingFang SC', sans-serif"
  body: "'Inter', 'PingFang SC', sans-serif"

layout_2_35: "asymmetric-right"
layout_1_1: "centered"

core_rules:
  - "背景使用米白/浅灰（纸色），装饰元素模拟折纸的几何折叠光影"
  - "核心装饰：三角形/多边形，一侧暗一侧亮，模拟折痕和纸面受光"
  - "使用 CSS clip-path 或 linear-gradient 创造折叠的 3D 错觉"
  - "色板简洁：纸色 + 深色 + 单一强调色"
  - "阴影要硬而干净（不放散），模拟纸张厚度"
  - "装饰区域和文字区域有清晰的分隔（折痕线）"

negative_rules:
  - "禁止使用模糊阴影——折纸阴影是硬的"
  - "禁止圆角——折纸的边是锐利的"
  - "禁止多色渐变——折纸是纯色面"
  - "禁止使用曲线装饰——折纸是直线几何"
  - "禁止超过 4 种颜色"

variants:
  - name: "彩纸版"
    diff: "使用多种彩色纸（红/蓝/黄/绿各一片）的折叠，更活泼"
    use_when: "儿童/手工/趣味内容"
  - name: "暗纸版"
    diff: "bg 改为 #1a1a2e, surface 改为 #222，深色纸折叠"
    use_when: "现代/极简/科技折纸感"

css_snippets:
  keyframes: |
    /* 折纸不使用动画 — 静态的精确美 */
  effects: |
    .fold-triangle {
      width: 120px; height: 100px;
      clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
      background: linear-gradient(135deg, #d0c8b8, #b8b0a0);
    }
    .fold-light {
      background: linear-gradient(135deg, rgba(255,255,255,0.3) 0%, transparent 60%);
    }
    .crease-line {
      height: 1px;
      background: rgba(0,0,0,0.15);
      transform: rotate(-5deg);
    }
  patterns: |
    .paper-grain {
      background-color: #f5f0e8;
      background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='g'%3E%3CfeTurbulence baseFrequency='0.6' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)' opacity='0.03'/%3E%3C/svg%3E");
    }
```
