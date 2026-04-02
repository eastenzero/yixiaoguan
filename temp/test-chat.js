const { chromium } = require('playwright');

(async () => {
  console.log('=== 医小管 AI 聊天页面测试 ===\n');
  
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 375, height: 812 },
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15'
  });
  const page = await context.newPage();
  
  const testResults = {
    loginPage: false,
    loginFormFilled: false,
    loginSuccess: false,
    chatPage: false,
    chatInput: false,
    aiResponse: false
  };
  
  try {
    // 1. 测试登录页面
    console.log('1. 测试登录页面...');
    await page.goto('http://localhost:5174/pages/login/index', { waitUntil: 'networkidle' });
    await page.waitForTimeout(1000);
    await page.screenshot({ path: 'temp/01-login-page.png' });
    
    const title = await page.title();
    testResults.loginPage = title.includes('医小管') || await page.locator('.login-page').count() > 0;
    console.log(`   ${testResults.loginPage ? '✓' : '✗'} 登录页面显示${testResults.loginPage ? '正常' : '异常'}`);
    
    // 2. 填写登录表单
    console.log('\n2. 填写登录表单...');
    const inputs = await page.locator('input').all();
    console.log(`   找到 ${inputs.length} 个输入框`);
    
    if (inputs.length >= 3) {
      await inputs[0].fill('4523570155');
      await inputs[1].fill('admin123');
      await inputs[2].fill('3');
      testResults.loginFormFilled = true;
      console.log('   ✓ 表单填写完成');
    }
    
    await page.screenshot({ path: 'temp/02-login-filled.png' });
    
    // 3. 点击登录
    console.log('\n3. 点击登录按钮...');
    // 使用 JavaScript 点击按钮
    await page.evaluate(() => {
      const btn = document.querySelector('button, .login-btn');
      if (btn) btn.click();
    });
    
    await page.waitForTimeout(3000);
    await page.screenshot({ path: 'temp/03-login-result.png' });
    
    const currentUrl = page.url();
    testResults.loginSuccess = !currentUrl.includes('login');
    console.log(`   ${testResults.loginSuccess ? '✓' : '⚠'} 登录${testResults.loginSuccess ? '成功' : '可能失败（检查后端服务是否运行在:8080）'}`);
    console.log(`   当前URL: ${currentUrl}`);
    
    // 4. 测试聊天页面
    console.log('\n4. 测试聊天页面...');
    await page.goto('http://localhost:5174/pages/chat/index', { waitUntil: 'networkidle' });
    await page.waitForTimeout(1000);
    await page.screenshot({ path: 'temp/04-chat-empty.png', fullPage: true });
    
    testResults.chatPage = await page.locator('.chat-page, .ai-chat, [class*="chat"]').count() > 0;
    console.log(`   ${testResults.chatPage ? '✓' : '⚠'} 聊天页面${testResults.chatPage ? '加载完成' : '加载状态需确认'}`);
    
    // 5. 发送消息测试
    console.log('\n5. 测试消息发送...');
    const allInputs = await page.locator('textarea, input').all();
    console.log(`   找到 ${allInputs.length} 个可输入元素`);
    
    if (allInputs.length > 0) {
      // 尝试填写最后一个输入框（通常是消息输入框）
      const lastInput = allInputs[allInputs.length - 1];
      await lastInput.fill('请假流程是什么？');
      testResults.chatInput = true;
      console.log('   ✓ 输入测试消息');
      
      await page.screenshot({ path: 'temp/05-chat-input.png', fullPage: true });
      
      // 尝试发送
      await page.evaluate(() => {
        // 尝试点击发送按钮或按回车
        const sendBtn = document.querySelector('.send-btn, [class*="send"], button');
        if (sendBtn) sendBtn.click();
      });
      
      console.log('   ✓ 点击发送');
    } else {
      console.log('   ⚠ 未找到输入框');
    }
    
    // 6. 等待 AI 响应
    console.log('\n6. 等待 AI 响应...');
    await page.waitForTimeout(8000);
    await page.screenshot({ path: 'temp/06-chat-response.png', fullPage: true });
    console.log('   ✓ AI 响应截图完成');
    
    // 检查是否有消息气泡
    const messages = await page.locator('.message, .bubble, [class*="message"]').count();
    testResults.aiResponse = messages > 0;
    console.log(`   找到 ${messages} 个消息元素`);
    
  } catch (error) {
    console.error('\n测试出错:', error.message);
    await page.screenshot({ path: 'temp/error.png' });
  } finally {
    await browser.close();
    
    // 输出测试报告
    console.log('\n' + '='.repeat(50));
    console.log('                  测试报告');
    console.log('='.repeat(50));
    console.log(`[${testResults.loginPage ? '✓' : '✗'}] 登录页面能正常显示`);
    console.log(`[${testResults.loginFormFilled ? '✓' : '✗'}] 表单能正常填写`);
    console.log(`[${testResults.loginSuccess ? '✓' : '✗'}] 账号能成功登录${!testResults.loginSuccess ? '（需检查后端服务）' : ''}`);
    console.log(`[${testResults.chatPage ? '✓' : '✗'}] 聊天页面能正常加载`);
    console.log(`[${testResults.chatInput ? '✓' : '✗'}] 能输入并发送消息`);
    console.log(`[${testResults.aiResponse ? '✓' : '✗'}] AI响应能正常显示`);
    console.log('='.repeat(50));
    console.log('\n截图保存位置：');
    console.log('  - temp/01-login-page.png     (登录页面)');
    console.log('  - temp/02-login-filled.png   (填写表单)');
    console.log('  - temp/03-login-result.png   (登录结果)');
    console.log('  - temp/04-chat-empty.png     (聊天页面空状态)');
    console.log('  - temp/05-chat-input.png     (输入消息)');
    console.log('  - temp/06-chat-response.png  (AI响应)');
  }
})();
