# 02 · Cyber Neon · 赛博霓虹

```yaml
name: "赛博霓虹"
name_en: "CyberNeon"
keywords: [暗底, 霓虹, 辉光, 扫描线, 科技感]
best_for: [技术教程, 产品发布, 开发工具, Web3, AI内容]
emotional_tone: "冷峻"

palette:
  bg: "#0a0a14"
  surface: "#111122"
  primary: "#00f0ff"
  accent: "#ff00aa"
  text: "#e0f0ff"
  muted: "#4a5a7a"

fonts:
  heading: "'Orbitron', 'Rajdhani', 'PingFang SC', sans-serif"
  body: "'JetBrains Mono', 'SF Mono', 'PingFang SC', monospace"

layout_2_35: "asymmetric-right"
layout_1_1: "centered"

core_rules:
  - "背景必须是深暗色（#0a0a14 附近），营造黑夜/终端感"
  - "标题使用 text-shadow 发光：0 0 20px primary, 0 0 40px primary（opacity 0.6）"
  - "必须有扫描线纹理（CSS repeating-linear-gradient 半透明横条）"
  - "装饰元素全部使用 primary 和 accent 的发光效果"
  - "网格线装饰：使用 background-image 画 40px 间隔的半透明网格"
  - "副标题和标签使用 monospace 等宽字体，强化终端感"

negative_rules:
  - "禁止使用暖色（红橙黄）——整个画面必须是冷色系"
  - "禁止纯白文字全文使用——正文用 muted 或稍暗的蓝白"
  - "禁止圆角和柔和过渡——边框和过渡要锐利"
  - "禁止使用 serif 字体"

variants:
  - name: "绿色终端版"
    diff: "primary 改为 #00ff41, accent 改为 #008f11, 模仿经典 CRT 绿屏"
    use_when: "黑客/安全/底层技术内容"
  - name: "紫金霓虹版"
    diff: "primary 改为 #b44dff, accent 改为 #ffd700"
    use_when: "高端科技或游戏相关内容"
  - name: "极简霓虹版"
    diff: "去掉网格线，只保留扫描线+发光标题，更干净的赛博风"
    use_when: "需要科技感但不想太花哨"

css_snippets:
  keyframes: |
    @keyframes neonFlicker {
      0%, 100% { opacity: 1; }
      95% { opacity: 0.95; }
      96% { opacity: 0.8; }
      97% { opacity: 1; }
    }
  effects: |
    .neon-glow {
      text-shadow: 0 0 10px var(--primary), 0 0 30px var(--primary), 0 0 60px var(--primary);
    }
    .neon-box {
      border: 1px solid var(--primary);
      box-shadow: 0 0 8px var(--primary), inset 0 0 8px var(--primary);
    }
  patterns: |
    .scanlines {
      background: repeating-linear-gradient(
        0deg, transparent, transparent 2px, rgba(0,240,255,0.03) 2px, rgba(0,240,255,0.03) 4px
      );
    }
    .cyber-grid {
      background-image:
        linear-gradient(rgba(0,240,255,0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,240,255,0.08) 1px, transparent 1px);
      background-size: 40px 40px;
    }
```
