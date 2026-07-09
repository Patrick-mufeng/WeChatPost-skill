# 生图提示词模板

每张图单独生成。根据正文内容替换变量，不要把多张图拼在一起。

```text
Generate one standalone 16:9 horizontal Chinese article illustration.

Visual DNA:
Pure white background. Minimalist hand-drawn black line art with flat color fills (flat cel-shading coloring-book style — no gradients, no shadows, no highlights, no paper texture). Slightly wobbly organic pen lines, not vector-clean. Lots of empty white space. Sparse red/orange handwritten Chinese annotations. Clean absurd product-sketch feeling. No complex background, no commercial vector style, no PPT infographic look, no cute mascot poster, no children's illustration, no realistic UI. Preserve at least 35% blank white space.

Recurring IP character 小霓 — fixed colors, never change:
A slender angular female cyber operator with geometric bob haircut (flat dark indigo #2c3e6b), porcelain skin (#f5efe6), white dot eyes (no pupils), calm detached expression. Wearing an oversized minimalist sage-green tech vest (#8a9b8e). Silver-gray data goggles pushed up on forehead (#b0b0b0). Thin antenna-like hair details same as hair color. Thin dark gray (#555) joint lines on elbows. 小霓 must perform the core conceptual action, not decorate the scene. Make 小霓 serious, deadpan, slightly detached, and competent-not-cute.

Theme:
{正文配图主题}

Structure type:
{结构类型：Workflow / 系统局部 / 前后对比 / 角色状态 / 概念隐喻 / 方法分层 / 地图路线 / 小漫画分镜}

Core idea:
{这张图要表达的核心意思}

Composition:
{具体画面：小霓在哪里、正在做什么、主要物件是什么、信息如何流动}

Suggested elements:
{元素1} / {元素2} / {元素3} / {元素4}

Chinese handwritten labels:
{标注词1} / {标注词2} / {标注词3} / {标注词4} / {可选标注词5}

Color rules:
- 小霓 always uses her fixed colors above — never change across illustrations.
- Other elements (objects, props, pipes, panels, backgrounds) use flat fills from the article mood palette: {色板主色} / {色板辅色} / {色板底色}. All flat, no gradients, no shading.
- Black (#333) for all line art, outlines, main text, and 小霓's contour lines.
- Red (#c75b3a) only for key warnings, critical annotations, results.
- Orange (#d4786e) only for main flow paths, arrows, data direction lines.
- Blue (#4a7d9a) only for secondary notes, system state — optional, not every image needs it.
- All color fills are flat cel-shading. No highlights, no rim light, no texture.

Constraints:
One image explains only one core structure. Keep the main subject around 40%-60% of the canvas. Preserve at least 35% blank white space. Use at most 5-8 short handwritten Chinese labels. Do not write a title in the top-left corner. Do not write the structure type on the image. Do not make it a formal diagram, course slide, or dense explainer. Do not copy prior examples or reuse known case compositions unless explicitly requested; invent a fresh visual metaphor for this specific article. It should be clear but not instructional, interesting but not childish, strange but clean.
```

## 图像编辑提示（备用）

以下 prompt 用于 Phase 4 QA 未通过时的局部修复。**不是默认生成路径**——仅在 AI 判断某张图有特定缺陷时使用，而非全局重生成。

### 去掉左上角标题：

```text
Edit the provided image. Remove only the handwritten title "{要删除的文字}" and its underline from the top-left corner. Fill that area with the same clean white background, matching the surrounding blank paper. Preserve everything else exactly: characters, labels, paths, line style, composition, aspect ratio, and image quality. Do not add any new text or objects.
```

增强怪诞感：

```text
Regenerate this illustration with the same core meaning and simple layout, but make 小霓 more central to the conceptual action. 小霓 should be doing the strange work that explains the idea, not standing beside the diagram. Keep it clean, sparse, hand-drawn, and not cute.
```


