# 40 · De Stijl · 风格派

```yaml
name: "风格派"
name_en: "DeStijl"
keywords: [蒙德里安, 网格, 三原色, 黑线, 荷兰, 现代主义]
best_for: [设计理论, 现代艺术, 建筑/空间, 结构内容]
emotional_tone: "冷峻"

palette:
  bg: "#f5f3f0"
  surface: "#ffffff"
  primary: "#111111"
  accent: "#e63946"
  text: "#111111"
  muted: "#888888"

fonts:
  heading: "'Jost', 'Futura', 'PingFang SC', sans-serif"
  body: "'Inter', 'PingFang SC', sans-serif"

layout_2_35: "split"
layout_1_1: "framed"

core_rules:
  - "使用黑色粗线（3-4px）将画面分割成矩形网格（蒙德里安风格）"
  - "部分矩形填充三原色（红黄蓝），部分留白或浅灰"
  - "文字放在一个干净的白色矩形内，被黑色边框包围"
  - "色块随机不对称分布，但视觉平衡"
  - "颜色严格限定：红(#e63946) + 黄(#ffd000) + 蓝(#1d7ab5) + 黑白灰"
  - "所有线条水平和垂直——无斜线无曲线"

negative_rules:
  - "禁止使用除红黄蓝黑白灰以外的任何颜色"
  - "禁止斜线或曲线——只有水平和垂直线"
  - "禁止渐变色——全部纯色平涂"
  - "禁止衬线字体"
  - "禁止阴影或 3D 效果——完全平面"

variants:
  - name: "暗底版"
    diff: "bg 改为 #1a1a1a，黑色线改为白色线，原色不变"
    use_when: "深色主题/现代艺术感"
  - name: "极简版"
    diff: "只用红+蓝+白，去掉黄色，更冷静"
    use_when: "严肃/极简/男性品牌"

css_snippets:
  keyframes: |
    /* 风格派不使用动画 — 永恒的秩序 */
  effects: |
    .mondrian-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      grid-template-rows: repeat(3, 1fr);
      gap: 4px;
      background: #111;
    }
    .mondrian-cell {
      background: #fff;
    }
    .cell-red { background: #e63946; }
    .cell-yellow { background: #ffd000; }
    .cell-blue { background: #1d7ab5; }
  patterns: |
    .black-bar-h {
      height: 4px; background: #111;
    }
    .black-bar-v {
      width: 4px; background: #111;
    }
    /* 
    蒙德里安构图示例（CSS Grid）：
    4列3行，黑色gap=4px
    红格：2×2 左上
    黄格：1×1 右下角
    蓝格：1×2 右侧中间
    其余白格
    */
```
