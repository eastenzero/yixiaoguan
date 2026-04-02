const { chromium } = require('playwright');
const fs = require('fs');

// 验证码识别函数 - 处理简单算术题
function solveCaptcha(text) {
  // 匹配数字运算符数字模式
  const match = text.match(/(\d+)\s*([\+\-\*×])\s*(\d+)/);
  if (match) {
    const num1 = parseInt(match[1]);
    const operator = match[2];
    const num2 = parseInt(match[3]);
    
    switch (operator) {
      case '+': return num1 + num2;
      case '-': return num1 - num2;
      case '*':
      case '×': return num1 * num2;
      default: return null;
    }
  }
  return null;
}

(async () => {
  console.log('========================================');
  console.log('=== 学生登录并提交提问测试 ===');
  console.log('========================================');
  console.log('测试账号: 4523570155 (白晓洋 - 放射学院 2023级)');
  console.log('测试时间:', new Date().toLocaleString());
  console.log('');

  const browser = await chromium.launch({ headless: false, slowMo: 150 });
  const context = await browser.newContext({ viewport: { width: 1280, height: 720 } });
  const page = await context.newPage();

  const testResults = {
    loginSuccess: false,
    questionPageFound: false,
    questionSubmitted: false,
    errors: []
  };

  try {
    // 步骤1: 打开登录页面
    console.log('📋 步骤1: 打开登录页面...');
    await page.goto('http://localhost:5173/login', { waitUntil: 'networkidle' });
    await page.screenshot({ path: 'test_result_01_login.png' });
    console.log('   ✅ 登录页面已打开');
    console.log('   📸 截图: test_result_01_login.png');
    console.log('');

    // 步骤2: 获取验证码并识别
    console.log('📋 步骤2: 识别验证码...');
    await page.waitForTimeout(500);
    
    // 截取验证码图片
    const captchaImg = page.locator('img[class*="captcha"], .captcha img').first();
    let captchaAnswer = null;
    
    if (await captchaImg.isVisible().catch(() => false)) {
      await captchaImg.screenshot({ path: 'test_result_02_captcha.png' });
      
      // 尝试从页面获取验证码文本（如果存在）
      const pageContent = await page.content();
      const captchaMatch = pageContent.match(/(\d+\s*[\+\-\*×]\s*\d+)/);
      
      if (captchaMatch) {
        captchaAnswer = solveCaptcha(captchaMatch[1]);
        console.log(`   ✅ 识别验证码: ${captchaMatch[1]} = ${captchaAnswer}`);
      } else {
        // 默认尝试 6-6=0 (从截图看到的验证码)
        captchaAnswer = 0;
        console.log(`   ⚠️ 无法识别验证码，尝试默认值: 0`);
      }
      console.log('   📸 截图: test_result_02_captcha.png');
    }
    console.log('');

    // 步骤3: 填写登录表单
    console.log('📋 步骤3: 填写登录表单...');
    await page.fill('input[placeholder*="用户名"]', '4523570155');
    await page.fill('input[placeholder*="密码"]', '4523570155');
    
    if (captchaAnswer !== null) {
      await page.fill('input[placeholder*="验证码"]', captchaAnswer.toString());
      console.log(`   ✅ 用户名、密码、验证码已填写 (验证码: ${captchaAnswer})`);
    } else {
      console.log('   ✅ 用户名和密码已填写');
    }
    console.log('');

    // 步骤4: 点击登录
    console.log('📋 步骤4: 点击登录按钮...');
    await page.click('button:has-text("登录")');
    console.log('   ✅ 登录按钮已点击');
    console.log('');

    // 步骤5: 等待登录结果
    console.log('📋 步骤5: 等待登录结果...');
    await page.waitForTimeout(3000);
    
    const currentUrl = page.url();
    const hasError = await page.locator('.el-form-item__error, .error-message').first().isVisible().catch(() => false);
    
    await page.screenshot({ path: 'test_result_03_logged_in.png' });
    console.log('   📸 截图: test_result_03_logged_in.png');
    
    if (!currentUrl.includes('login') && !hasError) {
      testResults.loginSuccess = true;
      console.log('   ✅ 登录成功！');
      console.log(`   📍 当前页面: ${currentUrl}`);
    } else {
      const errorText = await page.locator('.el-form-item__error, .error-message').first().textContent().catch(() => '未知错误');
      console.log('   ❌ 登录失败');
      console.log(`   ⚠️ 错误信息: ${errorText}`);
      testResults.errors.push(`登录失败: ${errorText}`);
    }
    console.log('');

    // 如果登录成功，继续测试提问功能
    if (testResults.loginSuccess) {
      // 步骤6: 查找提问入口
      console.log('📋 步骤6: 查找提问入口...');
      
      const keywords = ['提问', '咨询', '问题', '工单', '问答', '反馈'];
      let foundEntry = false;
      
      for (const keyword of keywords) {
        const link = page.locator(`text=${keyword}`).first();
        if (await link.isVisible().catch(() => false)) {
          console.log(`   ✅ 找到入口: "${keyword}"`);
          await link.click();
          foundEntry = true;
          testResults.questionPageFound = true;
          break;
        }
      }
      
      if (!foundEntry) {
        console.log('   ⚠️ 未找到明显的提问入口');
        console.log('   📝 尝试直接访问 /question 路径...');
        await page.goto('http://localhost:5173/question', { waitUntil: 'networkidle' });
      }
      
      await page.waitForTimeout(2000);
      await page.screenshot({ path: 'test_result_04_question_page.png' });
      console.log('   📸 截图: test_result_04_question_page.png');
      console.log('');

      // 步骤7: 填写提问表单
      console.log('📋 步骤7: 填写提问表单...');
      const questionTitle = '关于补考政策的咨询';
      const questionContent = '老师您好，我想咨询一下关于补考的相关政策。如果我期末考试不及格，什么时候可以参加补考？补考成绩如何计算？谢谢！';
      
      const titleInput = page.locator('input[placeholder*="标题"], input[name="title"]').first();
      const contentInput = page.locator('textarea[placeholder*="内容"], textarea[name="content"]').first();
      const categorySelect = page.locator('.el-select, select[name="category"]').first();
      const submitBtn = page.locator('button:has-text("提交"), button[type="submit"]').first();
      
      let formFilled = false;
      
      if (await titleInput.isVisible().catch(() => false)) {
        await titleInput.fill(questionTitle);
        console.log(`   ✅ 标题: ${questionTitle}`);
        formFilled = true;
      }
      
      if (await contentInput.isVisible().catch(() => false)) {
        await contentInput.fill(questionContent);
        console.log('   ✅ 内容已填写');
        formFilled = true;
      }
      
      if (await categorySelect.isVisible().catch(() => false)) {
        await categorySelect.click();
        await page.waitForTimeout(500);
        await page.locator('.el-select-dropdown__item').first().click();
        console.log('   ✅ 分类已选择');
      }
      
      await page.waitForTimeout(1000);
      await page.screenshot({ path: 'test_result_05_form_filled.png' });
      console.log('   📸 截图: test_result_05_form_filled.png');
      
      if (!formFilled) {
        console.log('   ⚠️ 未找到提问表单，可能是权限不足或页面未加载');
        testResults.errors.push('未找到提问表单');
      }
      console.log('');

      // 步骤8: 提交问题
      console.log('📋 步骤8: 提交问题...');
      if (await submitBtn.isVisible().catch(() => false)) {
        await submitBtn.click();
        console.log('   ✅ 提交按钮已点击');
        
        await page.waitForTimeout(3000);
        
        // 检查提交结果
        const successMsg = await page.locator('.el-message--success').first().isVisible().catch(() => false);
        const errorMsg = await page.locator('.el-message--error').first().isVisible().catch(() => false);
        
        await page.screenshot({ path: 'test_result_06_submit_result.png' });
        console.log('   📸 截图: test_result_06_submit_result.png');
        
        if (successMsg) {
          testResults.questionSubmitted = true;
          console.log('   ✅ 问题提交成功！');
        } else if (errorMsg) {
          const msg = await page.locator('.el-message--error').first().textContent().catch(() => '未知错误');
          console.log(`   ❌ 提交失败: ${msg}`);
          testResults.errors.push(`提交失败: ${msg}`);
        } else {
          console.log('   ⚠️ 无法确定提交结果');
        }
      } else {
        console.log('   ❌ 未找到提交按钮');
        testResults.errors.push('未找到提交按钮');
      }
    }
    
    console.log('');

  } catch (error) {
    console.error('❌ 测试过程中出现错误:', error.message);
    testResults.errors.push(error.message);
    await page.screenshot({ path: 'test_result_error.png' });
    console.log('   📸 错误截图: test_result_error.png');
  } finally {
    await browser.close();
  }

  // 输出测试报告
  console.log('========================================');
  console.log('=== 测试报告 ===');
  console.log('========================================');
  console.log('');
  console.log('📊 测试账号信息:');
  console.log('   用户名: 4523570155');
  console.log('   姓名: 白晓洋');
  console.log('   学院: 放射学院');
  console.log('   班级: 2023级医学影像技术本科4班');
  console.log('');
  console.log('📊 测试结果:');
  console.log(`   登录成功: ${testResults.loginSuccess ? '✅ 是' : '❌ 否'}`);
  console.log(`   找到提问入口: ${testResults.questionPageFound ? '✅ 是' : '❌ 否'}`);
  console.log(`   问题提交成功: ${testResults.questionSubmitted ? '✅ 是' : '❌ 否'}`);
  console.log('');
  
  if (testResults.errors.length > 0) {
    console.log('⚠️ 错误/问题:');
    testResults.errors.forEach((err, i) => console.log(`   ${i + 1}. ${err}`));
    console.log('');
  }
  
  console.log('📸 生成的截图:');
  const screenshots = [
    'test_result_01_login.png',
    'test_result_02_captcha.png', 
    'test_result_03_logged_in.png',
    'test_result_04_question_page.png',
    'test_result_05_form_filled.png',
    'test_result_06_submit_result.png'
  ];
  screenshots.forEach(f => console.log(`   - ${f}`));
  console.log('');
  
  // 最终结论
  console.log('📋 最终结论:');
  if (testResults.loginSuccess && testResults.questionSubmitted) {
    console.log('   ✅ 测试通过 - 学生可以正常登录并提交提问');
  } else if (testResults.loginSuccess && !testResults.questionSubmitted) {
    console.log('   ⚠️ 部分通过 - 学生可以登录，但提交提问存在问题');
  } else {
    console.log('   ❌ 测试失败 - 学生无法完成登录');
  }
  console.log('');
  console.log('========================================');
  
  // 保存测试报告
  const report = {
    testTime: new Date().toISOString(),
    testAccount: {
      username: '4523570155',
      name: '白晓洋',
      dept: '放射学院',
      class: '2023级医学影像技术本科4班'
    },
    results: testResults,
    screenshots: screenshots
  };
  
  fs.writeFileSync('test_report.json', JSON.stringify(report, null, 2));
  console.log('📄 测试报告已保存: test_report.json');
})();
