const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({ headless: false, slowMo: 1000 });
    const context = await browser.newContext({
        storageState: '.secrets/student-login-state.json'
    });
    const page = await context.newPage();

    const testMarkdown = encodeURIComponent('# 测试标题\n\n这是段落内容。\n\n- 列表项 1\n- 列表项 2\n\n**加粗文本**');
    const url = `http://localhost:5174/#/pages/knowledge/detail?id=999&summary=${testMarkdown}`;

    console.log('Navigating to:', url);
    await page.goto(url);
    await page.waitForTimeout(5000);

    // Debug: check what elements exist
    const markdown = await page.locator('.markdown-body').count();
    const plain = await page.locator('.plain-content').count();
    const fallbackNotice = await page.locator('text=知识详情暂不可用').count();

    console.log('markdown-body count:', markdown);
    console.log('plain-content count:', plain);
    console.log('fallback notice count:', fallbackNotice);

    // Get the actual text content
    if (plain > 0) {
        const plainText = await page.locator('.plain-content').first().textContent();
        console.log('Plain text content:', plainText);
    }

    if (markdown > 0) {
        const markdownHTML = await page.locator('.markdown-body').first().innerHTML();
        console.log('Markdown HTML:', markdownHTML.substring(0, 200));
    }

    await page.screenshot({ path: 'knowledge-debug.png', fullPage: true });

    console.log('\nScreenshot saved to knowledge-debug.png');
    console.log('Press Ctrl+C to close browser...');

    await page.waitForTimeout(30000);
    await browser.close();
})();
