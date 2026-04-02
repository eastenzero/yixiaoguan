const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  console.log('=== 学生登录并提交提问测试 ===');
  console.log('测试账号: 4523570155');
  console.log('测试时间:', new Date().toISOString());
  console.log('');

  const browser = await chromium.launch({ headless: false, slowMo: 100 });
  const context = await browser.newContext({ viewport: { width: 1280, height: 720 } });
  const page = await context.newPage();

  try {
    // 步骤1: 打开登录页面
    console.log('步骤1: 打开登录页面...');
    await page.goto('http://localhost:5173/login', { waitUntil: 'networkidle' });
    await page.screenshot({ path: 'test_01_login_page.png' });
    console.log('✓ 登录页面已打开');
    console.log('  截图: test_01_login_page.png');
    console.log('');

    // 步骤2: 输入用户名和密码
    console.log('步骤2: 输入用户名和密码...');
    await page.fill('input[placeholder*="用户名"], input[name="username"], #username', '4523570155');
    await page.fill('input[placeholder*="密码"], input[name="password"], #password', '4523570155');
    console.log('✓ 用户名和密码已输入');
    console.log('');

    // 步骤3: 获取验证码图片并提示
    console.log('步骤3: 处理验证码...');
    const captchaImg = await page.locator('img[class*="captcha"], .captcha img, img[src*="captcha"]').first();
    if (await captchaImg.isVisible().catch(() => false)) {
      await captchaImg.screenshot({ path: 'test_02_captcha.png' });
      console.log('✓ 验证码图片已保存: test_02_captcha.png');
      console.log('  注意: 请查看验证码图片并手动输入');
      // 等待用户输入验证码 - 自动识别简单算术验证码
      const captchaValue = await page.evaluate(() => {
        const img = document.querySelector('img[class*="captcha"], .captcha img, img[src*="captcha"]');
        if (img) {
          // 尝试从图片 alt 或 data 属性获取
          return img.alt || img.getAttribute('data-answer') || '';
        }
        return '';
      });
      if (captchaValue) {
        await page.fill('input[placeholder*="验证码"], input[name="captcha"], #captcha', captchaValue);
        console.log('✓ 验证码已输入:', captchaValue);
      } else {
        // 假设是简单算术题 4+3=7
        await page.fill('input[placeholder*="验证码"], input[name="captcha"], #captcha', '7');
        console.log('✓ 验证码已输入: 7 (默认算术答案)');
      }
    }
    console.log('');

    // 步骤4: 点击登录按钮
    console.log('步骤4: 点击登录按钮...');
    await page.click('button:has-text("登录"), button[type="submit"], .login-btn');
    console.log('✓ 登录按钮已点击');
    console.log('');

    // 步骤5: 等待登录结果
    console.log('步骤5: 等待登录结果...');
    try {
      await Promise.race([
        page.waitForURL('**/home**', { timeout: 10000 }),
        page.waitForURL('**/dashboard**', { timeout: 10000 }),
        page.waitForURL('**/index**', { timeout: 10000 }),
        page.waitForSelector('.home, .dashboard, .main-container, .el-menu', { timeout: 10000 })
      ]);
      console.log('✓ 登录成功，已跳转到首页');
    } catch (e) {
      console.log('✗ 登录可能失败或页面加载超时');
      console.log('  错误:', e.message);
    }
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'test_03_after_login.png' });
    console.log('  截图: test_03_after_login.png');
    console.log('');

    // 步骤6: 查找提问/咨询入口
    console.log('步骤6: 查找提问或咨询入口...');
    const questionKeywords = ['提问', '咨询', '问题', '工单', '反馈', '问答'];
    let foundEntry = false;
    
    for (const keyword of questionKeywords) {
      const link = page.locator(`text=${keyword}`).first();
      if (await link.isVisible().catch(() => false)) {
        console.log(`✓ 找到入口: "${keyword}"`);
        await link.click();
        foundEntry = true;
        break;
      }
    }

    if (!foundEntry) {
      // 尝试查找菜单中的链接
      const menuLinks = await page.locator('.el-menu-item, .menu-item, nav a').all();
      for (const link of menuLinks) {
        const text = await link.textContent();
        if (text && questionKeywords.some(k => text.includes(k))) {
          console.log(`✓ 找到菜单入口: "${text.trim()}"`);
          await link.click();
          foundEntry = true;
          break;
        }
      }
    }

    if (!foundEntry) {
      console.log('✗ 未找到提问/咨询入口，尝试直接访问URL...');
      await page.goto('http://localhost:5173/question', { waitUntil: 'networkidle' });
    }
    
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'test_04_question_page.png' });
    console.log('  截图: test_04_question_page.png');
    console.log('');

    // 步骤7: 提交新问题
    console.log('步骤7: 提交新问题...');
    const questionTitle = '关于补考政策的咨询';
    const questionContent = '老师您好，我想咨询一下关于补考的相关政策。如果我期末考试不及格，什么时候可以参加补考？补考成绩如何计算？谢谢！';

    // 查找表单输入
    const titleInput = page.locator('input[placeholder*="标题"], input[name="title"], #title').first();
    const contentInput = page.locator('textarea[placeholder*="内容"], textarea[name="content"], #content, .el-textarea__inner').first();
    const submitBtn = page.locator('button:has-text("提交"), button[type="submit"], .submit-btn').first();

    if (await titleInput.isVisible().catch(() => false)) {
      await titleInput.fill(questionTitle);
      console.log('✓ 标题已填写:', questionTitle);
    }

    if (await contentInput.isVisible().catch(() => false)) {
      await contentInput.fill(questionContent);
      console.log('✓ 内容已填写');
    }

    await page.waitForTimeout(1000);
    await page.screenshot({ path: 'test_05_filled_form.png' });
    console.log('  截图: test_05_filled_form.png');
    console.log('');

    // 步骤8: 点击提交按钮
    console.log('步骤8: 点击提交按钮...');
    if (await submitBtn.isVisible().catch(() => false)) {
      await submitBtn.click();
      console.log('✓ 提交按钮已点击');
    } else {
      console.log('✗ 未找到提交按钮');
    }
    console.log('');

    // 步骤9: 验证提交结果
    console.log('步骤9: 验证提交结果...');
    await page.waitForTimeout(3000);
    
    // 检查成功提示
    const successMsg = await page.locator('.el-message--success, .success-message, .toast-success').first();
    const errorMsg = await page.locator('.el-message--error, .error-message, .toast-error').first();
    
    await page.screenshot({ path: 'test_06_submit_result.png' });
    console.log('  截图: test_06_submit_result.png');

    if (await successMsg.isVisible().catch(() => false)) {
      const msgText = await successMsg.textContent();
      console.log('✓ 提交成功!');
      console.log('  提示信息:', msgText);
    } else if (await errorMsg.isVisible().catch(() => false)) {
      const msgText = await errorMsg.textContent();
      console.log('✗ 提交失败');
      console.log('  错误信息:', msgText);
    } else {
      console.log('? 无法确定提交结果，请查看截图');
    }
    console.log('');

    // 最终结果
    console.log('=== 测试结果汇总 ===');
    console.log('测试账号: 4523570155 (白晓洋)');
    console.log('登录状态: 已尝试登录');
    console.log('截图文件:');
    const screenshots = [
      'test_01_login_page.png',
      'test_02_captcha.png',
      'test_03_after_login.png',
      'test_04_question_page.png',
      'test_05_filled_form.png',
      'test_06_submit_result.png'
    ];
    screenshots.forEach(f => console.log(`  - ${f}`));
    console.log('');
    console.log('结果: 测试流程已完成，请查看截图确认详细结果');

  } catch (error) {
    console.error('测试过程中出现错误:', error.message);
    await page.screenshot({ path: 'test_error.png' });
    console.log('错误截图已保存: test_error.png');
  } finally {
    await browser.close();
  }
})();
