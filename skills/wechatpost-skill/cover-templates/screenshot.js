// cover-templates/screenshot.js
// 用法: node screenshot.js <项目根目录> <文章文件夹名>
// 示例: node screenshot.js "D:/WeChatPost-skill" "DeepSeek价格战_2026-05-27"
// 功能: 截取封面预览 HTML 中的 2.35:1 和 1:1 两张封面，合并为一张拼接图
// 前置: npm install puppeteer

const puppeteer = require('puppeteer');
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

    await page.screenshot({ path: path.join(outDir, 'cover-2x35.png'), clip: { x: Math.round(rects.r235.x), y: Math.round(rects.r235.y), width: Math.round(rects.r235.w), height: Math.round(rects.r235.h) } });
    console.log('✅ cover-2x35.png (' + Math.round(rects.r235.w) + 'x' + Math.round(rects.r235.h) + ')');
    await page.screenshot({ path: path.join(outDir, 'cover-1x1.png'),  clip: { x: Math.round(rects.r11.x), y: Math.round(rects.r11.y), width: Math.round(rects.r11.w), height: Math.round(rects.r11.h) } });
    console.log('✅ cover-1x1.png  (' + Math.round(rects.r11.w) + 'x' + Math.round(rects.r11.h) + ')');

    // 合并 — 用 puppeteer 打开一个并排显示两张截图的临时 HTML 页面截图
    const w235 = Math.round(rects.r235.w);
    const h235 = Math.round(rects.r235.h);
    const w11  = Math.round(rects.r11.w);
    const h11  = Math.round(rects.r11.h);
    const targetH = h11;                    // 以 1:1 高度为基准
    const scale = targetH / h235;
    const w1 = Math.round(w235 * scale);    // 2.35:1 等比例缩放后的宽度
    const w2 = w11;                         // 1:1 宽度
    const combinedW = w1 + w2;

    const mergeHTML = `<!DOCTYPE html>
<html><head><style>
  *{margin:0;padding:0} body{background:#0a0a0a;display:flex;width:${combinedW}px;height:${targetH}px}
  img{display:block;height:${targetH}px}
</style></head><body>
  <img src="file:///${encodeURI(path.join(outDir, 'cover-2x35.png').replace(/\\/g, '/'))}" style="width:${w1}px">
  <img src="file:///${encodeURI(path.join(outDir, 'cover-1x1.png').replace(/\\/g, '/'))}" style="width:${w2}px">
</body></html>`;

    const mergePath = path.join(outDir, '_merge.html');
    fs.writeFileSync(mergePath, mergeHTML, 'utf-8');

    await page.setViewport({ width: combinedW, height: targetH, deviceScaleFactor: 1 });
    await page.goto('file:///' + encodeURI(mergePath.replace(/\\/g, '/')), { waitUntil: 'load', timeout: 10000 });
    await page.screenshot({ path: path.join(outDir, 'cover-combined.png') });
    fs.unlinkSync(mergePath);  // 清理临时文件
    console.log('✅ cover-combined.png (' + combinedW + 'x' + targetH + ', side-by-side)');
  } catch (err) {
    fail('截图失败: ' + err.message);
  } finally {
    if (browser) await browser.close();
  }

  console.log('📁 Output: ' + outDir);
})();
