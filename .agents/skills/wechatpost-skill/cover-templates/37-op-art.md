# 37 · Op Art · 视幻艺术

```yaml
name: "视幻艺术"
name_en: "OpArt"
keywords: [错视, 黑白, 波纹, 视觉, 图案, 欧普]
best_for: [设计前沿, 视觉实验, 心理学内容, 现代艺术]
emotional_tone: "冷峻"

palette:
  bg: "#ffffff"
  surface: "#f8f8f8"
  primary: "#111111"
  accent: "#111111"
  text: "#111111"
  muted: "#888888"

fonts:
  heading: "'Montserrat', 'Inter', 'PingFang SC', sans-serif"
  body: "'Inter', 'PingFang SC', sans-serif"

layout_2_35: "centered"
layout_1_1: "centered"

core_rules:
  - "背景使用黑白几何图案制造视幻效果：同心圆、棋盘格、波纹线"
  - "图案区域与文字区域需区分——文字放在干净的白色/黑色卡片上"
  - "使用 repeating-* CSS 背景创建密集的几何图案"
  - "配色严格黑白灰（可包含一个最小的高亮色，但通常不需要）"
  - "图案可以使用 moire 效果（两个不同角度的格线叠加）"
  - "整体像 Bridget Riley 的画作——视觉冲击、令人眩晕"

negative_rules:
  - "禁止使用彩色——欧普艺术是黑白的"
  - "禁止使用渐变——要硬边图案"
  - "禁止使用衬线字体"
  - "禁止圆角——图案是锐利的"
  - "禁止留白过多——图案要密集"

variants:
  - name: "彩色版"
    diff: "加入一个强调色（如电蓝），部分图案使用该色"
    use_when: "需要一点颜色的现代感"
  - name: "暗底版"
    diff: "bg 改为 #111, 图案改为白色线条，文字改为白色"
    use_when: "更神秘/太空/电子感"

css_snippets:
  keyframes: |
    @keyframes moireShift {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(2deg); }
    }
  effects: |
    .op-stripes {
      background: repeating-linear-gradient(
        0deg, #111 0px, #111 3px, #fff 3px, #fff 6px
      );
    }
    .op-checkerboard {
      background-image:
        linear-gradient(45deg, #111 25%, transparent 25%),
        linear-gradient(-45deg, #111 25%, transparent 25%),
        linear-gradient(45deg, transparent 75%, #111 75%),
        linear-gradient(-45deg, transparent 75%, #111 75%);
      background-size: 20px 20px;
    }
  patterns: |
    .concentric {
      background: repeating-radial-gradient(
        circle at center, #111 0px, #111 2px, #fff 2px, #fff 4px
      );
    }
    .moire-layer1 {
      background: repeating-linear-gradient(0deg, transparent, transparent 2px, #111 2px, #111 3px);
    }
    .moire-layer2 {
      background: repeating-linear-gradient(3deg, transparent, transparent 2px, #111 2px, #111 3px);
    }
```
