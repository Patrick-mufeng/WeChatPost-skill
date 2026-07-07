# 15 · Constellation · 星座星图

```yaml
name: "星座星图"
name_en: "Constellation"
keywords: [星图, 星座, 深空, 连线, 神秘, 探索]
best_for: [深度思考, 哲学, 科学科普, 宇宙主题]
emotional_tone: "严肃"

palette:
  bg: "#060d1a"
  surface: "transparent"
  primary: "#e8d5b0"
  accent: "#7eb8da"
  text: "#d0c8b8"
  muted: "#5a7080"

fonts:
  heading: "'Cinzel', 'Noto Serif SC', 'Songti SC', serif"
  body: "'Source Sans Pro', 'PingFang SC', sans-serif"

layout_2_35: "asymmetric-right"
layout_1_1: "centered"

core_rules:
  - "背景深空蓝黑，散布 15-30 个白色/金色星点（大小 1-4px 随机）"
  - "部分星点之间用极细白色/淡蓝线连接（opacity 0.3-0.5），模拟星座连线"
  - "标题使用金色/暖白，模拟星光色"
  - "右下或左下必须有罗盘/星盘装饰（同心圆 + 十字线）"
  - "整体氛围静谧、深邃、神秘"
  - "文字区可以有微弱的径向光晕，就像被星光照射"

negative_rules:
  - "禁止使用高饱和颜色——星空是柔和的"
  - "禁止使用粗体无衬线——要用优雅的衬线"
  - "禁止大面积亮色块——画面 80% 以上必须是暗色"
  - "禁止机械的均匀网格——星点是随机的"

variants:
  - name: "星云版"
    diff: "背景加入紫色和青色的模糊光斑，模拟星云"
    use_when: "更绚丽的宇宙主题"
  - name: "天文台版"
    diff: "加入十字准星、赤经赤纬标记线，更科学仪器感"
    use_when: "硬核天文/物理内容"

css_snippets:
  keyframes: |
    @keyframes twinkle {
      0%, 100% { opacity: 0.4; }
      50% { opacity: 1; }
    }
  effects: |
    .star {
      position: absolute;
      background: #fff;
      border-radius: 50%;
      box-shadow: 0 0 4px #fff, 0 0 8px rgba(126,184,218,0.5);
    }
    .constellation-line {
      position: absolute;
      height: 1px;
      background: rgba(255,255,255,0.25);
      transform-origin: left center;
    }
  patterns: |
    .compass-rose circle {
      fill: none;
      stroke: rgba(232,213,176,0.3);
      stroke-width: 0.5px;
    }
    .compass-rose line {
      stroke: rgba(232,213,176,0.2);
      stroke-width: 0.5px;
    }
```
