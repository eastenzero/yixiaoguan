#!/usr/bin/env python3
"""
AC-7: H5 前端登录验证脚本 V2
改进的选择器策略
"""

import sys
import time
from playwright.sync_api import sync_playwright

def verify_h5_login():
    """验证 H5 登录功能"""
    
    print("=" * 60)
    print("AC-7: H5 前端登录验证 V2")
    print("=" * 60)
    
    h5_url = "http://192.168.100.165:5174"
    test_username = "2524010001"
    test_password = "2524010001"
    
    results = {
        'page_accessible': False,
        'login_form_found': False,
        'login_attempted': False,
        'login_success': False,
        'error_message': None
    }
    
    try:
        with sync_playwright() as p:
            print("\n[1/6] 启动浏览器...")
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={'width': 390, 'height': 844},
                user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15'
            )
            page = context.new_page()
            
            print(f"\n[2/6] 访问: {h5_url}")
            response = page.goto(h5_url, timeout=15000, wait_until='networkidle')
            print(f"✅ 状态码: {response.status}")
            results['page_accessible'] = True
            
            time.sleep(2)
            page.screenshot(path='temp/h5_step1_page.png')
            
            print("\n[3/6] 查找并填写表单...")
            
            # 获取页面所有输入框
            inputs = page.query_selector_all('input')
            print(f"找到 {len(inputs)} 个输入框")
            
            username_filled = False
            password_filled = False
            
            for i, input_elem in enumerate(inputs):
                input_type = input_elem.get_attribute('type') or ''
                placeholder = input_elem.get_attribute('placeholder') or ''
                print(f"  输入框 {i+1}: type={input_type}, placeholder={placeholder}")
                
                if input_type == 'text' or 'username' in placeholder.lower() or '账号' in placeholder or '学号' in placeholder:
                    if not username_filled:
                        input_elem.fill(test_username)
                        print(f"  ✅ 填写用户名")
                        username_filled = True
                elif input_type == 'password' or '密码' in placeholder:
                    if not password_filled:
                        input_elem.fill(test_password)
                        print(f"  ✅ 填写密码")
                        password_filled = True
            
            if username_filled and password_filled:
                results['login_form_found'] = True
                page.screenshot(path='temp/h5_step2_filled.png')
                
                print("\n[4/6] 查找登录按钮...")
                
                # 尝试多种方式查找按钮
                button_found = False
                
                # 方法1: 查找所有按钮
                buttons = page.query_selector_all('button')
                print(f"找到 {len(buttons)} 个按钮")
                
                for i, btn in enumerate(buttons):
                    btn_text = btn.inner_text().strip()
                    print(f"  按钮 {i+1}: '{btn_text}'")
                    
                    if '登录' in btn_text or '登 录' in btn_text or 'login' in btn_text.lower():
                        print(f"  ✅ 找到登录按钮")
                        button_found = True
                        
                        print("\n[5/6] 点击登录...")
                        btn.click()
                        results['login_attempted'] = True
                        break
                
                # 方法2: 如果没找到button，尝试view/div等元素
                if not button_found:
                    print("  尝试查找其他可点击元素...")
                    clickables = page.query_selector_all('[class*="button"], [class*="btn"], view[class*="login"]')
                    print(f"  找到 {len(clickables)} 个可能的按钮元素")
                    
                    for elem in clickables:
                        elem_text = elem.inner_text().strip() if elem.inner_text() else ''
                        if '登录' in elem_text:
                            print(f"  ✅ 找到登录元素: {elem_text}")
                            elem.click()
                            results['login_attempted'] = True
                            button_found = True
                            break
                
                # 方法3: 尝试提交表单
                if not button_found:
                    print("  尝试直接提交表单...")
                    forms = page.query_selector_all('form')
                    if forms:
                        print(f"  找到 {len(forms)} 个表单，尝试提交第一个")
                        page.keyboard.press('Enter')
                        results['login_attempted'] = True
                        button_found = True
                
                if results['login_attempted']:
                    print("\n[6/6] 等待响应...")
                    time.sleep(3)
                    
                    current_url = page.url
                    print(f"当前 URL: {current_url}")
                    
                    page.screenshot(path='temp/h5_step3_after.png')
                    
                    # 检查是否有错误
                    page_text = page.inner_text('body')
                    
                    if '密码错误' in page_text or '用户不存在' in page_text or 'error' in page_text.lower():
                        print(f"❌ 检测到错误信息")
                        results['error_message'] = "登录失败"
                    elif current_url != h5_url and '/login' not in current_url.lower():
                        print(f"✅ URL 已变化，登录可能成功")
                        results['login_success'] = True
                    elif '首页' in page_text or '主页' in page_text or 'home' in page_text.lower():
                        print(f"✅ 检测到首页内容")
                        results['login_success'] = True
                    else:
                        print(f"⚠️ 无法确定登录状态")
                        # 保存页面内容用于调试
                        with open('temp/h5_page_content.txt', 'w', encoding='utf-8') as f:
                            f.write(page_text[:1000])
                else:
                    results['error_message'] = "未找到登录按钮"
            else:
                results['error_message'] = "表单填写不完整"
            
            browser.close()
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        results['error_message'] = str(e)
    
    return results

def main():
    results = verify_h5_login()
    
    print("\n" + "=" * 60)
    print("验证结果")
    print("=" * 60)
    print(f"页面可访问: {'✅' if results['page_accessible'] else '❌'}")
    print(f"登录表单: {'✅' if results['login_form_found'] else '❌'}")
    print(f"尝试登录: {'✅' if results['login_attempted'] else '❌'}")
    print(f"登录成功: {'✅' if results['login_success'] else '❌'}")
    
    if results['error_message']:
        print(f"\n错误: {results['error_message']}")
    
    if results['login_success']:
        print("\n✅ AC-7 验证通过")
        return 0
    elif results['login_attempted']:
        print("\n⚠️ AC-7 部分通过（已尝试登录，但无法确认成功）")
        return 1
    else:
        print("\n❌ AC-7 验证失败")
        return 2

if __name__ == '__main__':
    sys.exit(main())
