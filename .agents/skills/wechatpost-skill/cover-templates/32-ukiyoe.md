# 32 · Ukiyo-e · 浮世绘

```yaml
name: "浮世绘"
name_en: "Ukiyoe"
keywords: [浮世绘, 海浪, 木版画, 靛蓝, 日本, 北斋]
best_for: [日本文化, 传统艺术, 历史内容, 东方美学]
emotional_tone: "严肃"

palette:
  bg: "#e8dcc8"
  surface: "transparent"
  primary: "#1a2a5e"
  accent: "#c44a20"
  text: "#1a1a2e"
  muted: "#6a5a4a"

fonts:
  heading: "'Noto Serif SC', 'Songti SC', serif"
  body: "'Noto Sans SC', 'PingFang SC', sans-serif"

layout_2_35: "asymmetric-right"
layout_1_1: "centered"

core_rules:
  - "背景使用暖米色（仿木版画纸），装饰使用靛蓝色海浪纹样"
  - "必须有浮世绘风格的海浪装饰（多层弧形叠加 + 白色浪尖泡沫点）"
  - "配色克制：靛蓝 + 橘红（朱色）+ 纸米色，经典浮世绘三色"
  - "标题使用衬线体，可以竖排（writing-mode: vertical-rl）"
  - "色调平涂（无渐变），模拟木版画的色块感"
  - "右侧可留富士山剪影或松枝剪影"

negative_rules:
  - "禁止使用渐变色——木版画是纯色平涂"
  - "禁止使用无衬线字体做标题"
  - "禁止超过 4 种颜色"
  - "禁止现代科技元素"
  - "禁止高饱和荧光色"

variants:
  - name: "雪景版"
    diff: "bg 改为 #d0d8e0，加入雪花点，蓝色调为主"
    use_when: "冬季/雪景/静谧主题"
  - name: "红富士版"
    diff: "加入大面积朱红色块（赤富士风格），更壮丽"
    use_when: "壮丽/日出/力量主题"

css_snippets:
  keyframes: |
    /* 浮世绘不使用动画 — 永恒的静态美 */
  effects: |
    .wave-arc {
      position: absolute;
      border: 2px solid #1a2a5e;
      border-radius: 50% / 80%;
      border-bottom: none;
      border-left: none;
      border-right: none;
    }
    .foam-dot {
      position: absolute;
      width: 4px; height: 4px;
      background: #e8dcc8;
      border-radius: 50%;
      box-shadow: 0 0 2px #e8dcc8;
    }
  patterns: |
    .seigaiha {
      background:
        radial-gradient(circle at 50% 0, transparent 40%, rgba(26,42,94,0.15) 40%, rgba(26,42,94,0.15) 60%, transparent 60%);
      background-size: 30px 30px;
    }
```
