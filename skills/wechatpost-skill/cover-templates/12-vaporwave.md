# 12 · Vaporwave · 蒸汽波

```yaml
name: "蒸汽波"
name_en: "Vaporwave"
keywords: [蒸汽波, 粉紫, 霓虹日落, 复古未来, 合成器]
best_for: [亚文化, 创意内容, 音乐/艺术, 怀旧主题]
emotional_tone: "轻松"

palette:
  bg: "#1a0a2e"
  surface: "rgba(255,107,157,0.08)"
  primary: "#ff6b9d"
  accent: "#00f5ff"
  text: "#ffe0f0"
  muted: "#a890c8"

fonts:
  heading: "'Russo One', 'PingFang SC', sans-serif"
  body: "'Share Tech Mono', 'PingFang SC', monospace"

layout_2_35: "centered"
layout_1_1: "centered"

core_rules:
  - "背景必须有粉色到紫色的纵向渐变 + 底部水平网格线（日落地平线感）"
  - "标题使用粗体宽字（Russo One / Impact-like），带轻微 text-shadow"
  - "必须有日文装饰文字（如 美学排版 / 未来的），竖排或小号横排"
  - "整体色调：粉+紫+青，模拟 80s 霓虹夜景"
  - "使用 3D 透视网格线或水平分层线营造空间深度"
  - "装饰：太阳圆（粉橙渐变圆形）、星点、扫描线"

negative_rules:
  - "禁止使用衬线字体"
  - "禁止使用自然色系（绿/棕）"
  - "禁止留白——蒸汽波是 Maximalist"
  - "禁止过于锐利的现代科技感——要复古"

variants:
  - name: "暗夜蒸汽波版"
    diff: "去掉太阳圆，使用紫色为主色调，更像深夜街头"
    use_when: "深夜情绪/城市孤独主题"
  - name: "极简蒸汽波版"
    diff: "只保留渐变背景+太阳+标题，去掉网格和日文"
    use_when: "需要蒸汽波味道但不想要太繁复"

css_snippets:
  keyframes: |
    @keyframes vaporFloat {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-10px); }
    }
  effects: |
    .vapor-sun {
      position: absolute;
      width: 40%; height: 50%;
      background: linear-gradient(180deg, #ff6b9d, #ff8c42, transparent);
      border-radius: 50%;
      filter: blur(2px);
    }
    .horizon-grid {
      background: repeating-linear-gradient(
        0deg, rgba(0,245,255,0.1) 0px, rgba(0,245,255,0.1) 1px, transparent 1px, transparent 3px
      );
      transform: perspective(500px) rotateX(60deg);
    }
  patterns: |
    .jp-text {
      writing-mode: vertical-rl;
      font-size: 14px;
      color: rgba(255,107,157,0.6);
      letter-spacing: 4px;
    }
```
