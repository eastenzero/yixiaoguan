const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  console.log('========================================');
  console.log('=== 学生登录并提交提问测试 ===');
  console.log('========================================');
  console.log('测试时间:', new Date().toLocaleString());
  console.log('');

  const browser = await chromium.launch({ headless: false, slowMo: 200 });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });

  const results = {
    loginSuccess: false,
    questionSubmitted: false,
    errors: []
  };

  try {
    // 1. 打开登录页面
    console.log('📋 步骤1: 打开登录页面');
    await page.goto('http://localhost:5173/login', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1000);
    await page.screenshot({ path: 'final_01_login.png' });
    console.log('   ✅ 登录页面已加载');
    console.log('');

    // 2. 填写表单
    console.log('📋 步骤2: 填写登录信息');
    
    // 用户名
    await page.fill('input[placeholder*="用户名"]', '4523570155');
    console.log('   ✅ 用户名: 4523570155');
    
    // 密码
    await page.fill('input[placeholder*="密码"]', '4523570155');
    console.log('   ✅ 密码已填写');
    
    // 验证码 - 从截图可以看到是 "4/4=?"
    // 根据历史截图，验证码可能是变化的，我们尝试识别
    await page.waitForTimeout(500);
    
    // 截图验证码区域并尝试获取答案
    // 注意: 从之前的截图看到验证码是 "4/4=?" 或 "6-6=?" 等算术题
    // 我们检查页面是否有提示
    const captchaText = await page.locator('.captcha, img[src*="captcha"]').first().getAttribute('alt').catch(() => '');
    
    // 默认使用常见的算术答案
    let captchaAnswer = '1'; // 4/4=1, 或其他常见答案
    
    // 尝试解析页面中的验证码
    const imgSrc = await page.locator('img[src*="captcha"]').first().getAttribute('src').catch(() => '');
    
    await page.fill('input[placeholder*="验证码"]', captchaAnswer);
    console.log(`   ✅ 验证码: ${captchaAnswer} (尝试值)`);
    
    await page.screenshot({ path: 'final_02_form_filled.png' });
    console.log('');

    // 3. 点击登录
    console.log('📋 步骤3: 点击登录');
    const loginBtn = page.locator('button:has-text("登录"), button[type="submit"]').first();
    
    if (await loginBtn.isVisible().catch(() => false)) {
      await loginBtn.click();
      console.log('   ✅ 登录按钮已点击');
    } else {
      console.log('   ❌ 未找到登录按钮');
      results.errors.push('未找到登录按钮');
    }
    console.log('');

    // 4. 等待结果
    console.log('📋 步骤4: 等待登录结果');
    await page.waitForTimeout(3000);
    
    const url = page.url();
    const hasLoginError = await page.locator('.el-message--error').first().isVisible().catch(() => false);
    
    await page.screenshot({ path: 'final_03_after_login.png' });
    console.log(`   📍 当前URL: ${url}`);
    
    if (!url.includes('login') && !hasLoginError) {
      results.loginSuccess = true;
      console.log('   ✅ 登录成功！');
    } else {
      const errorMsg = await page.locator('.el-message--error').first().textContent().catch(() => '未知错误');
      console.log(`   ❌ 登录失败: ${errorMsg}`);
      results.errors.push(`登录失败: ${errorMsg}`);
    }
    console.log('');

    // 5. 如果登录成功，尝试提交问题
    if (results.loginSuccess) {
      console.log('📋 步骤5: 查找提问功能');
      
      // 尝试点击"学生提问"菜单
      const menuItems = await page.locator('.el-menu-item, .menu-item').all();
      let clicked = false;
      
      for (const item of menuItems) {
        const text = await item.textContent().catch(() => '');
        if (text.includes('提问') || text.includes('咨询')) {
          await item.click();
          clicked = true;
          console.log(`   ✅ 点击菜单: ${text.trim()}`);
          break;
        }
      }
      
      if (!clicked) {
        console.log('   ⚠️ 未找到提问菜单');
      }
      
      await page.waitForTimeout(2000);
      await page.screenshot({ path: 'final_04_question_page.png' });
      console.log('');

      // 6. 填写问题
      console.log('📋 步骤6: 填写提问表单');
      
      const titleInput = page.locator('input[placeholder*="标题"]').first();
      const contentInput = page.locator('textarea').first();
      const submitBtn = page.locator('button:has-text("提交")').first();
      
      if (await titleInput.isVisible().catch(() => false)) {
        await titleInput.fill('关于补考政策的咨询');
        console.log('   ✅ 标题已填写');
        
        if (await contentInput.isVisible().catch(() => false)) {
          await contentInput.fill('老师您好，我想咨询一下关于补考的相关政策。如果我期末考试不及格，什么时候可以参加补考？补考成绩如何计算？谢谢！');
          console.log('   ✅ 内容已填写');
        }
        
        await page.waitForTimeout(1000);
        await page.screenshot({ path: 'final_05_form_ready.png' });
        
        // 提交
        if (await submitBtn.isVisible().catch(() => false)) {
          await submitBtn.click();
          console.log('   ✅ 提交按钮已点击');
          
          await page.waitForTimeout(2000);
          
          const success = await page.locator('.el-message--success').first().isVisible().catch(() => false);
          if (success) {
            results.questionSubmitted = true;
            console.log('   ✅ 提交成功！');
          } else {
            console.log('   ⚠️ 提交结果待确认');
          }
        }
      } else {
        console.log('   ⚠️ 未找到提问表单');
        results.errors.push('未找到提问表单');
      }
      
      await page.screenshot({ path: 'final_06_final.png' });
    }
    
  } catch (err) {
    console.error('❌ 错误:', err.message);
    results.errors.push(err.message);
    await page.screenshot({ path: 'final_error.png' });
  } finally {
    await browser.close();
  }

  // 输出报告
  console.log('');
  console.log('========================================');
  console.log('=== 测试报告 ===');
  console.log('========================================');
  console.log('');
  console.log('📊 测试账号: 4523570155 (白晓洋)');
  console.log('📊 测试结果:');
  console.log(`   登录成功: ${results.loginSuccess ? '✅ 通过' : '❌ 失败'}`);
  console.log(`   提问提交: ${results.questionSubmitted ? '✅ 通过' : '❌ 失败'}`);
  console.log('');
  console.log('📸 截图文件:');
  ['final_01_login.png', 'final_02_form_filled.png', 'final_03_after_login.png', 
   'final_04_question_page.png', 'final_05_form_ready.png', 'final_06_final.png'].forEach(f => {
    if (fs.existsSync(f)) console.log(`   - ${f}`);
  });
  console.log('');
  console.log('📋 结论:', results.loginSuccess ? 
    (results.questionSubmitted ? '✅ 测试通过' : '⚠️ 登录成功但提问功能存在问题') : 
    '❌ 登录失败');
  console.log('========================================');
  
  // 保存报告
  fs.writeFileSync('final_report.json', JSON.stringify(results, null, 2));
})();
