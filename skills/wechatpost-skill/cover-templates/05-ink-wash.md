# 05 · Ink Wash · 东方水墨

```yaml
name: "东方水墨"
name_en: "InkWash"
keywords: [水墨, 竖排, 印章, 留白, 传统]
best_for: [人文随笔, 传统文化, 诗词赏析, 哲学思考]
emotional_tone: "严肃"

palette:
  bg: "#f5f0e8"
  surface: "transparent"
  primary: "#1a0d08"
  accent: "#c43a30"
  text: "#3a2a1a"
  muted: "#8b6b4a"

fonts:
  heading: "'Noto Serif SC', 'Songti SC', 'KaiTi', serif"
  body: "'Noto Serif SC', 'KaiTi', serif"

layout_2_35: "left-column"
layout_1_1: "centered"

core_rules:
  - "标题使用竖排（writing-mode: vertical-rl），位于画面左侧"
  - "右侧大量留白，可放置一枚红色印章（圆形或方形 accent 色边框）"
  - "背景必须模拟宣纸纹理（微黄底色 + CSS 噪点叠加）"
  - "使用墨色浓淡变化：标题深黑，副标题中灰，装饰用淡墨"
  - "装饰元素仅限于：印章、墨线、笔触飞白"
  - "留白面积必须 ≥40%，不可填满"

negative_rules:
  - "禁止使用任何西式装饰（网格、几何形、渐变）"
  - "禁止使用无衬线字体"
  - "禁止高饱和颜色（除印章红外）"
  - "禁止内容区超过画面 60%"

variants:
  - name: "浓墨版"
    diff: "bg 改为 #1a0d08, text 改为 #e8d8c0，白字黑底仿拓片"
    use_when: "庄重、悲怆主题"
  - name: "青绿山水版"
    diff: "primary 改为 #2d5016, accent 改为 #8b5a2b，加入青绿色水彩晕染"
    use_when: "山水/田园/自然主题"

css_snippets:
  keyframes: |
    @keyframes inkDrop {
      0% { transform: scale(0); opacity: 0.6; }
      70% { transform: scale(1.1); opacity: 0.3; }
      100% { transform: scale(1); opacity: 0.15; }
    }
  effects: |
    .paper-texture {
      background-color: #f5f0e8;
      background-image: url("data:image/svg+xml,%3Csvg width='200' height='200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
    }
    .vertical-text {
      writing-mode: vertical-rl;
      text-orientation: mixed;
      letter-spacing: 6px;
    }
    .seal {
      width: 56px; height: 56px;
      border: 2px solid #c43a30;
      border-radius: 50%;
      color: #c43a30;
      display: flex; align-items: center; justify-content: center;
      transform: rotate(-8deg);
      font-size: 11px;
    }
  patterns: |
    .ink-splash {
      position: absolute;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(26,13,8,0.1), transparent 70%);
    }
```
