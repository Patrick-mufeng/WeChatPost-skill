# 03 · Editorial Bold · 社论杂志

```yaml
name: "社论杂志"
name_en: "EditorialBold"
keywords: [衬线, 大字标题, 戏剧对比, 杂志感, 权威]
best_for: [深度长文, 品牌故事, 行业分析, 人物专访]
emotional_tone: "严肃"

palette:
  bg: "#f5f0eb"
  surface: "#ffffff"
  primary: "#1a1a1a"
  accent: "#c41e3a"
  text: "#2a2a2a"
  muted: "#6b6b6b"

fonts:
  heading: "'Playfair Display', 'Noto Serif SC', 'Songti SC', serif"
  body: "'Source Serif Pro', 'Noto Serif SC', serif"

layout_2_35: "centered"
layout_1_1: "centered"

core_rules:
  - "标题使用超大衬线字体，字号 56-80px，占据画面 40-50% 高度"
  - "标题可以使用多行，每行长度不均等，形成节奏感"
  - "副标题使用斜体衬线（italic），字号 18-22px，颜色 muted"
  - "标题和正文之间必须有至少 40px 间距"
  - "accent 色仅用于极小点缀（一条下划线、一个引号标记），面积 ≤2%"
  - "整体布局完全居中，所有文字居中对齐"

negative_rules:
  - "禁止使用无衬线字体做标题"
  - "禁止使用发光、阴影等数字特效"
  - "禁止装饰性几何图形"
  - "禁止中英文混排时使用不同字体族"

variants:
  - name: "暗底版"
    diff: "bg 改为 #1a1a1a, text 改为 #e8e0d8, surface 改为 #222"
    use_when: "深色主题或夜间阅读场景"
  - name: "左对齐版"
    diff: "全部左对齐而非居中，标题靠左、正文紧随"
    use_when: "文章偏理性分析而非感性叙事"
  - name: "双色标题版"
    diff: "标题首字或关键词使用 accent 色，其余 primary"
    use_when: "标题中有强烈对比词汇（如'AI vs 人工'）"

css_snippets:
  keyframes: |
    /* 社论杂志不使用动画 */
  effects: |
    .editorial-title {
      font-size: clamp(48px, 6vw, 76px);
      font-weight: 900;
      line-height: 1.1;
      letter-spacing: -0.01em;
    }
    .editorial-subtitle {
      font-style: italic;
      color: #6b6b6b;
      font-size: 18px;
      margin-top: 32px;
      max-width: 480px;
    }
    .editorial-accent {
      display: inline-block;
      width: 40px;
      height: 3px;
      background: #c41e3a;
      margin: 20px 0;
    }
  patterns: |
    /* 无图案 */
```
