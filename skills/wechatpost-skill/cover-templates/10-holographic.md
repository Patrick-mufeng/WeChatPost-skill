# 10 · Holographic · 全息未来

```yaml
name: "全息未来"
name_en: "Holographic"
keywords: [虹彩, 棱镜, 渐变, 未来感, 光谱]
best_for: [前沿科技, Web3, 元宇宙, AI产品, 科幻]
emotional_tone: "冷峻"

palette:
  bg: "#080818"
  surface: "rgba(255,255,255,0.03)"
  primary: "#7b5ea7"
  accent: "#5eeadb"
  text: "#e8e0ff"
  muted: "#7a8aaa"

fonts:
  heading: "'Space Grotesk', 'Inter', 'PingFang SC', sans-serif"
  body: "'Inter', 'PingFang SC', sans-serif"

layout_2_35: "asymmetric-right"
layout_1_1: "centered"

core_rules:
  - "标题使用虹彩渐变：linear-gradient 包含 3-4 个颜色站（紫→青→粉→蓝），background-clip: text"
  - "背景必须有 2 道交叉的棱镜光柱（倾斜的模糊渐变带）"
  - "标题文字必须加微发光：filter: drop-shadow(0 0 10px currentColor)"
  - "边框和装饰使用 semi-transparent 的白色/浅紫"
  - "整体氛围：像透过棱镜看光线折射的效果"
  - "所有颜色必须来自光谱：紫→蓝→青→绿→黄→粉，不可使用纯暖色"

negative_rules:
  - "禁止使用纯色标题——标题必须是渐变"
  - "禁止使用暗沉配色——整体必须明亮通透"
  - "禁止使用衬线字体"
  - "禁止直角边框——所有边框用圆角"
  - "禁止大面积不透明色块——保持透明度和光感"

variants:
  - name: "暖光谱版"
    diff: "光谱改为暖色系：金→橙→粉→紫"
    use_when: "偏消费/生活类科技产品"
  - name: "极光版"
    diff: "加入极光飘带动画（keyframes shifting gradient），更动态"
    use_when: "活动宣传/动态内容"
  - name: "暗光谱版"
    diff: "bg 改为 #020208，光谱饱和度降低，更神秘"
    use_when: "深邃/哲学/太空主题"

css_snippets:
  keyframes: |
    @keyframes prismShift {
      0% { filter: hue-rotate(0deg); }
      100% { filter: hue-rotate(360deg); }
    }
    @keyframes prismSlide {
      0% { transform: translateX(-100%) rotate(15deg); opacity: 0; }
      50% { opacity: 0.6; }
      100% { transform: translateX(200%) rotate(15deg); opacity: 0; }
    }
  effects: |
    .holo-text {
      background: linear-gradient(135deg, #7b5ea7, #5eeadb, #ff6bbb, #5b8def);
      -webkit-background-clip: text; background-clip: text;
      color: transparent;
      filter: drop-shadow(0 0 15px rgba(94,234,219,0.4));
    }
    .prism-beam {
      position: absolute;
      width: 200%;
      height: 3px;
      background: linear-gradient(90deg, transparent, rgba(94,234,219,0.3), rgba(255,107,187,0.3), transparent);
      filter: blur(2px);
    }
  patterns: |
    .holo-grid {
      background-image:
        linear-gradient(rgba(94,234,219,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(94,234,219,0.04) 1px, transparent 1px);
      background-size: 50px 50px;
    }
```
