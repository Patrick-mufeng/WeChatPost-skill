# 35 · Tropical Miami · 迈阿密热浪

```yaml
name: "迈阿密热浪"
name_en: "TropicalMiami"
keywords: [棕榈, 粉彩, 迈阿密, 80s, 度假, 夏日]
best_for: [旅行/度假, 夏日内容, 时尚潮流, 轻松品牌]
emotional_tone: "轻松"

palette:
  bg: "#ffeedd"
  surface: "#ffffff"
  primary: "#ff6b9d"
  accent: "#50c8b4"
  text: "#1a1a2e"
  muted: "#6a7a8a"

fonts:
  heading: "'Pacifico', 'PingFang SC', cursive"
  body: "'Montserrat', 'PingFang SC', sans-serif"

layout_2_35: "asymmetric-right"
layout_1_1: "centered"

core_rules:
  - "背景使用温暖粉彩底色（肉粉/奶油），装饰棕榈叶剪影"
  - "配色大胆：粉+青（teal）+奶油白，迈阿密装饰艺术配色"
  - "标题使用手写/草书字体（Pacifico），自由奔放"
  - "棕榈叶装饰使用 CSS clip-path 或 SVG 剪影，半透明叠加"
  - "画面右侧或左下放置棕榈叶，左侧留白给文字"
  - "整体氛围：80s迈阿密度假风，明快、热情、自由"

negative_rules:
  - "禁止暗色背景——迈阿密是阳光的"
  - "禁止衬线字体"
  - "禁止冷色系为主——必须是暖色调"
  - "禁止几何硬边——棕榈是曲线的"
  - "禁止超过 4 种颜色"

variants:
  - name: "日落版"
    diff: "bg 改为日落橙渐变，棕榈叶变为黑色剪影"
    use_when: "日落/傍晚/浪漫度假"
  - name: "霓虹夜版"
    diff: "bg 改为深紫，棕榈叶用霓虹粉色勾勒"
    use_when: "迈阿密夜生活/派对"

css_snippets:
  keyframes: |
    @keyframes palmSway {
      0%, 100% { transform: rotate(0deg); }
      50% { transform: rotate(3deg); }
    }
  effects: |
    .palm-frond {
      position: absolute;
      opacity: 0.2;
      pointer-events: none;
      transform-origin: bottom center;
      animation: palmSway 6s ease-in-out infinite;
    }
  patterns: |
    .art-deco-stripe {
      background: repeating-linear-gradient(
        90deg, #ff6b9d 0px, #ff6b9d 4px, #50c8b4 4px, #50c8b4 8px
      );
      height: 3px;
    }
```
