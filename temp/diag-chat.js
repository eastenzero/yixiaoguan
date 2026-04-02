const { chromium } = require('playwright');
const { execSync } = require('child_process');

function getRedisCode(uuid) {
  if (!uuid) return null;
  const cmd = `docker exec yx_redis redis-cli -a "Yx@Redis2026!" get captcha_codes:${uuid}`;
  const result = execSync(cmd, { encoding: 'utf-8', timeout: 3000 }).trim();
  return result.replace(/^"/, '').replace(/"$/, '');
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });

  let captchaUuid = null;
  page.on('response', async resp => {
    const url = resp.url();
    if (url.includes('/api/captchaImage')) {
      try { const j = await resp.json(); if (j.uuid) captchaUuid = j.uuid; } catch(e){}
    }
  });

  // Login
  await page.goto('http://localhost:5174/#/pages/login/index');
  await page.waitForTimeout(2000);
  const code = captchaUuid ? getRedisCode(captchaUuid) : null;
  await page.fill('input[type="text"]', '4523570155');
  await page.fill('input[type="password"]', 'admin123');
  await page.locator('.captcha-input input').first().fill(code || '0000');
  await page.click('button:has-text("登录"), .login-btn');
  await page.waitForTimeout(3000);

  // Go to chat
  await page.goto('http://localhost:5174/#/pages/chat/index');
  await page.waitForTimeout(3000);

  // Listen for /api/chat response
  let chatResponse = null;
  page.on('response', async resp => {
    const url = resp.url();
    if (url.includes('/api/chat')) {
      try {
        chatResponse = { url, status: resp.status(), body: await resp.text() };
      } catch(e){}
    }
  });

  // Fill and send
  await page.locator('uni-input.message-input input').fill('学校图书馆几点开门？');
  await page.locator('button:has-text("发送"), .send-btn').first().click();
  await page.waitForTimeout(12000);

  const text = await page.innerText('body');
  console.log('\n=== CHAT PAGE TEXT ===');
  console.log(text);

  if (chatResponse) {
    console.log('\n=== CHAT API RESPONSE ===');
    console.log('Status:', chatResponse.status);
    console.log('Body:', chatResponse.body.substring(0, 800));
  } else {
    console.log('\nNo /api/chat response captured');
  }

  await page.screenshot({ path: 'C:/Users/Administrator/Documents/code/yixiaoguan/temp/diag-chat-after.png', fullPage: true });
  console.log('Screenshot saved');
  await browser.close();
})();
