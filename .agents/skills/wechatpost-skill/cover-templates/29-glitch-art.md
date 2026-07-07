# 29 · Glitch Art · 故障艺术

```yaml
name: "故障艺术"
name_en: "GlitchArt"
keywords: [故障, RGB分离, 数据损坏, 数字, 前卫, 扭曲]
best_for: [数字文化, 先锋内容, 实验艺术, 电子音乐]
emotional_tone: "冷峻"

palette:
  bg: "#0d0d0d"
  surface: "#111111"
  primary: "#ff0044"
  accent: "#00ffff"
  text: "#ffffff"
  muted: "#666666"

fonts:
  heading: "'Share Tech Mono', 'Fira Code', 'PingFang SC', monospace"
  body: "'Space Mono', 'PingFang SC', monospace"

layout_2_35: "centered"
layout_1_1: "centered"

core_rules:
  - "标题使用 RGB 通道分离：用 text-shadow 创建红/青偏移（red -4px 0, cyan 4px 0）"
  - "装饰区域使用像素块平移效果（clip-path 或 transform skew）模拟图像损坏"
  - "背景加入随机扫描线撕裂效果（不规则的水平条带）"
  - "必须使用等宽字体，增强数字感"
  - "颜色以黑底 + 高饱和红/青为主，模拟损坏的视频信号"
  - "可以加入噪点叠加和水平位移线"

negative_rules:
  - "禁止使用圆角——故障是锐利的数字损坏"
  - "禁止使用衬线字体"
  - "禁止使用柔和配色——必须是刺眼的数字色"
  - "禁止使用渐变——故障艺术是纯色二进制感"
  - "禁止完美的对齐——有意制造偏移和错位"

variants:
  - name: "VHS版"
    diff: "加入 VHS 录像带的色偏和跟踪线噪音，更复古"
    use_when: "怀旧/80s/录像带美学"
  - name: "数据溢出版"
    diff: "文字部分被 pixelated 矩形块覆盖，像数据损坏"
    use_when: "网络安全/黑客/数据主题"
  - name: "黑白版"
    diff: "只用黑白灰 + 噪点，无彩色偏移"
    use_when: "暗黑极简/摄影/实验"

css_snippets:
  keyframes: |
    @keyframes glitchShift {
      0%, 90%, 100% { transform: translate(0); }
      91% { transform: translate(-8px, 2px); }
      92% { transform: translate(6px, -1px); }
      93% { transform: translate(-3px, -3px); }
      94% { transform: translate(0); }
    }
    @keyframes scanTear {
      0% { transform: translateX(0); opacity: 0; }
      50% { opacity: 0.8; }
      100% { transform: translateX(20px); opacity: 0; }
    }
  effects: |
    .glitch-text {
      color: #fff;
      text-shadow:
        -4px 0 #ff0044,
        4px 0 #00ffff;
      animation: glitchShift 3s infinite;
    }
    .scan-tear {
      position: absolute;
      width: 100%; height: 4px;
      background: rgba(255,0,68,0.4);
      clip-path: polygon(0% 0%, 80% 0%, 90% 100%, 10% 100%);
    }
  patterns: |
    .glitch-noise {
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.08'/%3E%3C/svg%3E");
    }
```
