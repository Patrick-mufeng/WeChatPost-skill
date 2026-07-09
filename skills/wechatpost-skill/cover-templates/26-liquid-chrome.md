# 26 · Liquid Chrome · 液态金属

```yaml
name: "液态金属"
name_en: "LiquidChrome"
keywords: [金属, 液态, 镜面, 银铬, 未来工业, 反射]
best_for: [未来科技, 工业设计, 高端制造, 金属感品牌]
emotional_tone: "冷峻"

palette:
  bg: "#111118"
  surface: "linear-gradient metallic"
  primary: "#e8e8f0"
  accent: "#a0b8e0"
  text: "#e0e0e8"
  muted: "#6a6a80"

fonts:
  heading: "'Orbitron', 'Exo', 'PingFang SC', sans-serif"
  body: "'Rajdhani', 'PingFang SC', sans-serif"

layout_2_35: "centered"
layout_1_1: "centered"

core_rules:
  - "标题使用金属渐变（银色/铬色线性渐变 + background-clip: text）"
  - "背景使用深色，配合金属反射光条（白色半透明长条 + 模糊）"
  - "装饰元素：流动的液态金属形状（使用 SVG 或 CSS 不规则形状 + 金属渐变填充）"
  - "核心视觉是'镜面反射'——光在金属表面流动的错觉"
  - "使用 linear-gradient 多层叠加模拟金属光泽: 银→白→灰→银"
  - "边框使用 1px 半透明白色，像金属的边缘"

negative_rules:
  - "禁止使用暖色——金属感必须偏冷"
  - "禁止使用粗糙纹理——金属是光滑的"
  - "禁止圆角——工业金属是锐利的"
  - "禁止纯色标题——必须是金属渐变"
  - "禁止暗沉——即使深色底，金属字必须亮"

variants:
  - name: "黄金版"
    diff: "金属色改为金色系（#d4af37 → #f5d77a → #c6963a）"
    use_when: "奢侈工业品/金饰/高端制造"
  - name: "钛金版"
    diff: "金属色改为钛色（#b0b8c0 → #d8e0e8 → #889098），更冷峻"
    use_when: "航空/精密仪器/硬核工业"

css_snippets:
  keyframes: |
    @keyframes liquidFlow {
      0% { background-position: -200% center; }
      100% { background-position: 200% center; }
    }
  effects: |
    .chrome-text {
      background: linear-gradient(
        135deg, #889098, #e8e8f0 20%, #a0b8e0 40%, #ffffff 50%, #a0b8e0 60%, #e8e8f0 80%, #889098
      );
      background-size: 200% auto;
      -webkit-background-clip: text; background-clip: text;
      color: transparent;
      animation: liquidFlow 4s linear infinite;
    }
    .reflection-beam {
      position: absolute;
      width: 3px; height: 80%;
      background: linear-gradient(180deg, transparent, rgba(255,255,255,0.4), transparent);
      filter: blur(8px);
      transform: skewX(-15deg);
    }
  patterns: |
    .metal-brushed {
      background: repeating-linear-gradient(
        90deg, transparent, transparent 1px, rgba(255,255,255,0.02) 1px, rgba(255,255,255,0.02) 2px
      );
    }
```
