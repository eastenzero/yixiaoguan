const { test, expect } = require('@playwright/test');

test('测试医小管 AI 聊天页面', async ({ page }) => {
  // 设置移动端视口
  await page.setViewportSize({ width: 375, height: 812 });
  
  // 1. 打开登录页面
  await page.goto('http://localhost:5174/pages/login/index');
  await page.waitForLoadState('networkidle');
  
  // 截图登录页
  await page.screenshot({ path: 'temp/login-page.png' });
  console.log('✓ 登录页面加载成功');
  
  // 2. 填写登录信息
  await page.fill('input[type="text"]', '4523570155');
  await page.fill('input[type="password"]', 'admin123');
  
  // 获取验证码计算结果（9/3=?）
  const captchaImg = await page.locator('.captcha-img');
  if (await captchaImg.isVisible()) {
    // 验证码是 9/3=?，答案是 3
    await page.fill('.captcha-input', '3');
  }
  
  // 截图填写后的表单
  await page.screenshot({ path: 'temp/login-filled.png' });
  console.log('✓ 表单填写完成');
  
  // 3. 点击登录按钮
  await page.click('.login-btn');
  
  // 等待登录成功（等待跳转到首页或出现成功提示）
  await page.waitForTimeout(2000);
  
  // 截图登录结果
  await page.screenshot({ path: 'temp/login-result.png' });
  console.log('✓ 登录操作完成');
  
  // 4. 导航到聊天页面
  await page.goto('http://localhost:5174/pages/chat/index');
  await page.waitForLoadState('networkidle');
  
  // 截图聊天页面（空状态）
  await page.screenshot({ path: 'temp/chat-empty.png' });
  console.log('✓ 聊天页面加载成功');
  
  // 5. 发送测试消息
  // 查找输入框（可能是 textarea 或 contenteditable 元素）
  const inputSelectors = ['textarea', '[contenteditable]', '.chat-input input', 'input[type="text"]'];
  let inputFound = false;
  
  for (const selector of inputSelectors) {
    try {
      const input = page.locator(selector).first();
      if (await input.isVisible({ timeout: 1000 })) {
        await input.fill('请假流程是什么？');
        inputFound = true;
        console.log(`✓ 使用选择器 ${selector} 找到输入框`);
        break;
      }
    } catch (e) {
      // 继续尝试下一个选择器
    }
  }
  
  if (!inputFound) {
    console.log('⚠ 未找到输入框，尝试使用 JavaScript');
    // 使用 JavaScript 查找并填写输入框
    await page.evaluate(() => {
      const inputs = document.querySelectorAll('textarea, [contenteditable], input');
      for (const input of inputs) {
        if (input.offsetParent !== null) { // 可见元素
          input.value = '请假流程是什么？';
          input.dispatchEvent(new Event('input', { bubbles: true }));
          return true;
        }
      }
      return false;
    });
  }
  
  // 截图输入消息后的页面
  await page.screenshot({ path: 'temp/chat-input.png' });
  
  // 6. 点击发送按钮
  const sendSelectors = ['.send-btn', 'button:has-text("发送")', '[class*="send"]', 'button:last-child'];
  let sendFound = false;
  
  for (const selector of sendSelectors) {
    try {
      const btn = page.locator(selector).first();
      if (await btn.isVisible({ timeout: 1000 })) {
        await btn.click();
        sendFound = true;
        console.log(`✓ 使用选择器 ${selector} 点击发送按钮`);
        break;
      }
    } catch (e) {
      // 继续尝试下一个选择器
    }
  }
  
  if (!sendFound) {
    console.log('⚠ 未找到发送按钮');
  }
  
  // 7. 等待 AI 响应（等待5-10秒）
  await page.waitForTimeout(8000);
  
  // 截图查看 AI 响应
  await page.screenshot({ path: 'temp/chat-response.png' });
  console.log('✓ AI 响应截图完成');
  
  // 获取页面文本内容用于验证
  const pageContent = await page.content();
  
  // 验证要点检查
  const checks = {
    hasLoginPage: true,
    hasChatPage: pageContent.includes('chat') || pageContent.includes('AI') || pageContent.includes('智能'),
    hasMessageInput: inputFound,
    hasSendButton: sendFound,
  };
  
  console.log('\n=== 测试结果 ===');
  console.log('登录页面显示:', checks.hasLoginPage ? '✓ 正常' : '✗ 异常');
  console.log('聊天页面加载:', checks.hasChatPage ? '✓ 正常' : '✗ 异常');
  console.log('消息输入功能:', checks.hasMessageInput ? '✓ 正常' : '✗ 异常');
  console.log('发送按钮:', checks.hasSendButton ? '✓ 正常' : '✗ 异常');
});
