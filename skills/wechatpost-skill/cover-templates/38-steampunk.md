# 38 · Steampunk · 蒸汽朋克

```yaml
name: "蒸汽朋克"
name_en: "Steampunk"
keywords: [蒸汽朋克, 黄铜, 齿轮, 维多利亚科幻, 工业革命]
best_for: [科幻文学, 手工艺, 复古科技, 创客/DIY]
emotional_tone: "激昂"

palette:
  bg: "#1a1410"
  surface: "#2a2018"
  primary: "#d4a84b"
  accent: "#c44a20"
  text: "#e8dcc0"
  muted: "#8a7050"

fonts:
  heading: "'Playfair Display', 'Cinzel', 'Songti SC', serif"
  body: "'Crimson Text', 'Noto Serif SC', serif"

layout_2_35: "framed"
layout_1_1: "framed"

core_rules:
  - "背景使用深棕色/暗木色，装饰用黄铜色齿轮和铆钉"
  - "边框模拟金属板：暗色 + 铆钉圆点排列 + 黄铜色边框"
  - "标题使用衬线体，金色渐变，模拟蚀刻金属牌"
  - "装饰元素：齿轮（CSS conic-gradient 或 SVG）、铆钉、蒸汽管"
  - "四角用圆形铆钉（border-radius: 50% + box-shadow）装饰"
  - "整体像维多利亚时代的蒸汽机械面板"

negative_rules:
  - "禁止使用无衬线字体"
  - "禁止使用冷色系（蓝/绿/紫）——只有黄铜/棕/暗红"
  - "禁止简约装饰——蒸汽朋克是繁复的"
  - "禁止圆角——金属板是直的"
  - "禁止现代科技元素（发光、全息）"

variants:
  - name: "铜绿版"
    diff: "加入铜绿色（#4a8a6a），模拟生锈铜器的铜绿"
    use_when: "古旧/废弃/考古主题"
  - name: "白银版"
    diff: "黄铜改为银色，整体更冷，像白银时代的科幻"
    use_when: "蒸汽朋克中的'白领'科幻"

css_snippets:
  keyframes: |
    @keyframes gearRotate {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
  effects: |
    .brass-text {
      background: linear-gradient(135deg, #d4a84b, #f5d77a, #c49a2c);
      -webkit-background-clip: text; background-clip: text;
      color: transparent;
    }
    .metal-plate {
      background: linear-gradient(180deg, #2a2018, #1a1410);
      border: 2px solid rgba(212,168,75,0.4);
      box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
    }
    .rivet {
      width: 8px; height: 8px;
      background: radial-gradient(circle at 40% 40%, #d4a84b, #8a6040);
      border-radius: 50%;
      box-shadow: 0 1px 2px rgba(0,0,0,0.4);
    }
  patterns: |
    .gear {
      position: absolute;
      width: 60px; height: 60px;
      border: 4px dashed rgba(212,168,75,0.3);
      border-radius: 50%;
      animation: gearRotate 20s linear infinite;
    }
```
