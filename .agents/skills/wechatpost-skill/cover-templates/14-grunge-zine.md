# 14 · Grunge Zine · 朋克拼贴

```yaml
name: "朋克拼贴"
name_en: "GrungeZine"
keywords: [撕裂, 拼贴, 噪音, 手写, 朋克, 反叛]
best_for: [独立创作, 反主流, 音乐评论, 青年文化]
emotional_tone: "激昂"

palette:
  bg: "#e8e0d8"
  surface: "#ffffff"
  primary: "#1a1a1a"
  accent: "#ff3b3b"
  text: "#111111"
  muted: "#666666"

fonts:
  heading: "'Permanent Marker', 'Impact', 'PingFang SC', cursive"
  body: "'Special Elite', 'Courier New', 'PingFang SC', monospace"

layout_2_35: "diagonal"
layout_1_1: "centered"

core_rules:
  - "模拟拼贴效果：文字区域像被剪刀剪下后粘贴，使用不规则边框"
  - "使用 box-shadow 制造纸张叠加效果：多层不同偏移的阴影"
  - "必须有噪点纹理覆盖（CSS filter + SVG noise 或 dot pattern）"
  - "颜色粗糙：黑白为主 + 醒目的红色强调"
  - "排版刻意不完美：行间距不均、字母略有旋转"
  - "装饰元素：胶带条、撕边、手写箭头"

negative_rules:
  - "禁止整齐对齐——必须有意制造不完美"
  - "禁止使用渐变——要粗糙的纯色"
  - "禁止使用衬线字体"
  - "禁止使用圆角和柔化过渡"
  - "禁止超过 4 种颜色"

variants:
  - name: "暗底朋克版"
    diff: "bg 改为 #111, surface 改为 #1a1a1a, text 改为 #eee"
    use_when: "暗黑/金属/工业主题"
  - name: "彩色噪点版"
    diff: "加入 CMYK 偏移效果（text-shadow 多色偏移），更迷幻"
    use_when: "迷幻/实验/前卫内容"

css_snippets:
  keyframes: |
    @keyframes grain {
      0%, 100% { transform: translate(0, 0); }
      10% { transform: translate(-1%, -1%); }
      50% { transform: translate(2%, 1%); }
      90% { transform: translate(-1%, 2%); }
    }
  effects: |
    .grunge-noise {
      position: absolute;
      inset: 0;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.1'/%3E%3C/svg%3E");
      pointer-events: none;
    }
    .torn-paper {
      clip-path: polygon(0% 5%, 3% 0%, 8% 3%, 15% 0%, 25% 4%, 35% 0%, 45% 5%, 55% 0%, 65% 3%, 75% 0%, 85% 4%, 95% 0%, 100% 5%, 100% 95%, 95% 100%, 85% 96%, 75% 100%, 65% 97%, 55% 100%, 45% 95%, 35% 100%, 25% 96%, 15% 100%, 5% 97%, 0% 95%);
    }
  patterns: |
    .tape-strip {
      background: rgba(255,255,255,0.6);
      transform: rotate(-3deg);
      width: 60px; height: 20px;
    }
```
