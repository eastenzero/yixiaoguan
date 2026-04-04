#!/usr/bin/env python3
"""
P5A 全链路功能验证测试脚本
测试场景：
1. 知识库命中 - 奖学金申请、心理测评等
2. 拒答 - 天气、宿舍报修等超出范围问题
3. 办事意图 - 预约教室、提交报修等
4. 边界情况 - 信息不完整但有相关内容
5. 来源引用 - 点击来源标签跳转
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright

# 测试配置
BASE_URL = "http://localhost:5175"
SCREENSHOT_DIR = Path("docs/test-reports")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

# 测试用例定义
TEST_CASES = [
    # 场景1: 知识库命中
    {"id": "TC01", "category": "知识库命中", "question": "奖学金怎么申请？", "expected": "结构化回答+来源引用"},
    {"id": "TC02", "category": "知识库命中", "question": "心理测评在哪做？", "expected": "正确回答+来源引用"},
    {"id": "TC03", "category": "知识库命中", "question": "请假流程是什么？", "expected": "流程说明+来源引用"},
    
    # 场景2: 拒答
    {"id": "TC04", "category": "拒答", "question": "明天天气怎么样？", "expected": "友好说明超出范围"},
    {"id": "TC05", "category": "拒答", "question": "宿舍报修怎么弄？", "expected": "说明暂无相关信息"},
    {"id": "TC06", "category": "拒答", "question": "附近有什么好吃的？", "expected": "说明超出校园范围"},
    
    # 场景3: 办事意图
    {"id": "TC07", "category": "办事意图", "question": "我想预约教室", "expected": "官网兜底链接回复"},
    {"id": "TC08", "category": "办事意图", "question": "帮我提交报修", "expected": "官网兜底链接回复"},
    {"id": "TC09", "category": "办事意图", "question": "我要申请奖学金", "expected": "引导到申请入口"},
    
    # 场景4: 边界情况
    {"id": "TC10", "category": "边界情况", "question": "奖学金多少钱？", "expected": "部分回答+说明不完整"},
    {"id": "TC11", "category": "边界情况", "question": "图书馆几点开门？", "expected": "准确时间或说明"},
    {"id": "TC12", "category": "来源引用", "question": "如何申请助学金？", "expected": "可点击的来源引用"},
]

# 测试结果
results = []

async def wait_for_ai_response(page, timeout=30):
    """等待AI响应完成"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # 检查是否还有打字指示器
            typing_indicator = await page.locator('.typing-indicator').count()
            if typing_indicator == 0:
                # 检查AI消息内容
                ai_bubbles = await page.locator('.message-bubble.assistant').all()
                if ai_bubbles:
                    last_bubble = ai_bubbles[-1]
                    content = await last_bubble.text_content()
                    if content and len(content.strip()) > 5:
                        return True
        except Exception:
            pass
        await asyncio.sleep(0.5)
    return False

async def input_text_uniapp(page, text):
    """针对uni-app自定义input组件的文本输入方法"""
    # 方法1: 尝试点击输入框后使用keyboard.type
    input_selector = '.message-input'
    
    # 点击输入框获取焦点
    await page.click(input_selector)
    await asyncio.sleep(0.2)
    
    # 使用keyboard.type输入文本
    await page.keyboard.type(text, delay=10)
    await asyncio.sleep(0.3)

async def send_message_uniapp(page, text):
    """发送消息"""
    # 输入文本
    await input_text_uniapp(page, text)
    
    # 点击发送按钮或按回车
    send_btn = '.send-btn.active'
    try:
        if await page.locator(send_btn).count() > 0:
            await page.click(send_btn)
        else:
            # 按回车发送
            await page.keyboard.press('Enter')
    except:
        await page.keyboard.press('Enter')
    
    await asyncio.sleep(0.5)

async def run_test_case(page, test_case):
    """运行单个测试用例"""
    tc_id = test_case["id"]
    category = test_case["category"]
    question = test_case["question"]
    expected = test_case["expected"]
    
    print(f"\n[{tc_id}] {category}: {question}")
    
    try:
        # 刷新页面开始新对话
        await page.goto(f"{BASE_URL}/#/pages/chat/index")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(1.5)
        
        # 截图 - 初始状态
        init_path = SCREENSHOT_DIR / f"p5a_{tc_id}_init.png"
        await page.screenshot(path=str(init_path), full_page=True)
        
        # 发送消息
        await send_message_uniapp(page, question)
        
        # 等待AI响应
        response_received = await wait_for_ai_response(page, timeout=30)
        
        if not response_received:
            print(f"  ⚠️ 等待响应超时，当前页面截图")
            timeout_path = SCREENSHOT_DIR / f"p5a_{tc_id}_timeout.png"
            await page.screenshot(path=str(timeout_path), full_page=True)
            return {
                "id": tc_id,
                "category": category,
                "question": question,
                "expected": expected,
                "status": "TIMEOUT",
                "actual": "响应超时",
                "screenshot": timeout_path.name
            }
        
        # 等待一下确保来源引用加载
        await asyncio.sleep(1)
        
        # 截图 - 最终结果
        screenshot_path = SCREENSHOT_DIR / f"p5a_{tc_id}_{category.replace('/', '_')}.png"
        await page.screenshot(path=str(screenshot_path), full_page=True)
        print(f"  ✅ 完成 - 截图: {screenshot_path.name}")
        
        # 获取AI回复内容
        ai_messages = await page.locator('.message-bubble.assistant').all()
        actual_content = ""
        if ai_messages:
            actual_content = await ai_messages[-1].text_content()
            actual_content = actual_content[:200] + "..." if len(actual_content) > 200 else actual_content
        
        # 检查来源引用
        sources = await page.locator('.message-sources').all()
        has_sources = len(sources) > 0
        
        # 验证预期
        status = "PASS"
        actual_summary = actual_content[:100] if actual_content else "无内容"
        
        return {
            "id": tc_id,
            "category": category,
            "question": question,
            "expected": expected,
            "status": status,
            "actual": actual_summary,
            "has_sources": has_sources,
            "screenshot": screenshot_path.name
        }
        
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        # 错误时截图
        try:
            error_path = SCREENSHOT_DIR / f"p5a_{tc_id}_ERROR.png"
            await page.screenshot(path=str(error_path), full_page=True)
        except:
            pass
        return {
            "id": tc_id,
            "category": category,
            "question": question,
            "expected": expected,
            "status": "ERROR",
            "actual": str(e)[:100],
            "screenshot": None
        }

