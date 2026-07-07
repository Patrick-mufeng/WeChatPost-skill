# 24 · Psychedelic · 迷幻60s

```yaml
name: "迷幻60s"
name_en: "Psychedelic"
keywords: [迷幻, 变形, 彩虹, 酸性, 60s, 致幻]
best_for: [音乐/艺术, 创意实验, 反文化, 节庆内容]
emotional_tone: "轻松"

palette:
  bg: "#1a0533"
  surface: "transparent"
  primary: "#ff00ff"
  accent: "#00ffcc"
  text: "#ffeedd"
  muted: "#a080c0"

fonts:
  heading: "'Monoton', 'PingFang SC', cursive"
  body: "'Comfortaa', 'PingFang SC', sans-serif"

layout_2_35: "centered"
layout_1_1: "centered"

core_rules:
  - "标题使用极度变形字体（Monoton / 波浪效果），文字扭曲或呈弧形排列"
  - "背景使用多个色相旋转的渐变叠加（conic-gradient + blend-mode）"
  - "颜色必须横跨全光谱：红橙黄绿蓝紫粉"
  - "装饰元素：同心波浪线、涡旋、液态变形椭圆"
  - "使用 filter: hue-rotate 动画（慢速 20-30s）创造呼吸感"
  - "文字可以有彩虹色 text-shadow 偏移"

negative_rules:
  - "禁止使用衬线字体"
  - "禁止使用黑白或低饱和——必须是全彩"
  - "禁止简单几何（方形/三角）——要有机流动形"
  - "禁止暗沉配色——即使暗底也要有高饱和色"

variants:
  - name: "暗化版"
    diff: "降低背景亮度，但保持色相饱和，更地下俱乐部感"
    use_when: "深夜派对/地下音乐"
  - name: "日出版"
    diff: "bg 改为暖色渐变（黄→橙→粉），模仿日出迷幻"
    use_when: "清晨派对/正面能量"

css_snippets:
  keyframes: |
    @keyframes acidTrip {
      0% { filter: hue-rotate(0deg); }
      100% { filter: hue-rotate(360deg); }
    }
    @keyframes waveMove {
      0% { transform: translateX(0) scaleY(1); }
      50% { transform: translateX(-10%) scaleY(1.5); }
      100% { transform: translateX(0) scaleY(1); }
    }
  effects: |
    .psychedelic-bg {
      background: conic-gradient(
        from 0deg, #ff006e, #ff6b00, #ffd000, #00ff88, #00a3ff, #7b2ff7, #ff006e
      );
      opacity: 0.3;
      animation: acidTrip 25s linear infinite;
    }
    .warp-text {
      transform: skew(-5deg);
      text-shadow: 3px 0 #ff006e, -3px 0 #00a3ff;
    }
  patterns: |
    .concentric-waves {
      border: 3px solid;
      border-radius: 50% / 30%;
      border-color: #ff00ff #00ffcc #ffd000 #ff006e;
    }
```
