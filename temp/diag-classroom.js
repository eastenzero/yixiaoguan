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

  // Go to classroom apply
  await page.goto('http://localhost:5174/#/pages/apply/classroom');
  await page.waitForTimeout(3000);

  // Try to set form values via Vue component
  const formSet = await page.evaluate(() => {
    const uniPage = document.querySelector('uni-page');
    if (!uniPage) return 'no uni-page';
    // Walk up to find Vue component instance
    let inst = uniPage.__vueParentComponent;
    if (!inst) return 'no __vueParentComponent';
    // Try to find form data in ctx
    const ctx = inst.ctx;
    if (ctx.form) {
      // Set values directly
      ctx.form.classroomId = 1;
      ctx.form.date = '2026-04-03';
      ctx.form.startTime = '10:00';
      ctx.form.endTime = '12:00';
      ctx.form.peopleCount = 10;
      ctx.form.phone = '13800138000';
      ctx.form.purpose = '测试申请';
      return 'form set ok';
    }
    return 'no form in ctx';
  });
  console.log('Vue form set result:', formSet);

  await page.waitForTimeout(500);

  // Click submit
  let submitResponse = null;
  page.on('response', async resp => {
    const url = resp.url();
    if (url.includes('/api/v1/classroom-applications') && resp.request().method() === 'POST') {
      try {
        submitResponse = { url, status: resp.status(), body: await resp.text() };
      } catch(e){}
    }
  });

  await page.locator('button:has-text("提交申请"), .submit-btn').first().click();
  await page.waitForTimeout(3000);

  const text = await page.innerText('body');
  console.log('\n=== AFTER SUBMIT ===');
  console.log(text.substring(0, 1500));

  if (submitResponse) {
    console.log('\n=== SUBMIT API ===');
    console.log('Status:', submitResponse.status);
    console.log('Body:', submitResponse.body.substring(0, 500));
  } else {
    console.log('\nNo submit API response captured');
  }

  await page.screenshot({ path: 'C:/Users/Administrator/Documents/code/yixiaoguan/temp/diag-classroom-submit2.png', fullPage: true });
  console.log('Screenshot saved');
  await browser.close();
})();
