# 30 · Botanical · 植物标本

```yaml
name: "植物标本"
name_en: "Botanical"
keywords: [植物, 标本, 科学插画, 复古, 自然, 博物]
best_for: [自然科普, 园艺内容, 环保主题, 田园生活]
emotional_tone: "温暖"

palette:
  bg: "#f8f4ec"
  surface: "#fafaf5"
  primary: "#2d5016"
  accent: "#8b6b4a"
  text: "#3a3020"
  muted: "#7a8a70"

fonts:
  heading: "'Cormorant Garamond', 'Noto Serif SC', 'Songti SC', serif"
  body: "'Source Serif Pro', 'Noto Serif SC', serif"

layout_2_35: "asymmetric-right"
layout_1_1: "framed"

core_rules:
  - "背景使用暖白/米色（仿旧纸张），边框用细线框"
  - "必须有植物插画装饰：蕨类叶片、花朵剪影、枝条线描"
  - "装饰使用单色或双色（深绿/棕），像19世纪植物图鉴"
  - "标题用衬线体，下方有拉丁文风格的小字"
  - "画面底部或侧边有'标本标签'：小字标注文章信息"
  - "整体像翻开一本古董植物学书籍"

negative_rules:
  - "禁止使用荧光色或高饱和色"
  - "禁止使用无衬线字体"
  - "禁止现代科技装饰（网格、发光、渐变）"
  - "禁止暗色背景"
  - "禁止超过 3 种颜色（纸张色+植物绿+墨水棕）"

variants:
  - name: "花卉版"
    diff: "装饰改为花卉（玫瑰/牡丹）线描，更浪漫"
    use_when: "花园/婚礼/女性自然主题"
  - name: "深色羊皮纸版"
    diff: "bg 改为 #d4c8b0（仿羊皮纸色），营造更古老的感觉"
    use_when: "中世纪/炼金术/古籍主题"

css_snippets:
  keyframes: |
    /* 植物标本不使用动画 */
  effects: |
    .herbarium-frame {
      border: 1px solid #8b6b4a;
      box-shadow: inset 0 0 0 2px rgba(139,107,74,0.1);
    }
    .specimen-label {
      font-size: 11px;
      font-family: 'Courier New', monospace;
      color: #5a4a30;
      border-top: 1px solid #8b6b4a;
      padding-top: 8px;
    }
  patterns: |
    .botanical-illustration {
      position: absolute;
      opacity: 0.3;
      pointer-events: none;
    }
    .leaf-vein {
      stroke: #2d5016;
      stroke-width: 0.5;
      fill: none;
      opacity: 0.5;
    }
```
