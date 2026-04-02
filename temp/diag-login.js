const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  
  await page.route('**/api/captchaImage', async route => {
    route.fulfill({ status: 200, body: JSON.stringify({ msg: '操作成功', img: '', uuid: 'test' }), headers: { 'content-type': 'application/json' } });
  });
  await page.route('**/api/login', async route => {
    const postData = route.request().postData();
    console.log('LOGIN REQUEST BODY:', postData);
    route.fulfill({ status: 200, body: JSON.stringify({ code: 500, msg: 'debug' }), headers: { 'content-type': 'application/json' } });
  });
  
  page.on('requestfinished', async req => {
    if (req.url().includes('login')) {
      const resp = await req.response();
      console.log('LOGIN RESPONSE:', resp.status(), await resp.text());
    }
  });
  
  await page.goto('http://localhost:5174/#/pages/login/index');
  await page.waitForTimeout(1500);
  
  await page.fill('input[type="text"]', '4523570155');
  await page.fill('input[type="password"]', 'admin123');
  await page.fill('.captcha-input input', '1234');
  
  const formValues = await page.evaluate(() => {
    const uniPage = document.querySelector('uni-page');
    if (uniPage && uniPage.__vueParentComponent) {
      return uniPage.__vueParentComponent.ctx.form;
    }
    return null;
  });
  console.log('Vue form values:', formValues);
  
  await page.click('button:has-text("登录"), .login-btn');
  await page.waitForTimeout(2000);
  await browser.close();
})();
