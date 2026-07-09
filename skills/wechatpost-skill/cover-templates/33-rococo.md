# 33 · Rococo · 洛可可

```yaml
name: "洛可可"
name_en: "Rococo"
keywords: [法式, 粉金, 卷草, 华丽, 浪漫, 宫廷]
best_for: [女性品牌, 婚礼内容, 奢华生活, 法式美学]
emotional_tone: "温暖"

palette:
  bg: "#faf0f5"
  surface: "#fff5f8"
  primary: "#c9a84c"
  accent: "#e8a0b0"
  text: "#3a2030"
  muted: "#a08090"

fonts:
  heading: "'Playfair Display', 'Songti SC', serif"
  body: "'Cormorant Garamond', 'Noto Serif SC', serif"

layout_2_35: "framed"
layout_1_1: "framed"

core_rules:
  - "背景使用淡粉色/奶油色，整体轻盈浪漫"
  - "四周使用华丽卷草纹边框（使用 border-image 或 CSS 花纹）"
  - "配色：金色 + 粉色 + 奶油白，三色为主"
  - "标题用衬线斜体，优雅纤细"
  - "边框装饰要繁复：多圈线框 + 角落花卉"
  - "点缀小花朵、蝴蝶结、爱心等小型装饰"

negative_rules:
  - "禁止使用无衬线粗体——洛可可是纤细优雅的"
  - "禁止暗色背景"
  - "禁止几何直线装饰——全部要用曲线和花卉"
  - "禁止亮色/荧光色"
  - "禁止现代科技元素"

variants:
  - name: "凡尔赛金版"
    diff: "金色比例增大，粉色退为点缀，bg 改为奶油金"
    use_when: "更正式/宫廷/奢华主题"
  - name: "蒂芙尼蓝版"
    diff: "粉色改为蒂芙尼蓝（#81d8d0），更清新"
    use_when: "珠宝/奢侈品/清新法式"

css_snippets:
  keyframes: |
    /* 洛可可不用动画 — 静谧的美 */
  effects: |
    .rococo-frame {
      border: 1px solid rgba(201,168,76,0.3);
      box-shadow: inset 0 0 0 4px rgba(201,168,76,0.08), inset 0 0 0 8px rgba(201,168,76,0.04);
    }
    .floral-corner {
      position: absolute;
      width: 50px; height: 50px;
      border: 1px solid rgba(201,168,76,0.3);
      border-radius: 50% 50% 0 50%;
      transform: rotate(45deg);
    }
  patterns: |
    .damask-pattern {
      background-image:
        radial-gradient(circle at 50% 50%, rgba(232,160,176,0.1) 2px, transparent 2px);
      background-size: 20px 20px;
    }
```
