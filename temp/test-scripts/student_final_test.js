const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  console.log('========================================');
  console.log('=== 学生登录并提交提问测试 ===');
  console.log('========================================');
  console.log('测试账号: 4523570155 (白晓洋)');
  console.log('测试时间:', new Date().toLocaleString());
  console.log('');

  let browser, page;
  const results = {
    loginSuccess: false,
    questionSubmitted: false,
    errors: [],
    screenshots: []
  };

  try {
    browser = await chromium.launch({ headless: false, slowMo: 300 });
    page = await browser.newPage({ viewport: { width: 1280, height: 720 } });

    // 步骤1: 打开登录页面
    console.log('📋 步骤1: 打开登录页面');
    await page.goto('http://localhost:5173/login', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1500);
    await page.screenshot({ path: 'test_01_login.png' });
    results.screenshots.push('test_01_login.png');
    console.log('   ✅ 登录页面已加载');
    console.log('   📸 test_01_login.png');
    console.log('');

    // 步骤2: 填写登录信息
    console.log('📋 步骤2: 填写登录信息');
    
    // 填写用户名
    await page.fill('input[placeholder*="用户名"]', '4523570155');
    console.log('   ✅ 用户名: 4523570155');
    
    // 填写密码
    await page.fill('input[placeholder*="密码"]', '4523570155');
    console.log('   ✅ 密码: 4523570155');
    
    // 等待验证码加载
    await page.waitForTimeout(800);
    
    // 填写验证码 (根据截图，当前是 "2-0=?", 答案是 2)
    // 由于验证码会变化，我们使用一个合理的猜测
    const captchaAnswer = '2'; // 2-0=2
    await page.fill('input[placeholder*="验证码"]', captchaAnswer);
    console.log(`   ✅ 验证码: ${captchaAnswer}`);
    
    await page.screenshot({ path: 'test_02_filled.png' });
    results.screenshots.push('test_02_filled.png');
    console.log('   📸 test_02_filled.png');
    console.log('');

    // 步骤3: 点击登录按钮
    console.log('📋 步骤3: 点击登录按钮');
    
    // 使用多种方式定位登录按钮
    const loginBtn = page.locator('.login-btn, button.el-button--primary, button:has-text("登")').first();
    await loginBtn.waitFor({ state: 'visible', timeout: 5000 });
    await loginBtn.click();
    console.log('   ✅ 登录按钮已点击');
    console.log('');

    // 步骤4: 等待登录结果
    console.log('📋 步骤4: 等待登录结果');
    await page.waitForTimeout(4000);
    
    const currentUrl = page.url();
    const errorVisible = await page.locator('.el-message--error, .error-message').first().isVisible().catch(() => false);
    
    await page.screenshot({ path: 'test_03_result.png' });
    results.screenshots.push('test_03_result.png');
    console.log(`   📍 当前URL: ${currentUrl}`);
    
    if (!currentUrl.includes('/login') && !errorVisible) {
      results.loginSuccess = true;
      console.log('   ✅ 登录成功！');
    } else {
      const errorText = await page.locator('.el-message--error, .error-message').first().textContent().catch(() => '请检查验证码');
      console.log(`   ❌ 登录失败: ${errorText}`);
      results.errors.push(`登录失败: ${errorText}`);
    }
    console.log('');

    // 步骤5: 查找提问功能并提交问题
    if (results.loginSuccess) {
      console.log('📋 步骤5: 查找提问功能');
      
      // 尝试点击"提问"或"问答"相关菜单
      const keywords = ['提问', '问答', '咨询', '工单'];
      let foundMenu = false;
      
      for (const keyword of keywords) {
        const menuItem = page.locator(`.el-menu-item:has-text("${keyword}"), .menu-item:has-text("${keyword}")`).first();
        if (await menuItem.isVisible().catch(() => false)) {
          await menuItem.click();
          console.log(`   ✅ 点击菜单: ${keyword}`);
          foundMenu = true;
          break;
        }
      }
      
      if (!foundMenu) {
        // 尝试直接访问问答页面
        await page.goto('http://localhost:5173/question', { waitUntil: 'domcontentloaded' });
        console.log('   ⚠️ 尝试直接访问 /question');
      }
      
      await page.waitForTimeout(2000);
      await page.screenshot({ path: 'test_04_question.png' });
      results.screenshots.push('test_04_question.png');
      console.log('   📸 test_04_question.png');
      console.log('');

      // 步骤6: 填写并提交问题
      console.log('📋 步骤6: 填写提问表单');
      
      const titleInput = page.locator('input[placeholder*="标题"], input[name="title"]').first();
      const contentInput = page.locator('textarea[placeholder*="内容"], textarea[name="content"]').first();
      const submitBtn = page.locator('button:has-text("提交"), button[type="submit"]').first();
      
      if (await titleInput.isVisible().catch(() => false)) {
        await titleInput.fill('关于补考政策的咨询');
        console.log('   ✅ 标题: 关于补考政策的咨询');
        
        if (await contentInput.isVisible().catch(() => false)) {
          await contentInput.fill('老师您好，我想咨询一下关于补考的相关政策。如果我期末考试不及格，什么时候可以参加补考？补考成绩如何计算？谢谢！');
          console.log('   ✅ 内容已填写');
        }
        
        await page.waitForTimeout(1000);
        await page.screenshot({ path: 'test_05_form.png' });
        results.screenshots.push('test_05_form.png');
        console.log('   📸 test_05_form.png');
        
        // 提交
        if (await submitBtn.isVisible().catch(() => false)) {
          await submitBtn.click();
          console.log('   ✅ 提交按钮已点击');
          
          await page.waitForTimeout(3000);
          
          const success = await page.locator('.el-message--success').first().isVisible().catch(() => false);
          await page.screenshot({ path: 'test_06_submit.png' });
          results.screenshots.push('test_06_submit.png');
          console.log('   📸 test_06_submit.png');
          
          if (success) {
            results.questionSubmitted = true;
            console.log('   ✅ 问题提交成功！');
          } else {
            console.log('   ⚠️ 提交结果待确认');
          }
        } else {
          console.log('   ❌ 未找到提交按钮');
          results.errors.push('未找到提交按钮');
        }
      } else {
        console.log('   ❌ 未找到提问表单');
        results.errors.push('未找到提问表单');
      }
    }

  } catch (err) {
    console.error('❌ 错误:', err.message);
    results.errors.push(err.message);
    if (page) {
      await page.screenshot({ path: 'test_error.png' }).catch(() => {});
      results.screenshots.push('test_error.png');
    }
  } finally {
    if (browser) await browser.close();
  }

  // 输出最终报告
  console.log('');
  console.log('========================================');
  console.log('=== 测试报告 ===');
  console.log('========================================');
  console.log('');
  console.log('👤 测试账号信息:');
  console.log('   用户名: 4523570155');
  console.log('   姓名: 白晓洋');
  console.log('   学院: 放射学院');
  console.log('   班级: 2023级医学影像技术本科4班');
  console.log('');
  console.log('📊 测试结果:');
  console.log(`   登录功能: ${results.loginSuccess ? '✅ 通过' : '❌ 失败'}`);
  console.log(`   提问提交: ${results.questionSubmitted ? '✅ 通过' : results.loginSuccess ? '⚠️ 未完成' : '❌ 未测试'}`);
  console.log('');
  console.log('📸 截图文件:');
  results.screenshots.forEach(f => console.log(`   - ${f}`));
  console.log('');
  
  if (results.errors.length > 0) {
    console.log('⚠️ 错误/问题:');
    results.errors.forEach((e, i) => console.log(`   ${i + 1}. ${e}`));
    console.log('');
  }
  
  // 最终结论
  console.log('📋 最终结论:');
  if (results.loginSuccess && results.questionSubmitted) {
    console.log('   ✅ 测试通过 - 学生可以正常登录并提交提问');
  } else if (results.loginSuccess) {
    console.log('   ⚠️ 部分通过 - 登录成功，但提问功能存在问题');
  } else {
    console.log('   ❌ 测试失败 - 学生无法完成登录（可能是验证码错误或账号问题）');
  }
  console.log('');
  console.log('========================================');
  
  // 保存报告
  fs.writeFileSync('student_test_report.json', JSON.stringify(results, null, 2));
  console.log('📄 报告已保存: student_test_report.json');
})();
