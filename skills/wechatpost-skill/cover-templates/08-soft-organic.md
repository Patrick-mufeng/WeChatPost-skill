# 08 · Soft Organic · 柔光暖调

```yaml
name: "柔光暖调"
name_en: "SoftOrganic"
keywords: [温暖, 有机形状, blob, 柔和, 生活感]
best_for: [生活随笔, 情感文章, 个人故事, 治愈内容]
emotional_tone: "温暖"

palette:
  bg: "#faf5f0"
  surface: "rgba(255,255,255,0.6)"
  primary: "#e07a5f"
  accent: "#f2cc8f"
  text: "#3d2c2c"
  muted: "#8b7171"

fonts:
  heading: "'Quicksand', 'Rounded Mplus', 'PingFang SC', sans-serif"
  body: "'Inter', 'PingFang SC', sans-serif"

layout_2_35: "centered"
layout_1_1: "centered"

core_rules:
  - "背景必须有 2 个有机 blob 形状（不规则圆润椭圆），使用暖色渐变"
  - "blob 使用 filter: blur(40-60px)，位于画面边角，创造柔和氛围"
  - "标题使用圆体/轻字重（500-600），营造温柔感"
  - "所有圆角使用 12-20px"
  - "主色调必须是暖色系（橙/粉/奶油），不可出现冷色"
  - "装饰元素：柔光点、细圆环、半透明波点"

negative_rules:
  - "禁止使用直角或锐利边缘"
  - "禁止使用冷色系（蓝/青/紫）"
  - "禁止使用衬线字体"
  - "禁止高对比度配色（整体必须柔和过渡）"
  - "禁止几何装饰（三角形、网格线）"

variants:
  - name: "日落版"
    diff: "blob 色改为橙色到粉色渐变（#f4845f → #f7a072 → #f28482）"
    use_when: "温暖故事/回忆/夕阳氛围"
  - name: "清晨版"
    diff: "blob 色改为淡黄到薄荷（#ffe8d6 → #d4e09b → #a5c882）"
    use_when: "清新/早晨/新开始主题"

css_snippets:
  keyframes: |
    @keyframes driftBlob {
      0%, 100% { transform: translate(0, 0) scale(1); }
      33% { transform: translate(15px, -10px) scale(1.05); }
      66% { transform: translate(-10px, 15px) scale(0.95); }
    }
  effects: |
    .organic-blob {
      position: absolute;
      border-radius: 60% 40% 55% 45% / 45% 55% 40% 60%;
      filter: blur(50px);
      opacity: 0.5;
      pointer-events: none;
    }
  patterns: |
    .soft-dots {
      background-image: radial-gradient(circle, rgba(224,122,95,0.15) 1px, transparent 1px);
      background-size: 30px 30px;
    }
```
