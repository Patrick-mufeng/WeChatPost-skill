# 01 · Swiss Minimal · 瑞士极简

```yaml
name: "瑞士极简"
name_en: "SwissMinimal"
keywords: [黑白, 无衬线, 几何, 留白, 网格]
best_for: [商业分析, 产品文档, 深度思考, 品牌宣言]
emotional_tone: "冷峻"

palette:
  bg: "#fafafa"
  surface: "#ffffff"
  primary: "#111111"
  accent: "#e63946"
  text: "#1a1a1a"
  muted: "#888888"

fonts:
  heading: "'Inter', 'Helvetica Neue', 'PingFang SC', sans-serif"
  body: "'Inter', 'Helvetica Neue', 'PingFang SC', sans-serif"

layout_2_35: "asymmetric-right"
layout_1_1: "framed"

core_rules:
  - "大面积留白：背景纯白或极浅灰，内容区不超过50%面积"
  - "标题使用极粗字重（700-900），字号 52-68px，字母间距 -0.02em"
  - "分割线使用 1px 实线，颜色为 muted，宽度不超过标题的80%"
  - "正文颜色使用 muted（#888），与标题形成强烈灰阶对比"
  - "仅使用 accent 色作为极端点缀（如一个圆点、一条下划线），占比 ≤1% 画面"

negative_rules:
  - "禁止使用任何渐变"
  - "禁止使用阴影或发光效果"
  - "禁止使用超过 2 种字重"
  - "禁止装饰性图案（图标、纹理、网格线全部禁止）"

variants:
  - name: "暗底版"
    diff: "bg 改为 #111，text 改为 #eee，surface 改为 #1a1a1a"
    use_when: "需要更严肃、更有力量感的表达"
  - name: "蓝色强调版"
    diff: "accent 改为 #2563eb，其余不变"
    use_when: "科技或商务内容需要一点品牌色"
  - name: "双栏版"
    diff: "layout 改为 split，左侧标题右侧正文，中间 1px 竖线"
    use_when: "标题和描述长度接近，适合均衡构图"

css_snippets:
  keyframes: |
    /* 瑞士极简不使用动画 */
  effects: |
    .swiss-rule {
      width: 60%;
      height: 1px;
      background: #888;
      margin: 24px 0;
    }
  patterns: |
    /* 无图案 — 极简的核心是无 */
```