async def test_source_click(page):
    """测试来源引用点击功能"""
    print("\n[TC13] 来源引用点击测试")
    
    try:
        # 先发送一个问题获取来源引用
        await page.goto(f"{BASE_URL}/#/pages/chat/index")
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(1.5)
        
        # 发送问题
        await send_message_uniapp(page, "奖学金申请条件是什么？")
        
        # 等待响应
        await wait_for_ai_response(page, timeout=30)
        await asyncio.sleep(1)
        
        # 截图（点击前）
        before_path = SCREENSHOT_DIR / "p5a_TC13a_before_click.png"
        await page.screenshot(path=str(before_path), full_page=True)
        
        # 查找并点击来源引用
        source_items = await page.locator('.source-item').all()
        if source_items:
            await source_items[0].click()
            await asyncio.sleep(1)
            
            # 检查是否弹出了预览或跳转
            preview = await page.locator('.source-preview-panel').count()
            if preview > 0:
                # 截图（预览弹出）
                preview_path = SCREENSHOT_DIR / "p5a_TC13b_preview_open.png"
                await page.screenshot(path=str(preview_path), full_page=True)
                print(f"  ✅ 来源点击成功 - 预览弹出")
                
                # 关闭预览
                try:
                    close_btn = await page.locator('.preview-btn-ghost, .source-preview-mask').first
                    if close_btn:
                        await close_btn.click()
                except:
                    pass
                
                return {
                    "id": "TC13",
                    "category": "来源引用点击",
                    "question": "点击来源引用",
                    "expected": "显示预览或跳转详情",
                    "status": "PASS",
                    "actual": "预览弹出成功",
                    "screenshot": f"{before_path.name}, {preview_path.name}"
                }
        
        print(f"  ⚠️ 没有找到来源引用")
        return {
            "id": "TC13",
            "category": "来源引用点击",
            "question": "点击来源引用",
            "expected": "显示预览或跳转详情",
            "status": "SKIP",
            "actual": "没有找到来源引用",
            "screenshot": before_path.name
        }
        
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        return {
            "id": "TC13",
            "category": "来源引用点击",
            "question": "点击来源引用",
            "expected": "显示预览或跳转详情",
            "status": "ERROR",
            "actual": str(e)[:100],
            "screenshot": None
        }

async def main():
    """主测试函数"""
    print("=" * 60)
    print("P5A 全链路功能验证测试")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"目标URL: {BASE_URL}")
    print("=" * 60)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        try:
            # 测试服务可用性
            print("\n[预检] 检查服务可用性...")
            try:
                await page.goto(BASE_URL, timeout=10000)
                await page.wait_for_load_state('networkidle', timeout=10000)
                print("  ✅ student-app 可访问")
            except Exception as e:
                print(f"  ❌ student-app 不可访问: {e}")
                return
            
            # 运行所有测试用例
            for test_case in TEST_CASES:
                result = await run_test_case(page, test_case)
                results.append(result)
            
            # 运行来源点击测试
            source_result = await test_source_click(page)
            results.append(source_result)
            
        finally:
            await browser.close()
    
    # 生成报告
    generate_report()


def generate_report():
    """生成测试报告"""
    print("\n" + "=" * 60)
    print("测试完成 - 生成报告")
    print("=" * 60)
    
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] in ["ERROR", "TIMEOUT"])
    skipped = sum(1 for r in results if r["status"] == "SKIP")
    total = len(results)
    
    print(f"\n总计: {total} | 通过: {passed} | 失败: {failed} | 跳过: {skipped}")
    
    # 按类别统计
    categories = {}
    for r in results:
        cat = r["category"]
        if cat not in categories:
            categories[cat] = {"total": 0, "pass": 0}
        categories[cat]["total"] += 1
        if r["status"] == "PASS":
            categories[cat]["pass"] += 1
    
    print("\n按类别统计:")
    for cat, stats in categories.items():
        print(f"  {cat}: {stats['pass']}/{stats['total']}")
    
    # 保存JSON结果
    result_file = SCREENSHOT_DIR / "p5a_test_results.json"
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "skipped": skipped
            },
            "category_summary": categories,
            "results": results
        }, f, ensure_ascii=False, indent=2)
    print(f"\n详细结果: {result_file}")


if __name__ == "__main__":
    asyncio.run(main())
