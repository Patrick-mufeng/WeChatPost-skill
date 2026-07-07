# Template Schema · 模板字段规范

每个模板文件必须包含以下全部字段。字段缺失视为模板未完成。

---

## 必填字段

### 元信息

```yaml
name: "模板中文名"
name_en: "TemplateEnglishName"       # 用于文件命名
keywords: [关键词1, 关键词2, 关键词3]   # 3-6个，用于风格检索
best_for: [场景1, 场景2, 场景3]       # 最适用的文章类型
emotional_tone: "冷峻/温暖/激昂/轻松/严肃"
```

### 色板

```yaml
palette:
  bg: "#hex"           # 封面背景色
  surface: "#hex"      # 卡片/区块底色
  primary: "#hex"      # 主色（标题色）
  accent: "#hex"       # 强调色（高亮、装饰）
  text: "#hex"         # 正文色
  muted: "#hex"        # 次要文字色
```

### 字体

```yaml
fonts:
  heading: "'FontName', fallback, sans-serif"
  body: "'FontName', fallback, sans-serif"
  # 中文回退：PingFang SC / Noto Sans SC / Microsoft YaHei
  # 英文回退：Inter / SF Pro Display / Segoe UI
```

### 布局

```yaml
layout_2_35: "asymmetric-right | centered | left-column | diagonal | split"  # 2.35:1布局范式
layout_1_1: "centered | top-down | framed"                                    # 1:1布局范式
```

布局范式说明：

| 范式 | 描述 |
|------|------|
| `asymmetric-right` | 左文字右装饰，文字占50-60% |
| `asymmetric-left` | 右文字左装饰 |
| `centered` | 全部居中 |
| `left-column` | 左侧竖排文字+右侧大面积留白/装饰 |
| `diagonal` | 对角线构图 |
| `split` | 上下或左右等分 |
| `framed` | 居中内容+四周边框装饰 |
| `top-down` | 从上到下依次排列 |

### 核心规则

```yaml
core_rules:
  - "规则1：具体可执行的设计指令"
  - "规则2"
  - "规则3"
  - "规则4"
  - "规则5"
  # 最少4条，最多8条
```

每条规则必须可被执行（不说"要好看"，要说"标题使用 text-shadow 发光效果，颜色为 primary"）。

### 禁止规则

```yaml
negative_rules:
  - "禁止1：该风格绝对不能做的事"
  - "禁止2"
  - "禁止3"
  # 最少3条，最多6条
```

### 变体

```yaml
variants:
  - name: "变体名"
    diff: "与原版的具体差异（配色微调/装饰替换/布局微调）"
    use_when: "什么场景下用这个变体"
  # 最少2个
```

### CSS 片段

```yaml
css_snippets:
  keyframes: |
    /* 该风格特有动画 */
  effects: |
    /* 该风格特效（发光/模糊/渐变等） */
  patterns: |
    /* 该风格图案（网格/纹理/装饰） */
  effects: |\n    /* 该风格特效（发光/模糊/渐变等） */\n  patterns: |\n    /* 该风格图案（网格/纹理/装饰） */\n---

## 模板文件命名

```
{序号}-{name_en}.md

示例：
01-swiss-minimal.md
15-constellation.md
40-de-stijl.md
```

---

## 校验清单

模板完成后必须通过以下检查：

- [ ] 所有必填字段存在且非空
- [ ] palette 含 6 个色值（bg/surface/primary/accent/text/muted）
- [ ] core_rules ≥ 4 条
- [ ] negative_rules ≥ 3 条
- [ ] variants ≥ 2 个
- [ ] css_snippets 至少含 effects 和 patterns
- [ ] 文件名符合命名规范

