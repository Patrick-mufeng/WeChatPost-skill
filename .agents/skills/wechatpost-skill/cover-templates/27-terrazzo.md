# 27 · Terrazzo · 水磨石

```yaml
name: "水磨石"
name_en: "Terrazzo"
keywords: [斑点, 温暖, 现代, 活泼, 碎石, 极繁]
best_for: [生活方式, 家居设计, 手工艺, 现代品牌]
emotional_tone: "轻松"

palette:
  bg: "#faf5f0"
  surface: "#ffffff"
  primary: "#2c3e50"
  accent: "#e07a5f"
  text: "#1a1a2e"
  muted: "#8a7a70"

fonts:
  heading: "'Poppins', 'PingFang SC', sans-serif"
  body: "'Inter', 'PingFang SC', sans-serif"

layout_2_35: "centered"
layout_1_1: "centered"

core_rules:
  - "背景必须有水磨石斑点纹理：多个不同大小、颜色、透明度的圆形散布"
  - "斑点色：暖粉/灰/米/浅蓝，3-4 种色相，低饱和度"
  - "使用 CSS radial-gradient 或多个 div 散布圆形模拟碎石"
  - "标题使用现代几何无衬线（Poppins），圆润但不幼稚"
  - "文字区要有干净的白/浅色卡片作为'安全区'，与斑点背景形成对比"
  - "整体温暖、亲切，像走进一家有磨石地面的精品店"

negative_rules:
  - "禁止尖锐几何形——水磨石是圆润随机的"
  - "禁止高饱和色——斑点要柔和融入底色"
  - "禁止暗色背景——水磨石是明亮的"
  - "禁止整齐排列——斑点是随机散布的"
  - "禁止超过 5 种斑点色"

variants:
  - name: "深色磨石版"
    diff: "bg 改为 #1a1a2e，斑点改为浅亮的粉/蓝/白"
    use_when: "暗色主题/夜店/酒吧设计"
  - name: "单色磨石版"
    diff: "所有斑点同一色系（如全部粉系），更统一"
    use_when: "女性品牌/统一色调需求"

css_snippets:
  keyframes: |
    /* 水磨石不使用动画 */
  effects: |
    .terrazzo-chip {
      position: absolute;
      border-radius: 50%;
      opacity: 0.4;
      pointer-events: none;
    }
  patterns: |
    .terrazzo-bg {
      position: relative;
      overflow: hidden;
    }
    /* 斑点通过 JS 随机生成 15-25 个 div 散布，模拟碎石效果 */
```
