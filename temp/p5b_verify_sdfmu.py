"""p5b 验证脚本：确认办事意图回复含 sdfmu.edu.cn"""
import asyncio
import json
from playwright.async_api import async_playwright

BASE_URL = "http://localhost:5174"
LOGIN_URL = "http://localhost:8080/login"
RESULTS = []

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # 1. 打开学生端并登录
        await page.goto(f"{BASE_URL}/#/pages/login/index", wait_until="networkidle")
        await asyncio.sleep(2)

        # 尝试填写用户名密码
        try:
            await page.fill("input[type='text'], uni-input input, .username-input input", "student001")
            await page.fill("input[type='password'], uni-input.password input", "student123")
            await page.click("button.submit-btn, .login-btn, button[type='submit']")
            await asyncio.sleep(3)
        except Exception as e:
            print(f"Login UI error: {e}")

        # 2. 导航到聊天页面
        await page.goto(f"{BASE_URL}/#/pages/chat/index", wait_until="networkidle")
        await asyncio.sleep(2)

        # 3. 发送"我想预约教室"
        test_questions = [
            ("我想预约教室", "sdfmu.edu.cn"),
            ("帮我提交报修", "sdfmu.edu.cn"),
        ]

        for question, expected_keyword in test_questions:
            try:
                # 清空输入框并输入问题
                input_sel = "textarea, input[type='text'], .chat-input, uni-input input"
                await page.click(input_sel)
                await page.keyboard.type(question)
                await asyncio.sleep(0.5)

                # 发送
                await page.keyboard.press("Enter")
                await asyncio.sleep(5)  # 等待响应

                # 获取最后一条 AI 消息
                page_content = await page.content()
                has_link = "sdfmu.edu.cn" in page_content

                screenshot_path = f"docs/test-reports/p5b_verify_{question[:4]}.png"
                await page.screenshot(path=screenshot_path)

                RESULTS.append({
                    "question": question,
                    "expected": expected_keyword,
                    "found": has_link,
                    "status": "PASS" if has_link else "FAIL",
                    "screenshot": screenshot_path
                })
                print(f"[{'PASS' if has_link else 'FAIL'}] '{question}' -> sdfmu.edu.cn found: {has_link}")

            except Exception as e:
                RESULTS.append({
                    "question": question,
                    "expected": expected_keyword,
                    "found": False,
                    "status": "ERROR",
                    "error": str(e)
                })
                print(f"[ERROR] '{question}': {e}")

        await browser.close()

    # 输出结果
    print("\n=== 验证结果 ===")
    for r in RESULTS:
        print(json.dumps(r, ensure_ascii=False))

    pass_count = sum(1 for r in RESULTS if r["status"] == "PASS")
    print(f"\n通过: {pass_count}/{len(RESULTS)}")
    return pass_count == len(RESULTS)

if __name__ == "__main__":
    result = asyncio.run(main())
    exit(0 if result else 1)
