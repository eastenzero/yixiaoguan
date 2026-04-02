#!/usr/bin/env node
/**
 * 学生移动端 AI 对话功能测试脚本 (Node.js + Playwright)
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

// 配置
const BASE_URL = 'http://localhost:5174';
const CHAT_URL = `${BASE_URL}/pages/chat/index`;
const LOGIN_URL = `${BASE_URL}/pages/login/index`;
const TEST_ACCOUNT = '4523570155';
const TEST_PASSWORD = 'admin123';

// 截图保存目录
const SCREENSHOT_DIR = path.join(__dirname, '..', 'docs', 'test-reports', 'student-chat-test');
if (!fs.existsSync(SCREENSHOT_DIR)) {
  fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
}

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function testStudentChat() {
  console.log('=== 学生移动端 AI 对话功能测试 ===\n');
  
  // 启动浏览器
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 375, height: 812 }
  });
  const page = await context.newPage();
  
  try {
    // ========== 步骤 1: 访问登录页面 ==========
    console.log('步骤 1: 访问登录页面');
    await page.goto(LOGIN_URL, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '01-login-page.png') });
    console.log('✓ 登录页面截图已保存');
    
    // ========== 步骤 2: 填写登录信息 ==========
    console.log('\n步骤 2: 填写登录信息');
    
    // 等待页面完全加载
    await page.waitForLoadState('domcontentloaded');
    await delay(1000);
    
    // 使用更通用的选择器
    const inputs = await page.locator('input').all();
    console.log(`找到 ${inputs.length} 个输入框`);
    
    // 填写学号（第一个输入框）
    if (inputs.length > 0) {
      await inputs[0].fill(TEST_ACCOUNT);
      console.log(`✓ 填写学号: ${TEST_ACCOUNT}`);
    }
    
    // 填写密码（第二个输入框）
    if (inputs.length > 1) {
      await inputs[1].fill(TEST_PASSWORD);
      console.log(`✓ 填写密码: ${'*'.repeat(TEST_PASSWORD.length)}`);
    }
    
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '02-form-filled.png') });
    console.log('✓ 表单填写截图已保存');
    
    // 保存验证码图片
    const captchaElement = page.locator('.captcha-img');
    await captchaElement.screenshot({ path: path.join(SCREENSHOT_DIR, 'captcha-image.png') });
    console.log('✓ 验证码图片已保存');
    
    console.log('\n步骤 3: 识别并填写验证码');
    
    // 读取验证码图片并识别
    // 当前验证码是数学表达式 "5+2=?"
    // 我们需要通过 OCR 或手动识别
    // 这里为了测试，我们先读取当前显示的验证码
    
    // 由于验证码是动态生成的，我们需要等待验证码加载完成
    await delay(500);
    
    // 重新获取验证码截图
    await captchaElement.screenshot({ path: path.join(SCREENSHOT_DIR, 'captcha-current.png') });
    
    // 注意：这里需要 OCR 识别验证码
    // 由于当前验证码是 "5+2=?", 答案是 7
    // 实际测试时需要根据当前显示的验证码填写正确答案
    
    // 先尝试使用固定值 7 (5+2=7)，但需要注意验证码可能已经刷新
    // 让我们先查看当前的验证码是什么
    
    // 从页面获取验证码图片的 src
    const captchaSrc = await captchaElement.getAttribute('src');
    if (captchaSrc) {
      console.log('✓ 验证码图片已加载');
    }
    
    // 由于无法自动识别验证码，我们尝试使用后端 API 直接登录
    // 或者跳过登录测试，直接基于代码分析进行测试报告
    
    console.log('\n注意：验证码需要手动识别');
    console.log(`当前验证码图片: ${path.join(SCREENSHOT_DIR, 'captcha-current.png')}`);
    console.log('由于验证码是动态生成的，自动化测试受限');
    
    // 尝试填写验证码并登录
    // 注意：这里填写的是之前截图中的验证码答案，可能已经过期
    const captchaAnswer = '7'; // 假设当前验证码仍是 5+2=?
    if (inputs.length > 2) {
      await inputs[2].fill(captchaAnswer);
      console.log(`✓ 尝试填写验证码: ${captchaAnswer}`);
    }
    
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '03-captcha-filled.png') });
    console.log('✓ 验证码填写截图已保存');
    
    // 点击登录按钮
    console.log('\n步骤 4: 点击登录');
    await page.click('.login-btn');
    await delay(3000);
    
    // 检查是否登录成功
    const currentUrl = page.url();
    console.log(`当前页面: ${currentUrl}`);
    
    if (currentUrl.includes('/home') || currentUrl.includes('/chat')) {
      console.log('✓ 登录成功！');
      
      // 继续测试聊天功能
      await testChatFunctionality(page);
    } else {
      console.log('✗ 登录失败，仍在登录页面');
      await page.screenshot({ path: path.join(SCREENSHOT_DIR, '03-login-failed.png') });
      
      // 检查是否有错误提示
      const toastVisible = await page.locator('.uni-toast').isVisible().catch(() => false);
      if (toastVisible) {
        const toastText = await page.locator('.uni-toast').textContent();
        console.log(`错误提示: ${toastText}`);
      }
    }
    
  } catch (error) {
    console.error('测试出错:', error);
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, 'error-screenshot.png') });
  } finally {
    await browser.close();
  }
}

async function testChatFunctionality(page) {
  console.log('\n=== 测试 AI 对话功能 ===\n');
  
  // ========== 进入聊天页面 ==========
  console.log('步骤 1: 进入聊天页面');
  await page.goto(CHAT_URL, { waitUntil: 'networkidle' });
  await page.screenshot({ path: path.join(SCREENSHOT_DIR, '05-chat-initial.png') });
  console.log('✓ 聊天页面初始状态截图已保存');
  
  // 检查页面元素
  const title = await page.locator('.title').textContent();
  console.log(`✓ 页面标题: ${title}`);
  
  // 检查空状态
  const emptyStateVisible = await page.locator('.empty-state').isVisible().catch(() => false);
  if (emptyStateVisible) {
    console.log('✓ 空状态显示正常');
    const emptyTitle = await page.locator('.empty-title').textContent();
    console.log(`  - 空状态标题: ${emptyTitle}`);
    
    const emptyDesc = await page.locator('.empty-desc').textContent();
    console.log(`  - 空状态描述: ${emptyDesc}`);
  }
  
  // 检查快捷问题
  const quickChips = await page.locator('.chip').count();
  console.log(`✓ 快捷问题数量: ${quickChips}`);
  
  // 显示快捷问题内容
  if (quickChips > 0) {
    const chipTexts = await page.locator('.chip').allTextContents();
    console.log(`  - 快捷问题: ${chipTexts.join(', ')}`);
  }
  
  // 检查输入框
  const inputVisible = await page.locator('.message-input').isVisible().catch(() => false);
  console.log(`✓ 输入框显示: ${inputVisible}`);
  
  // ========== 测试快捷问题 ==========
  if (quickChips > 0) {
    console.log('\n步骤 2: 测试快捷问题');
    const chip = page.locator('.chip').first;
    const chipText = await chip.textContent();
    console.log(`✓ 点击快捷问题: ${chipText}`);
    await chip.click();
    await delay(1000);
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '06-quick-question-clicked.png') });
    console.log('✓ 快捷问题点击后截图已保存');
    
    // 等待 AI 响应
    console.log('\n步骤 3: 等待 AI 响应');
    try {
      // 等待用户消息出现
      await page.waitForSelector('.message-item.user', { timeout: 5000 });
      console.log('✓ 用户消息已显示');
      
      // 等待 AI 响应（最多30秒）
      await page.waitForSelector('.message-item.assistant', { timeout: 30000 });
      console.log('✓ AI 响应已显示');
      
      // 等待流式输出完成
      await delay(5000);
      await page.screenshot({ path: path.join(SCREENSHOT_DIR, '07-ai-response.png') });
      console.log('✓ AI 响应截图已保存');
      
      // 检查 AI 消息内容
      const aiMessage = await page.locator('.message-item.assistant .message-text').textContent();
      console.log(`✓ AI 回复内容预览: ${aiMessage.substring(0, 100)}...`);
      
      // 检查是否有来源引用
      const sourcesVisible = await page.locator('.message-sources').isVisible().catch(() => false);
      console.log(`✓ 来源引用显示: ${sourcesVisible}`);
      
    } catch (e) {
      console.log(`✗ AI 响应测试失败: ${e.message}`);
      await page.screenshot({ path: path.join(SCREENSHOT_DIR, '07-ai-response-error.png') });
    }
  }
  
  // ========== 测试手动输入 ==========
  console.log('\n步骤 4: 测试手动输入');
  const testMessage = '奖学金怎么申请？';
  await page.fill('.message-input', testMessage);
  
  // 检查发送按钮是否激活
  const sendBtnActive = await page.locator('.send-btn.active').isVisible().catch(() => false);
  console.log(`✓ 发送按钮激活: ${sendBtnActive}`);
  
  await page.click('.send-btn');
  console.log(`✓ 发送消息: ${testMessage}`);
  
  await delay(1000);
  await page.screenshot({ path: path.join(SCREENSHOT_DIR, '08-manual-message-sent.png') });
  console.log('✓ 手动消息发送后截图已保存');
  
  // 等待 AI 响应
  try {
    await page.waitForSelector('.message-item.assistant', { timeout: 30000 });
    await delay(5000);
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '09-manual-response.png') });
    console.log('✓ 手动消息 AI 响应截图已保存');
    
    // 获取所有消息
    const allMessages = await page.locator('.message-item').count();
    console.log(`✓ 总消息数量: ${allMessages}`);
    
  } catch (e) {
    console.log(`✗ 手动消息测试失败: ${e.message}`);
  }
  
  // ========== 测试复制功能 ==========
  console.log('\n步骤 5: 测试复制功能');
  try {
    const copyBtn = page.locator('.copy-btn').first;
    const copyBtnVisible = await copyBtn.isVisible().catch(() => false);
    if (copyBtnVisible) {
      await copyBtn.click();
      console.log('✓ 点击复制按钮');
      await delay(500);
      
      // 检查是否有复制成功提示
      const checkIconVisible = await page.locator('.copy-btn .icon-check, .copy-btn svg[data-icon="check"]').isVisible().catch(() => false);
      console.log(`✓ 复制成功图标显示: ${checkIconVisible}`);
    } else {
      console.log('✗ 复制按钮未找到');
    }
  } catch (e) {
    console.log(`✗ 复制功能测试失败: ${e.message}`);
  }
  
  console.log('\n=== AI 对话功能测试完成 ===');
}

// 运行测试
testStudentChat().catch(console.error);
