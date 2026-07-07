# 07 · Dark Luxury · 暗金奢华

```yaml
name: "暗金奢华"
name_en: "DarkLuxury"
keywords: [黑金, 衬线, 金属, 高级感, 尊贵]
best_for: [品牌发布, 高端内容, 商业报告, 投资分析]
emotional_tone: "激昂"

palette:
  bg: "#0a0a0a"
  surface: "#111111"
  primary: "#d4af37"
  accent: "#c6963a"
  text: "#e8e0d0"
  muted: "#8a8060"

fonts:
  heading: "'Playfair Display', 'Noto Serif SC', 'Songti SC', serif"
  body: "'Lato', 'PingFang SC', sans-serif"

layout_2_35: "centered"
layout_1_1: "framed"

core_rules:
  - "背景使用近乎纯黑（#0a0a0a），营造低调奢华感"
  - "标题和装饰全部使用金色（#d4af37），配合细微渐变模拟金属光泽"
  - "标题使用衬线字体，字号 48-68px，letter-spacing: 2px"
  - "必须有细金线装饰（1px gold, 位于标题上方或下方）"
  - "四角或两侧使用金色细边框（1px, 距边缘 20px，不完全闭合）"
  - "字体颜色永远不能是纯白——必须是温暖的米白（#e8e0d0）"

negative_rules:
  - "禁止使用任何冷色（蓝/绿/紫）"
  - "禁止使用无衬线字体做标题"
  - "禁止使用发光或霓虹效果——金色是反射不是发光"
  - "禁止大面积平铺金色（金色是点缀不是底色）"
  - "禁止使用圆角——所有边框和线条必须笔直"

variants:
  - name: "白金版"
    diff: "primary 改为 #e8e8e8, accent 改为 #c0c0c0，冷峻高级感"
    use_when: "科技产品/银器/电子产品"
  - name: "玫瑰金版"
    diff: "primary 改为 #e8b4b8, accent 改为 #d4a0a0"
    use_when: "女性品牌/婚礼/美妆"
  - name: "极简黑金版"
    diff: "去掉四角边框，仅保留一条金线和标题，更克制"
    use_when: "极简主义品牌"

css_snippets:
  keyframes: |
    @keyframes goldShine {
      0% { background-position: -200% center; }
      100% { background-position: 200% center; }
    }
  effects: |
    .gold-text {
      background: linear-gradient(135deg, #d4af37 0%, #f5d77a 30%, #c6963a 60%, #d4af37 100%);
      -webkit-background-clip: text; background-clip: text;
      color: transparent;
    }
    .gold-line {
      width: 120px; height: 1px;
      background: linear-gradient(90deg, transparent, #d4af37, transparent);
    }
    .corner-frame {
      position: absolute;
      width: 30px; height: 30px;
      border-color: rgba(212,175,55,0.6);
      border-style: solid;
    }
    .corner-tl { top: 20px; left: 20px; border-width: 1px 0 0 1px; }
    .corner-br { bottom: 20px; right: 20px; border-width: 0 1px 1px 0; }
  patterns: |
    /* 无图案 — 奢华靠材质感而非纹理 */
```
