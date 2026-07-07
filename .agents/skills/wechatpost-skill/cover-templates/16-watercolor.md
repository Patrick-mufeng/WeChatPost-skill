# 16 · Watercolor · 水彩渲染

```yaml
name: "水彩渲染"
name_en: "Watercolor"
keywords: [水彩, 渲染, 柔和, 手绘, 艺术, 晕染]
best_for: [艺术随笔, 旅行游记, 诗歌, 情感表达]
emotional_tone: "温暖"

palette:
  bg: "#faf8f4"
  surface: "transparent"
  primary: "#2c3e50"
  accent: "#e07a5f"
  text: "#3a3a3a"
  muted: "#8a7a6a"

fonts:
  heading: "'Caveat', 'Ma Shan Zheng', 'KaiTi', cursive"
  body: "'Quicksand', 'PingFang SC', sans-serif"

layout_2_35: "asymmetric-right"
layout_1_1: "centered"

core_rules:
  - "背景必须有水彩晕染色斑（不规则椭圆，使用 CSS radial-gradient + blur）"
  - "水彩色斑使用 2-3 种柔和颜色（粉/黄/蓝），透明度 0.2-0.4，blur: 40-80px"
  - "标题使用手写/草书字体（Caveat / 马山正 / 楷体）"
  - "文字周围可以模拟水彩渗边效果（多重 box-shadow 微偏移）"
  - "整体氛围像水彩纸上的画作：湿润、柔和、透明"
  - "装饰元素：水渍斑点、笔触纹理、飞溅小点"

negative_rules:
  - "禁止使用饱和色——所有颜色必须像掺了水"
  - "禁止使用锐利边缘（圆角 ≥ 12px）"
  - "禁止使用几何图形（方形/三角形）"
  - "禁止暗色背景"
  - "禁止等宽字体"

variants:
  - name: "深色水彩版"
    diff: "bg 改为 #1a1a2e，水彩斑改用深蓝深紫，文字改为浅色"
    use_when: "夜晚/梦境/忧郁主题"
  - name: "花卉水彩版"
    diff: "水彩斑做成花朵形状（多个径向渐变叠加），颜色更丰富"
    use_when: "花园/春天/女性主题"

css_snippets:
  keyframes: |
    @keyframes washSpread {
      0% { transform: scale(0.8); opacity: 0; }
      100% { transform: scale(1); opacity: 0.3; }
    }
  effects: |
    .watercolor-wash {
      position: absolute;
      border-radius: 45% 55% 60% 40% / 50% 45% 55% 50%;
      filter: blur(60px);
      opacity: 0.25;
      pointer-events: none;
    }
    .wet-edge {
      box-shadow:
        0 0 0 3px rgba(224,122,95,0.05),
        0 0 0 6px rgba(224,122,95,0.03),
        0 0 0 10px rgba(224,122,95,0.01);
    }
  patterns: |
    .splatter-dot {
      position: absolute;
      border-radius: 50%;
      background: rgba(224,122,95,0.15);
      filter: blur(2px);
    }
```
