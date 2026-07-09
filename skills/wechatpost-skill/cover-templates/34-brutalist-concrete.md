# 34 · Brutalist Concrete · 混凝土粗野

```yaml
name: "混凝土粗野"
name_en: "BrutalistConcrete"
keywords: [水泥, 建筑, 粗野主义, 灰调, 体块, 城市]
best_for: [建筑/设计评论, 城市内容, 工业主题, 基础设施]
emotional_tone: "冷峻"

palette:
  bg: "#b8b4ac"
  surface: "#c8c4bc"
  primary: "#2a2826"
  accent: "#6b4e3d"
  text: "#1a1816"
  muted: "#7a7670"

fonts:
  heading: "'Archivo Black', 'PingFang SC', sans-serif"
  body: "'Space Mono', 'PingFang SC', monospace"

layout_2_35: "split"
layout_1_1: "framed"

core_rules:
  - "背景模拟水泥墙面：灰调底色 + 混凝土纹理（噪音 + 气泡点）"
  - "使用巨大矩形色块（灰/黑）分割画面，像建筑体块"
  - "标题使用极粗无衬线（Archivo Black），字号大且紧凑"
  - "所有元素形状为矩形——无圆角、无曲线"
  - "色彩限于灰阶：混凝土灰 + 炭黑 + 单一强调色（暗棕/锈色）"
  - "阴影也是硬的 box-shadow（无 blur），模拟建筑投影"

negative_rules:
  - "禁止使用圆角——建筑是直的"
  - "禁止使用渐变色"
  - "禁止曲线装饰——只有直线和矩形"
  - "禁止超过 3 种色相（灰+黑+棕锈）"
  - "禁止使用衬线字体"

variants:
  - name: "白水泥版"
    diff: "bg 改为 #e8e4e0, surface 改为 #f0ece8"
    use_when: "现代极简建筑/画廊"
  - name: "暗水泥版"
    diff: "bg 改为 #3a3836, text 改为 #c8c4bc"
    use_when: "夜景城市/工业/暗黑建筑"

css_snippets:
  keyframes: |
    /* 混凝土不使用动画 — 永恒的静止 */
  effects: |
    .concrete-texture {
      background-color: #b8b4ac;
      background-image: url("data:image/svg+xml,%3Csvg width='200' height='200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='0.65' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.06'/%3E%3C/svg%3E");
    }
    .concrete-block {
      background: #2a2826;
      box-shadow: 8px 8px 0 rgba(0,0,0,0.1);
    }
  patterns: |
    .rebar-line {
      height: 2px;
      background: rgba(107,78,61,0.4);
      width: 30%;
    }
```
