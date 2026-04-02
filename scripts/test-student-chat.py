#!/usr/bin/env python3
"""
学生移动端 AI 对话功能测试脚本
"""
import asyncio
from playwright.async_api import async_playwright
import os

# 配置
BASE_URL = "http://localhost:5174"
CHAT_URL = f"{BASE_URL}/pages/chat/index"
LOGIN_URL = f"{BASE_URL}/pages/login/index"
TEST_ACCOUNT = "4523570155"
TEST_PASSWORD = "admin123"

# 截图保存目录
SCREENSHOT_DIR = "docs/test-reports/student-chat-test"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


async def test_student_chat():
    """测试学生移动端 AI 对话功能"""
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 375, 'height': 812})
        page = await context.new_page()
        
        print("=== 学生移动端 AI 对话功能测试 ===\n")
        
        # ========== 步骤 1: 访问登录页面 ==========
        print("步骤 1: 访问登录页面")
        await page.goto(LOGIN_URL)
        await page.wait_for_load_state('networkidle')
        await page.screenshot(path=f"{SCREENSHOT_DIR}/01-login-page.png")
        print("✓ 登录页面截图已保存")
        
        # ========== 步骤 2: 填写登录信息 ==========
        print("\n步骤 2: 填写登录信息")
        
        # 填写学号
        await page.fill('input[placeholder="请输入学号"]', TEST_ACCOUNT)
        print(f"✓ 填写学号: {TEST_ACCOUNT}")
        
        # 填写密码
        await page.fill('input[placeholder="请输入密码"]', TEST_PASSWORD)
        print(f"✓ 填写密码: {'*' * len(TEST_PASSWORD)}")
        
        # 获取验证码答案
        captcha_img = await page.locator('.captcha-img').get_attribute('src')
        print(f"✓ 验证码图片已加载")
        
        # 等待用户查看验证码（这里需要手动输入或OCR识别）
        # 由于验证码是数学表达式，我们先截图查看
        await page.screenshot(path=f"{SCREENSHOT_DIR}/02-form-filled.png")
        print("✓ 表单填写截图已保存")
        
        # 获取验证码图片并查看
        captcha_element = page.locator('.captcha-img')
        await captcha_element.screenshot(path=f"{SCREENSHOT_DIR}/captcha-image.png")
        print("✓ 验证码图片已保存")
        
        # 由于验证码需要识别，这里先暂停并显示提示
        print("\n注意: 需要手动识别验证码")
        print(f"验证码图片保存在: {SCREENSHOT_DIR}/captcha-image.png")
        
        # 尝试自动识别简单数学验证码 (格式通常是 "a+b=?" 或 "a*b=?")
        # 这里我们先读取验证码图片的 alt 或 title 属性（如果有的话）
        # 或者我们可以通过其他方式获取验证码答案
        
        # 暂时暂停，等待手动输入验证码
        # 在实际自动化中，可以集成 OCR 服务
        
        print("\n=== 登录步骤需要验证码识别，测试暂停 ===")
        print("请查看验证码图片并手动登录，然后运行后续测试")
        
        await browser.close()
        return False


async def test_chat_functionality(context):
    """测试聊天功能（需要已登录的 context）"""
    page = await context.new_page()
    
    print("\n=== 测试 AI 对话功能 ===\n")
    
    # ========== 进入聊天页面 ==========
    print("步骤 1: 进入聊天页面")
    await page.goto(CHAT_URL)
    await page.wait_for_load_state('networkidle')
    await page.screenshot(path=f"{SCREENSHOT_DIR}/05-chat-initial.png")
    print("✓ 聊天页面初始状态截图已保存")
    
    # 检查页面元素
    title = await page.locator('.title').text_content()
    print(f"✓ 页面标题: {title}")
    
    # 检查空状态
    empty_state = await page.locator('.empty-state').is_visible()
    if empty_state:
        print("✓ 空状态显示正常")
        empty_title = await page.locator('.empty-title').text_content()
        print(f"  - 空状态标题: {empty_title}")
    
    # 检查快捷问题
    quick_chips = await page.locator('.chip').count()
    print(f"✓ 快捷问题数量: {quick_chips}")
    
    # 检查输入框
    input_visible = await page.locator('.message-input').is_visible()
    print(f"✓ 输入框显示: {input_visible}")
    
    # ========== 测试快捷问题 ==========
    print("\n步骤 2: 测试快捷问题")
    chip = page.locator('.chip').first
    chip_text = await chip.text_content()
    print(f"✓ 点击快捷问题: {chip_text}")
    await chip.click()
    await page.wait_for_timeout(1000)
    await page.screenshot(path=f"{SCREENSHOT_DIR}/06-quick-question-clicked.png")
    print("✓ 快捷问题点击后截图已保存")
    
    # 等待 AI 响应
    print("\n步骤 3: 等待 AI 响应")
    try:
        # 等待消息出现
        await page.wait_for_selector('.message-item.user', timeout=5000)
        print("✓ 用户消息已显示")
        
        # 等待 AI 响应
        await page.wait_for_selector('.message-item.assistant', timeout=30000)
        print("✓ AI 响应已显示")
        
        # 等待流式输出完成
        await page.wait_for_timeout(5000)
        await page.screenshot(path=f"{SCREENSHOT_DIR}/07-ai-response.png")
        print("✓ AI 响应截图已保存")
        
        # 检查 AI 消息内容
        ai_message = await page.locator('.message-item.assistant .message-text').text_content()
        print(f"✓ AI 回复内容: {ai_message[:100]}...")
        
    except Exception as e:
        print(f"✗ AI 响应测试失败: {e}")
        await page.screenshot(path=f"{SCREENSHOT_DIR}/07-ai-response-error.png")
    
    # ========== 测试手动输入 ==========
    print("\n步骤 4: 测试手动输入")
    test_message = "奖学金怎么申请？"
    await page.fill('.message-input', test_message)
    await page.click('.send-btn')
    print(f"✓ 发送消息: {test_message}")
    
    await page.wait_for_timeout(1000)
    await page.screenshot(path=f"{SCREENSHOT_DIR}/08-manual-message-sent.png")
    print("✓ 手动消息发送后截图已保存")
    
    # 等待 AI 响应
    try:
        await page.wait_for_timeout(10000)
        await page.screenshot(path=f"{SCREENSHOT_DIR}/09-manual-response.png")
        print("✓ 手动消息 AI 响应截图已保存")
    except Exception as e:
        print(f"✗ 手动消息测试失败: {e}")
    
    await page.close()


if __name__ == "__main__":
    asyncio.run(test_student_chat())
