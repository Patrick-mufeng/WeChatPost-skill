# 17 · Pop Art · 波普艺术

```yaml
name: "波普艺术"
name_en: "PopArt"
keywords: [波普, 沃霍尔, 半调, 漫画, 高饱和, 流行]
best_for: [娱乐内容, 流行文化, 年轻受众, 社交媒体]
emotional_tone: "轻松"

palette:
  bg: "#ffe600"
  surface: "#ffffff"
  primary: "#e63946"
  accent: "#1d7ab5"
  text: "#111111"
  muted: "#555555"

fonts:
  heading: "'Bebas Neue', 'Anton', 'PingFang SC', sans-serif"
  body: "'Archivo Black', 'PingFang SC', sans-serif"

layout_2_35: "centered"
layout_1_1: "framed"

core_rules:
  - "背景使用 2-3 个高饱和色块分割（非渐变，硬切）"
  - "标题使用极粗无衬线压缩体（Bebas Neue / Anton），字号大且紧凑"
  - "必须使用半调网点纹理（halftone dots pattern）覆盖部分区域"
  - "配色极度饱和：正黄、正红、正蓝——没有中间色调"
  - "装饰：对话气泡、Ben-Day dots、粗黑轮廓线"
  - "标题可以有多层轮廓（-webkit-text-stroke）模拟漫画字效"

negative_rules:
  - "禁止使用渐变色——全部纯色块"
  - "禁止使用衬线字体"
  - "禁止使用暗沉或柔和的颜色"
  - "禁止超过 5 种颜色"
  - "禁止无装饰——波普就是要"满""

variants:
  - name: "粉红版"
    diff: "bg 改为 #ff6b9d，主色调改为粉+紫+黄"
    use_when: "女性向/恋爱/浪漫内容"
  - name: "四格版"
    diff: "画面切为 2×2 四格，每格不同高饱和底色"
    use_when: "对比/选择/多主题内容"

css_snippets:
  keyframes: |
    @keyframes popIn {
      0% { transform: scale(0.8); opacity: 0; }
      70% { transform: scale(1.05); }
      100% { transform: scale(1); opacity: 1; }
    }
  effects: |
    .comic-outline {
      -webkit-text-stroke: 3px #111;
      paint-order: stroke fill;
    }
    .speech-bubble {
      background: #fff;
      border: 3px solid #111;
      border-radius: 20px;
      position: relative;
    }
    .speech-bubble::after {
      content: ''; position: absolute;
      bottom: -15px; left: 30px;
      width: 0; height: 0;
      border-left: 15px solid transparent;
      border-right: 15px solid transparent;
      border-top: 15px solid #111;
    }
  patterns: |
    .halftone {
      background-image: radial-gradient(circle, #e63946 2px, transparent 2px);
      background-size: 12px 12px;
    }
    .benday-yellow {
      background-image: radial-gradient(circle, #ffe600 3px, transparent 3px);
      background-size: 16px 16px;
    }
```
