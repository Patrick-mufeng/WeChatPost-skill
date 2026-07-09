# Puppeteer 截图说明

封面使用 **Puppeteer**（而非 html2canvas）进行截图。Puppeteer 原生支持所有现代 CSS 特性，无需特殊 fallback 处理。

## Puppeteer 原生支持的 CSS 特性

| CSS 特性 | Puppeteer | 说明 |
|----------|-----------|------|
| `background-clip: text` | ✅ 完全支持 | 渐变文字正常渲染 |
| `filter: blur()` | ✅ 完全支持 | 模糊效果正常 |
| `filter: drop-shadow()` | ✅ 完全支持 | 投影效果正常 |
| `backdrop-filter` | ✅ 完全支持 | 毛玻璃效果正常 |
| CSS `background-image` SVG data URI | ✅ 完全支持 | 纹理噪点正常 |

## 兼容性注意事项

- Puppeteer 使用 Chromium 内核，CSS 支持度与最新 Chrome 一致
- 字体需使用 web-safe 字体或通过 `@font-face` 加载
- 中文回退字体：`PingFang SC` / `Noto Sans SC` / `Microsoft YaHei`
- 英文回退字体：`Inter` / `SF Pro Display` / `Segoe UI`
- 封面卡片 CSS 中禁止使用 `vw` 单位（详见设计原则）

## 截图流程

1. Puppeteer 打开 `preview.html`
2. 在同一个 viewport 中取 `.cover-2x35` 和 `.cover-1x1` 的 `getBoundingClientRect`
3. 分别 clip 截图保存为 `cover-2x35.png` 和 `cover-1x1.png`
4. Puppeteer 打开一个临时并排 HTML 页面，截图保存为 `cover-combined.png`
5. 清理临时文件
