# 23 · Victorian · 维多利亚

```yaml
name: "维多利亚"
name_en: "Victorian"
keywords: [华丽, 暗金, 装饰, 学术, 古典, 繁复]
best_for: [品牌叙事, 古典文化, 文学评论, 高级定制]
emotional_tone: "激昂"

palette:
  bg: "#0d0a08"
  surface: "#1a1410"
  primary: "#c9a84c"
  accent: "#8b1a2b"
  text: "#e8dcc8"
  muted: "#8a7a60"

fonts:
  heading: "'Playfair Display', 'Noto Serif SC', 'Songti SC', serif"
  body: "'Crimson Text', 'Noto Serif SC', serif"

layout_2_35: "framed"
layout_1_1: "framed"

core_rules:
  - "四周必须有繁复的边框装饰（多重边框 + 角落花纹）"
  - "标题使用华丽衬线体，可加首字下沉或花体首字母"
  - "边框使用金色 + 暗红配色，模拟烫金工艺"
  - "标题上/下方有装饰性的花纹分隔线（非简单横线）"
  - "整体包裹感强——文字被框在华丽框架内"
  - "背景可用暗色木纹/皮质纹理"

negative_rules:
  - "禁止使用无衬线字体"
  - "禁止简化装饰——维多利亚就是繁复"
  - "禁止现代科技元素"
  - "禁止留白超过 30%"
  - "禁止使用冷色系"

variants:
  - name: "淡色版"
    diff: "bg 改为 #f5efe0, surface 改为 #faf5eb, text 改为 #2a1a0a"
    use_when: "茶话会/下午茶/女性古典主题"
  - name: "哥特版"
    diff: "accent 改为 #4a0a1a，装饰加入尖拱，更黑暗"
    use_when: "哥特文学/暗黑浪漫"

css_snippets:
  keyframes: |
    /* 维多利亚不使用动画 — 静态的庄严 */
  effects: |
    .victorian-frame {
      border: 2px solid rgba(201,168,76,0.4);
      box-shadow: inset 0 0 0 1px rgba(201,168,76,0.2), 0 0 0 6px rgba(201,168,76,0.08);
    }
    .ornamental-divider {
      height: 20px;
      background: repeating-linear-gradient(
        90deg, transparent 0px, #c9a84c 2px, transparent 4px, transparent 12px
      );
      background-repeat: repeat-x;
      background-position: center;
      background-size: 16px 2px;
    }
  patterns: |
    .filigree-corner {
      position: absolute;
      width: 40px; height: 40px;
      border: 1px solid rgba(201,168,76,0.5);
      border-radius: 2px;
    }
    /* 角落花纹用 CSS border-image 或 SVG background */
```
