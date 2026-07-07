# 21 · Neon Noir · 霓虹黑色电影

```yaml
name: "霓虹黑色电影"
name_en: "NeonNoir"
keywords: [黑色电影, 霓虹, 雨夜, 侦探, 都市, 悬疑]
best_for: [悬疑/影评, 城市故事, 深夜内容, 犯罪/推理]
emotional_tone: "冷峻"

palette:
  bg: "#0a0a10"
  surface: "rgba(20,20,40,0.5)"
  primary: "#ff2a6d"
  accent: "#05d9e8"
  text: "#d8d8e8"
  muted: "#5a5a7a"

fonts:
  heading: "'Rajdhani', 'PingFang SC', sans-serif"
  body: "'Space Mono', 'PingFang SC', monospace"

layout_2_35: "asymmetric-right"
layout_1_1: "centered"

core_rules:
  - "深暗背景 + 霓虹色（粉+青）灯光反射，像雨夜的街道"
  - "标题使用细长无衬线字体（Rajdhani），letter-spacing: 3-5px"
  - "加入百叶窗阴影效果（repeating-linear-gradient 半透明斜条纹）"
  - "背景需要模糊的灯光反射（霓虹色的 radial-gradient 光斑）"
  - "边缘使用暗角（vignette），加强电影感"
  - "文字周围带微弱 neon glow（text-shadow 但不夸张）"

negative_rules:
  - "禁止明亮背景"
  - "禁止使用暖色系（橙色/黄色）——只有霓虹粉+青+紫"
  - "禁止圆角——黑色电影是硬朗的"
  - "禁止使用衬线字体"

variants:
  - name: "蓝色版"
    diff: "primary 改为 #0077ff, accent 改为 #00cccc，蓝色调电影"
    use_when: "科幻悬疑/冷峻推理"
  - name: "单色版"
    diff: "全片黑白灰 + 单一霓虹粉 accent，致敬经典黑色电影"
    use_when: "复古侦探/40s风格"

css_snippets:
  keyframes: |
    @keyframes rainDrop {
      0% { transform: translateY(-100%); opacity: 0; }
      50% { opacity: 0.3; }
      100% { transform: translateY(100%); opacity: 0; }
    }
  effects: |
    .neon-noir-vignette {
      background: radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.7) 100%);
    }
    .venetian-blinds {
      background: repeating-linear-gradient(
        100deg, transparent, transparent 6px, rgba(255,42,109,0.06) 6px, rgba(255,42,109,0.06) 8px
      );
    }
    .blur-lamp {
      position: absolute;
      width: 30%; height: 40%;
      background: radial-gradient(circle, rgba(5,217,232,0.15), transparent 70%);
      filter: blur(30px);
    }
  patterns: |
    /* 黑色电影用光效而非纹理 */
```
