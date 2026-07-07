# 06 · Memphis Design · 孟菲斯

```yaml
name: "孟菲斯"
name_en: "MemphisDesign"
keywords: [几何, 撞色, 波点, 童趣, 80s, 玩味]
best_for: [创意分享, 年轻品牌, 设计话题, 娱乐内容]
emotional_tone: "轻松"

palette:
  bg: "#fdf6e3"
  surface: "#ffffff"
  primary: "#e63946"
  accent: "#457b9d"
  text: "#1d3557"
  muted: "#6c757d"

fonts:
  heading: "'Fredoka One', 'PingFang SC', cursive"
  body: "'Nunito', 'PingFang SC', sans-serif"

layout_2_35: "asymmetric-right"
layout_1_1: "centered"

core_rules:
  - "背景使用柔和底色（米白/淡粉），上面叠加几何形状装饰"
  - "装饰几何形状：圆形、三角形、波浪线、波点，随机散布但视觉平衡"
  - "几何装饰使用 3-4 种高饱和色（红/蓝/黄/珊瑚），透明度 0.3-0.6"
  - "标题使用圆体/趣味体，字号 42-56px"
  - "所有元素不允许使用直线——用曲线、波浪、圆角代替"
  - "标签使用 pill 形状（border-radius: 40px）"

negative_rules:
  - "禁止使用衬线字体"
  - "禁止使用暗色背景（必须是亮色/粉彩系）"
  - "禁止使用直角边框"
  - "禁止单一的极简配色（至少 3 种颜色）"
  - "禁止使用阴影或发光效果"

variants:
  - name: "暗夜孟菲斯版"
    diff: "bg 改为 #1a1a2e, 几何形状使用荧光色（#ff6b6b, #4ecdc4, #ffe66d）"
    use_when: "夜店/派对/音乐相关内容"
  - name: "柔和版"
    diff: "几何形状改用较低饱和度的粉彩色（#f4a261, #e9c46a, #a8dadc）"
    use_when: "母婴/女性/温柔内容"

css_snippets:
  keyframes: |
    @keyframes wiggle {
      0%, 100% { transform: rotate(0deg); }
      25% { transform: rotate(2deg); }
      75% { transform: rotate(-2deg); }
    }
  effects: |
    .memphis-shape {
      position: absolute;
      opacity: 0.5;
      pointer-events: none;
    }
    .circle { border-radius: 50%; }
    .triangle {
      width: 0; height: 0;
      border-left: 20px solid transparent;
      border-right: 20px solid transparent;
      border-bottom: 35px solid currentColor;
    }
  patterns: |
    .dots-pattern {
      background-image: radial-gradient(circle, rgba(230,57,70,0.3) 2px, transparent 2px);
      background-size: 24px 24px;
    }
    .squiggle {
      border: 3px solid transparent;
      border-radius: 50%/100%;
      border-bottom-color: var(--accent);
      border-top-color: var(--primary);
    }
```
