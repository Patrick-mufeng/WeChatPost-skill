# 18 · Wabi-Sabi · 侘寂美学

```yaml
name: "侘寂美学"
name_en: "WabiSabi"
keywords: [素朴, 不对称, 留白, 残缺, 枯山水, 禅]
best_for: [生活哲学, 慢生活, 极简主义, 心灵成长]
emotional_tone: "严肃"

palette:
  bg: "#e8e0d5"
  surface: "transparent"
  primary: "#4a3f35"
  accent: "#8b7355"
  text: "#3a3028"
  muted: "#9a8a7a"

fonts:
  heading: "'Noto Serif SC', 'Songti SC', serif"
  body: "'Noto Sans SC', 'PingFang SC', sans-serif"

layout_2_35: "asymmetric-right"
layout_1_1: "centered"

core_rules:
  - "背景模拟粗糙纸或土墙纹理（微噪点 + 不均匀底色）"
  - "大面积留白——内容面积 ≤ 40%"
  - "文字故意不居中：偏移到一侧，另一侧完全空白"
  - "装饰极致简约：一条细线、一个小圆、一个淡色块"
  - "色板全部来自自然：土色、石色、木色——无人工色"
  - "字体用衬线，字间距稍大（letter-spacing: 1-2px），体现静气"

negative_rules:
  - "禁止对称布局"
  - "禁止高饱和色——全部以大地色系为基调"
  - "禁止超过 2 种装饰元素"
  - "禁止使用无衬线粗体做标题"
  - "禁止使用任何动效——侘寂是静止的"

variants:
  - name: "暗调侘寂版"
    diff: "bg 改为 #2a2520, text 改为 #d0c8b8"
    use_when: "夜晚/静谧/内省主题"
  - name: "陶土版"
    diff: "bg 加入红陶色暖调（#c4a882），模拟手工陶器质感"
    use_when: "手工艺/陶艺/匠心主题"

css_snippets:
  keyframes: |
    /* 侘寂不使用动画 — 静的本质 */
  effects: |
    .wabi-texture {
      background-color: #e8e0d5;
      background-image: url("data:image/svg+xml,%3Csvg width='300' height='300' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='0.5' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
    }
    .wabi-line {
      width: 40px; height: 1px;
      background: #8b7355;
      opacity: 0.6;
    }
  patterns: |
    .ensō {
      width: 60px; height: 60px;
      border: 2px solid rgba(74,63,53,0.3);
      border-radius: 50%;
      clip-path: circle(50% at 52% 48%);
    }
```
