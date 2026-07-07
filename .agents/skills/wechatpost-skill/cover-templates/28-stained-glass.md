# 28 · Stained Glass · 彩绘玻璃

```yaml
name: "彩绘玻璃"
name_en: "StainedGlass"
keywords: [彩色玻璃, 哥特, 宝石色, 神圣, 对称, 铅线]
best_for: [宗教/哲学, 文化遗产, 精神成长, 艺术历史]
emotional_tone: "激昂"

palette:
  bg: "#0a0a14"
  surface: "transparent"
  primary: "#c9a84c"
  accent: "#8b1a2b"
  text: "#f0e6d0"
  muted: "#6a5a8a"

fonts:
  heading: "'Cinzel', 'Noto Serif SC', 'Songti SC', serif"
  body: "'Cormorant Garamond', 'Noto Serif SC', serif"

layout_2_35: "framed"
layout_1_1: "framed"

core_rules:
  - "背景使用深暗色，封面中心或两侧有彩绘玻璃式的色块区域"
  - "色块之间用深色'铅线'（2-3px 暗边框）分隔，形成花窗效果"
  - "颜色使用宝石色系：红宝石、蓝宝石、祖母绿、紫水晶、金色"
  - "色块有半透明感（opacity 0.7-0.85），仿佛光线透过来"
  - "整体构图对称或放射状，模仿玫瑰窗（rose window）"
  - "文字放在中心或下方，被彩色光晕包围"

negative_rules:
  - "禁止不对称布局"
  - "禁止使用无衬线字体"
  - "禁止使用粉彩色——必须是深宝石色"
  - "禁止纯色块不透明——玻璃必须有透光感"
  - "禁止现代科技元素"

variants:
  - name: "玫瑰窗版"
    diff: "使用圆形放射状色块布局，中心为文字区"
    use_when: "教堂/神圣/庄严主题"
  - name: "现代彩玻版"
    diff: "配色更明快，铅线更细，更有 Tiffany 彩绘玻璃的现代感"
    use_when: "现代艺术/设计/轻奢"

css_snippets:
  keyframes: |
    @keyframes glassGlow {
      0%, 100% { box-shadow: 0 0 20px rgba(201,168,76,0.2); }
      50% { box-shadow: 0 0 40px rgba(201,168,76,0.4); }
    }
  effects: |
    .stained-panel {
      border: 3px solid rgba(10,10,20,0.8);
      opacity: 0.8;
      transition: opacity 0.3s;
    }
    .lead-line {
      background: #0a0a14;
      position: absolute;
    }
  patterns: |
    .jewel-ruby { background: rgba(200,30,50,0.75); }
    .jewel-sapphire { background: rgba(30,80,200,0.75); }
    .jewel-emerald { background: rgba(20,160,80,0.75); }
    .jewel-amethyst { background: rgba(120,40,180,0.75); }
    .jewel-gold { background: rgba(200,170,50,0.75); }
```
