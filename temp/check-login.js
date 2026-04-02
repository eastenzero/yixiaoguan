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
      try {
        const body = await resp.json();
        captchaUuid = body.uuid;
        console.log('Captured captcha UUID:', captchaUuid);
      } catch (e) {}
    }
    if (url.includes('/api/login')) {
      try {
        const body = await resp.text();
        console.log('NET POST', url, resp.status(), body.substring(0, 200));
      } catch (e) {}
    }
  });

  await page.goto('http://localhost:5174/#/pages/login/index');
  await page.waitForTimeout(2500);

  const code = captchaUuid ? getRedisCode(captchaUuid) : null;
  console.log('Captcha code from Redis:', code);

  await page.fill('input[type="text"]', '4523570155');
  await page.fill('input[type="password"]', 'admin123');
  const captchaInput = page.locator('.captcha-input input').first();
  await captchaInput.fill(code || '0000');

  console.log('Clicking login...');
  await page.click('button:has-text("登录"), .login-btn');
  await page.waitForTimeout(4000);

  console.log('URL:', page.url());
  const text = await page.innerText('body');
  console.log(text.substring(0, 1200));
  await browser.close();
})();
