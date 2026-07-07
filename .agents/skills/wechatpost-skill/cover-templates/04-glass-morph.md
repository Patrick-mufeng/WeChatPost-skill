# 04 · Glass Morph · 玻璃态

```yaml
name: "玻璃态"
name_en: "GlassMorph"
keywords: [毛玻璃, 景深, 渐变, 层次感, 现代]
best_for: [SaaS产品, 设计工具, UI/UX内容, 现代品牌]
emotional_tone: "冷峻"

palette:
  bg: "#0d1117"
  surface: "rgba(255,255,255,0.05)"
  primary: "#58a6ff"
  accent: "#f78166"
  text: "#e6edf3"
  muted: "#8b949e"

fonts:
  heading: "'SF Pro Display', 'Inter', 'PingFang SC', sans-serif"
  body: "'SF Pro Text', 'Inter', 'PingFang SC', sans-serif"

layout_2_35: "centered"
layout_1_1: "centered"

core_rules:
  - "背景必须有2-3个模糊光球（blur 80-120px），使用 primary/accent 的半透明色"
  - "内容区使用 backdrop-filter: blur(20px) + 半透明背景，形成玻璃层叠感"
  - "卡片边框使用 1px solid rgba(255,255,255,0.15)"
  - "所有圆角使用 16-24px，营造柔和现代感"
  - "光效层次：模糊光球在最底层 → 玻璃卡片在中间 → 文字在最上层"

negative_rules:
  - "禁止使用锐利边框或直角"
  - "禁止使用纯黑或纯白色块"
  - "禁止在玻璃卡片上使用不透明背景"
  - "禁止超过 3 层玻璃叠层（景深太复杂会乱）"

variants:
  - name: "紫色雾化版"
    diff: "primary 改为 #a371f7, accent 改为 #f778ba，光球改为紫粉渐变"
    use_when: "创意工具/设计类产品"
  - name: "浅色玻璃版"
    diff: "bg 改为 #f0f4f8, surface 改为 rgba(255,255,255,0.6)，整体明亮通透"
    use_when: "轻量工具/效率应用"
  - name: "多卡片版"
    diff: "使用 3 个小玻璃卡片横向排列，而非一个大卡片"
    use_when: "展示多个特性或数据点"

css_snippets:
  keyframes: |
    @keyframes floatOrb {
      0%, 100% { transform: translate(0, 0); }
      50% { transform: translate(20px, -20px); }
    }
  effects: |
    .glass-bg {
      background: rgba(255,255,255,0.05);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255,255,255,0.15);
      border-radius: 20px;
    }
    .glow-orb {
      position: absolute;
      border-radius: 50%;
      filter: blur(100px);
      opacity: 0.4;
    }
  patterns: |
    /* 无图案 — 玻璃态靠光效而非纹理 */
```
