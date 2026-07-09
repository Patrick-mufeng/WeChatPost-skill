# 31 · Constructivist · 构成主义

```yaml
name: "构成主义"
name_en: "Constructivist"
keywords: [苏联, 红色, 对角线, 宣传画, 几何, 力量]
best_for: [社会评论, 宣言, 政治/历史, 激励内容]
emotional_tone: "激昂"

palette:
  bg: "#e63946"
  surface: "#111111"
  primary: "#ffffff"
  accent: "#111111"
  text: "#ffffff"
  muted: "#f0c0c0"

fonts:
  heading: "'Anton', 'Oswald', 'PingFang SC', sans-serif"
  body: "'Roboto Condensed', 'PingFang SC', sans-serif"

layout_2_35: "diagonal"
layout_1_1: "centered"

core_rules:
  - "配色仅用红+黑+白，非常强烈和直接"
  - "使用对角线构图——文字沿 15-30° 斜线排列"
  - "标题使用极粗压缩无衬线体（Anton），字号巨大"
  - "背景分割：红底为主 + 黑色几何斜面"
  - "装饰元素：粗黑线、五角星、齿轮、斜条纹"
  - "文字间距小、压缩感强，口号式的视觉冲击"

negative_rules:
  - "禁止使用红黑白以外的颜色"
  - "禁止使用衬线字体"
  - "禁止圆角或柔和过渡"
  - "禁止小字——全部要粗大有力"
  - "禁止装饰性花纹——要工业感"

variants:
  - name: "黑白版"
    diff: "bg 改为 #f0f0f0，文字黑色，强调色保持红色"
    use_when: "需要更冷静的表达"
  - name: "暗红版"
    diff: "bg 改为 #8b0000（暗红），更庄重"
    use_when: "历史/战争/严肃政治"

css_snippets:
  keyframes: |
    /* 构成主义不使用动画 — 静止的力量 */
  effects: |
    .construct-diagonal {
      transform: skewY(-5deg);
    }
    .bold-stripe {
      height: 8px;
      background: #111;
      width: 100%;
    }
    .star {
      width: 0; height: 0;
      border-left: 15px solid transparent;
      border-right: 15px solid transparent;
      border-bottom: 25px solid #fff;
      position: relative;
    }
  patterns: |
    .diagonal-bg {
      background: repeating-linear-gradient(
        135deg, transparent, transparent 20px, rgba(17,17,17,0.1) 20px, rgba(17,17,17,0.1) 40px
      );
    }
```
