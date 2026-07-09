// cover-templates/screenshot.js
// 用法: node screenshot.js <项目根目录> <文章文件夹名>
// 示例: node screenshot.js "D:/WeChatPost-skill" "DeepSeek价格战_2026-05-27"
// 功能: 截取封面预览 HTML 中的 2.35:1 和 1:1 两张封面，合并为一张拼接图
// 前置: npm install puppeteer canvas

const puppeteer = require('puppeteer');
const { createCanvas, loadImage } = require('canvas');
const path = require('path');
const fs = require('fs');

function fail(msg) {
  console.error('❌ ' + msg);
  process.exit(1);
}

(async () => {
  const workDir = process.argv[2];
  const folderName = process.argv[3];

  if (!workDir || !folderName) {
    console.error('用法: node screenshot.js <项目根目录> <文章文件夹名>');
    console.error('示例: node screenshot.js "D:/WeChatPost-skill" "DeepSeek价格战_2026-05-27"');
    process.exit(1);
  }

  // WeChatPost 目录结构: outputs/{标题}_{日期}/article/cover/
  const outDir = path.resolve(workDir, 'outputs', folderName, 'article', 'cover');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  const htmlPath = path.join(outDir, 'preview.html');
  if (!fs.existsSync(htmlPath)) {
    fail('preview.html not found: ' + htmlPath + '\n  请确认路径正确：outputs/{文章文件夹}/article/cover/preview.html');
  }

  let browser;
  try {
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();

    // 2.35:1 + 1:1 封面截图
    await page.setViewport({ width: 1440, height: 800, deviceScaleFactor: 2 });
    const url = 'file:///' + encodeURI(htmlPath.replace(/\\/g, '/'));
    await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });

    const rects = await page.evaluate(() => {
      const el235 = document.querySelector('.cover-2x35');
      const el11 = document.querySelector('.cover-1x1');
      if (!el235 || !el11) return null;
      const r235 = el235.getBoundingClientRect();
      const r11 = el11.getBoundingClientRect();
      return {
        r235: { x: r235.x, y: r235.y, w: r235.width, h: r235.height },
        r11:  { x: r11.x,  y: r11.y,  w: r11.width,  h: r11.height }
      };
    });
    if (!rects) {
      fail('.cover-2x35 or .cover-1x1 element not found in preview.html');
    }

    await page.screenshot({ path: path.join(outDir, 'cover-2x35.png'), clip: rects.r235 });
    console.log('✅ cover-2x35.png (' + Math.round(rects.r235.w) + 'x' + Math.round(rects.r235.h) + ')');
    await page.screenshot({ path: path.join(outDir, 'cover-1x1.png'),  clip: rects.r11 });
    console.log('✅ cover-1x1.png  (' + Math.round(rects.r11.w) + 'x' + Math.round(rects.r11.h) + ')');
  } catch (err) {
    fail('截图失败: ' + err.message);
  } finally {
    if (browser) await browser.close();
  }

  // Canvas 合并 — 以 1:1 高度为基准，2.35:1 等比例缩放
  try {
    const img1 = await loadImage(path.join(outDir, 'cover-2x35.png'));
    const img2 = await loadImage(path.join(outDir, 'cover-1x1.png'));

    const targetH = img2.naturalHeight;
    const scale = targetH / img1.naturalHeight;
    const w1 = Math.round(img1.naturalWidth * scale);
    const w2 = img2.naturalWidth;

    const canvas = createCanvas(w1 + w2, targetH);
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#0a0a0a';
    ctx.fillRect(0, 0, w1 + w2, targetH);
    ctx.drawImage(img1, 0, 0, w1, targetH);
    ctx.drawImage(img2, w1, 0, w2, targetH);

    fs.writeFileSync(path.join(outDir, 'cover-combined.png'), canvas.toBuffer('image/png'));
    console.log('✅ cover-combined.png (' + (w1 + w2) + 'x' + targetH + ', side-by-side)');
  } catch (err) {
    fail('合并图片失败: ' + err.message);
  }

  console.log('📁 Output: ' + outDir);
})();
