# 13 · Art Deco · 装饰艺术

```yaml
name: "装饰艺术"
name_en: "ArtDeco"
keywords: [金色, 几何对称, 扇形, 奢华, 盖茨比, 20s]
best_for: [品牌故事, 高端发布, 建筑/设计, 经典内容]
emotional_tone: "激昂"

palette:
  bg: "#0d0d0d"
  surface: "#1a1a1a"
  primary: "#d4af37"
  accent: "#c49a2c"
  text: "#f0e6d0"
  muted: "#8a7a5a"

fonts:
  heading: "'Playfair Display', 'Cinzel', 'Songti SC', serif"
  body: "'Montserrat', 'PingFang SC', sans-serif"

layout_2_35: "centered"
layout_1_1: "framed"

core_rules:
  - "标题上下必须有对称的几何装饰（扇形放射纹、阶梯式线条）"
  - "使用金色渐变模拟金属光泽，标题用 gold-text 效果"
  - "版面完全居中对称——左右镜像"
  - "装饰线条层层递进：外层细金线 → 中层中等 → 内层文字"
  - "字体间距大（letter-spacing: 3-6px），体现仪式感"
  - "背景使用极暗黑，突出金色装饰"

negative_rules:
  - "禁止不对称布局"
  - "禁止使用冷色系金色以外的主色"
  - "禁止圆角——装饰艺术是锐利几何"
  - "禁止现代科技元素（网格、终端、发光）"

variants:
  - name: "翡翠金版"
    diff: "bg 加入深绿（#0a1a0a），金色不变，更盖茨比"
    use_when: "绿金主题/复古奢华"
  - name: "黑白金版"
    diff: "bg 改为 #fafafa, text 改为 #111，金色不变"
    use_when: "高端极简品牌"

css_snippets:
  keyframes: |
    /* 装饰艺术不使用动画 — 静态对称 */
  effects: |
    .artdeco-frame {
      border: 1px solid rgba(212,175,55,0.4);
      position: relative;
    }
    .fan-motif {
      width: 80px; height: 40px;
      background: repeating-conic-gradient(
        rgba(212,175,55,0.3) 0deg 5deg, transparent 5deg 10deg
      );
      border-radius: 0 0 80px 80px;
    }
    .stepped-line {
      height: 1px;
      background: linear-gradient(90deg, transparent, #d4af37 20%, #d4af37 80%, transparent);
    }
  patterns: |
    .geometric-border {
      border: 2px solid rgba(212,175,55,0.3);
      outline: 1px solid rgba(212,175,55,0.15);
      outline-offset: 6px;
    }
```
