# 20 · Newspaper · 报纸印刷

```yaml
name: "报纸印刷"
name_en: "Newspaper"
keywords: [报纸, 印刷, 多栏, 衬线, 新闻纸, 经典]
best_for: [深度报道, 行业分析, 时事评论, 严肃内容]
emotional_tone: "严肃"

palette:
  bg: "#f5f0e5"
  surface: "#fafaf7"
  primary: "#1a1a1a"
  accent: "#8b0000"
  text: "#2a2a2a"
  muted: "#5a5a5a"

fonts:
  heading: "'Playfair Display', 'Noto Serif SC', 'Songti SC', serif"
  body: "'PT Serif', 'Noto Serif SC', serif"

layout_2_35: "split"
layout_1_1: "top-down"

core_rules:
  - "背景模拟新闻纸：微黄色调 + 轻微纹理"
  - "标题使用超大衬线体，跨越多栏（类似报纸头版头条）"
  - "正文区使用 2-3 栏布局（CSS columns），栏间用细竖线分隔"
  - "标题下方必须有细横线（hairline rule），报纸标志性元素"
  - "画面顶部可以有报纸名称 + 日期行（小号全部大写）"
  - "底部有装饰性的小字/页脚线"

negative_rules:
  - "禁止使用无衬线字体做标题"
  - "禁止使用暗色背景——报纸是白纸黑字"
  - "禁止使用渐变或阴影——印刷品是平的"
  - "禁止超过 3 种颜色（黑白红经典报色）"
  - "禁止圆形装饰——报纸排版是方正的"

variants:
  - name: "号外版"
    diff: "标题占画面 70%，超大字，正文缩减到一句话，紧急感"
    use_when: "突发/重磅/独家内容"
  - name: "财经版"
    diff: "加入股票行情小字条、数据表格装饰，accent 改为 #003366 深蓝"
    use_when: "财经/数据/报表内容"

css_snippets:
  keyframes: |
    /* 报纸不使用动画 */
  effects: |
    .news-headline {
      font-size: clamp(42px, 5vw, 68px);
      font-weight: 900;
      line-height: 1.1;
      letter-spacing: -0.01em;
    }
    .hairline-rule {
      width: 100%; height: 1px;
      background: #1a1a1a;
      margin: 8px 0;
    }
    .news-columns {
      column-count: 2;
      column-gap: 24px;
      column-rule: 1px solid #d0c8b8;
    }
  patterns: |
    .newspaper-texture {
      background-color: #f5f0e5;
      background-image: url("data:image/svg+xml,%3Csvg width='200' height='200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='0.8' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
    }
    .dateline {
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 2px;
      color: #5a5a5a;
      border-top: 1px solid #1a1a1a;
      padding-top: 8px;
    }
```
