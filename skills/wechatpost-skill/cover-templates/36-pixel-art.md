# 36 · Pixel Art · 像素艺术

```yaml
name: "像素艺术"
name_en: "PixelArt"
keywords: [像素, 8-bit, 点阵, 复古游戏, NES, 怀旧]
best_for: [游戏内容, 怀旧主题, Geek文化, 独立游戏]
emotional_tone: "轻松"

palette:
  bg: "#2c2c54"
  surface: "#40407a"
  primary: "#f7dc6f"
  accent: "#ff6b6b"
  text: "#ffffff"
  muted: "#aaaacc"

fonts:
  heading: "'Press Start 2P', 'PingFang SC', monospace"
  body: "'Press Start 2P', 'VT323', 'PingFang SC', monospace"

layout_2_35: "centered"
layout_1_1: "framed"

core_rules:
  - "全部使用像素字体（Press Start 2P），字号小且方正"
  - "标题周围必须有像素边框（box-shadow: 多像素点叠加）"
  - "装饰使用像素块（小方形 div 排列成图案）"
  - "配色限定 NES 调色板：深蓝背景 + 金色/红色强调"
  - "使用 image-rendering: pixelated 保证锯齿感"
  - "装饰元素：像素星星、像素云、像素箭头、宝箱/金币图标"

negative_rules:
  - "禁止使用任何抗锯齿字体——必须是像素字体"
  - "禁止圆角和渐变——像素是方块的"
  - "禁止使用超过 8 种颜色——NES 调色板限制"
  - "禁止平滑过渡和模糊效果"

variants:
  - name: "Game Boy版"
    diff: "全部使用绿色系（#0f380f, #306230, #8bac0f, #9bbc0f），4阶绿"
    use_when: "Game Boy/童年/极简像素"
  - name: "SNES版"
    diff: "使用更丰富的16位调色板，色彩更明亮饱和"
    use_when: "更精致的像素/16位时代"

css_snippets:
  keyframes: |
    @keyframes pixelFloat {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-3px); }
    }
  effects: |
    .pixel-text {
      font-family: 'Press Start 2P', monospace;
      font-size: 16px;
      image-rendering: pixelated;
    }
    .pixel-border {
      box-shadow:
        4px 0 0 #f7dc6f, -4px 0 0 #f7dc6f,
        0 4px 0 #f7dc6f, 0 -4px 0 #f7dc6f,
        4px 4px 0 #ff6b6b, -4px -4px 0 #ff6b6b,
        4px -4px 0 #ff6b6b, -4px 4px 0 #ff6b6b;
    }
  patterns: |
    .pixel-grid {
      background-image: linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px);
      background-size: 8px 8px;
    }
```
