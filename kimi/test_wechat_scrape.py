#!/usr/bin/env python3
"""
WeChat Public Account Scraping Feasibility Test
Test methods to scrape content from WeChat public accounts related to 
Shandong First Medical University (山东第一医科大学)
"""

import asyncio
import json
from playwright.async_api import async_playwright

# Test configuration
SEARCH_KEYWORD = "山东第一医科大学"
OUTPUT_FILE = "kimi/wechat_test_data.json"

# Results collector
results = {
    "test_timestamp": None,
    "sogou_search": {
        "status": None,
        "accounts_found": [],
        "articles_found": [],
        "errors": []
    },
    "direct_wechat_access": {
        "status": None,
        "tested_articles": [],
        "errors": []
    },
    "anti_scraping_measures": []
}

async def test_sogou_wechat_search():
    """Test 1: Sogou WeChat Search"""
    print("=" * 60)
    print("Test 1: Sogou WeChat Search")
    print("=" * 60)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            # Navigate to Sogou WeChat search
            print("\n[Step 1] Opening Sogou WeChat search...")
            await page.goto("https://weixin.sogou.com/", wait_until="networkidle", timeout=30000)
            await asyncio.sleep(2)
            
            # Take initial screenshot
            await page.screenshot(path="kimi/test1_sogou_homepage.png")
            print("✓ Sogou WeChat search loaded successfully")
            results["sogou_search"]["status"] = "accessible"
            
            # Search for articles
            print(f"\n[Step 2] Searching for '{SEARCH_KEYWORD}' (articles)...")
            search_url = f"https://weixin.sogou.com/weixin?type=2&query={SEARCH_KEYWORD}"
            await page.goto(search_url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(3)
            
            await page.screenshot(path="kimi/test1_sogou_article_results.png")
            
            # Extract article information
            articles = await page.evaluate("""
                () => {
                    const items = document.querySelectorAll('.news-list li');
                    return Array.from(items).slice(0, 5).map(item => {
                        const titleEl = item.querySelector('h3 a');
                        const summaryEl = item.querySelector('.txt-info');
                        const accountEl = item.querySelector('.account');
                        const timeEl = item.querySelector('.s-p');
                        return {
                            title: titleEl?.textContent?.trim() || '',
                            href: titleEl?.getAttribute('href') || '',
                            summary: summaryEl?.textContent?.trim()?.substring(0, 100) || '',
                            account: accountEl?.textContent?.trim() || '',
                            time: timeEl?.textContent?.trim() || ''
                        };
                    });
                }
            """)
            
            results["sogou_search"]["articles_found"] = articles
            print(f"✓ Found {len(articles)} articles")
            for i, art in enumerate(articles[:3], 1):
                print(f"  {i}. {art.get('title', 'N/A')[:50]}...")
            
            # Check for anti-scraping measures
            page_content = await page.content()
            if "验证码" in page_content or "captcha" in page_content.lower():
                results["anti_scraping_measures"].append("Sogou: CAPTCHA detected")
                print("⚠ CAPTCHA/verification code detected")
            
            if "访问过于频繁" in page_content:
                results["anti_scraping_measures"].append("Sogou: Rate limiting detected")
                print("⚠ Rate limiting message detected")
            
            # Search for official accounts
            print(f"\n[Step 3] Searching for '{SEARCH_KEYWORD}' (official accounts)...")
            account_search_url = f"https://weixin.sogou.com/weixin?type=1&query={SEARCH_KEYWORD}"
            await page.goto(account_search_url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(3)
            
            await page.screenshot(path="kimi/test1_sogou_account_results.png")
            
            # Extract account information
            accounts = await page.evaluate("""
                () => {
                    const items = document.querySelectorAll('.account-box, .result');
                    return Array.from(items).slice(0, 5).map(item => {
                        const nameEl = item.querySelector('.account-name, h3');
                        const idEl = item.querySelector('.account-id, .info');
                        const descEl = item.querySelector('.account-desc');
                        return {
                            name: nameEl?.textContent?.trim() || '',
                            wechatId: idEl?.textContent?.trim() || '',
                            description: descEl?.textContent?.trim() || ''
                        };
                    });
                }
            """)
            
            results["sogou_search"]["accounts_found"] = accounts
            print(f"✓ Found {len(accounts)} official accounts")
            for i, acc in enumerate(accounts[:3], 1):
                print(f"  {i}. {acc.get('name', 'N/A')} ({acc.get('wechatId', 'N/A')})")
            
        except Exception as e:
            error_msg = str(e)
            print(f"✗ Error: {error_msg}")
            results["sogou_search"]["status"] = "error"
            results["sogou_search"]["errors"].append(error_msg)
        
        finally:
            await browser.close()

async def test_direct_wechat_access():
    """Test 2: Direct access to mp.weixin.qq.com articles"""
    print("\n" + "=" * 60)
    print("Test 2: Direct WeChat Article Access")
    print("=" * 60)
    
    # Sample WeChat article URLs to test (these are example formats)
    test_urls = [
        "https://mp.weixin.qq.com/s?biz=MzA5NjEyMDUyMA==",  # Generic format
        "https://mp.weixin.qq.com/s/xxxxx",  # Short format
    ]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # If we found articles from Sogou, try to visit one
        articles = results["sogou_search"].get("articles_found", [])
        
        if articles and articles[0].get("href"):
            article_url = articles[0]["href"]
            if article_url.startswith("/"):
                article_url = "https://weixin.sogou.com" + article_url
            
            print(f"\n[Step 1] Attempting to access article: {article_url[:60]}...")
            
            try:
                await page.goto(article_url, wait_until="networkidle", timeout=30000)
                await asyncio.sleep(3)
                
                await page.screenshot(path="kimi/test2_wechat_article.png")
                
                # Extract content if it's a WeChat article
                article_data = await page.evaluate("""
                    () => {
                        const isWeChat = window.location.href.includes('mp.weixin.qq.com');
                        return {
                            url: window.location.href,
                            isWeChat: isWeChat,
                            title: document.querySelector('#activity_name, .rich_media_title')?.textContent?.trim() 
                                   || document.title,
                            author: document.querySelector('#js_name, .profile_nickname')?.textContent?.trim(),
                            publishTime: document.querySelector('#publish_time')?.textContent?.trim(),
                            contentPreview: document.querySelector('#js_content, .rich_media_content')?.innerText?.substring(0, 500),
                            hasContent: !!document.querySelector('#js_content')
                        };
                    }
                """)
                
                results["direct_wechat_access"]["tested_articles"].append(article_data)
                
                if article_data.get("isWeChat"):
                    print(f"✓ Successfully navigated to WeChat article")
                    print(f"  Title: {article_data.get('title', 'N/A')[:60]}...")
                    print(f"  Author: {article_data.get('author', 'N/A')}")
                    print(f"  Has content: {article_data.get('hasContent')}")
                    results["direct_wechat_access"]["status"] = "accessible"
                else:
                    print(f"⚠ Redirected to: {article_data.get('url', 'unknown')}")
                    results["direct_wechat_access"]["status"] = "redirected"
                
                # Check for anti-scraping
                content = await page.content()
                if "请在微信客户端打开" in content:
                    results["anti_scraping_measures"].append("WeChat: Requires WeChat client")
                    print("⚠ Page requires WeChat client to view")
                
                if "访问频繁" in content or "verify" in content.lower():
                    results["anti_scraping_measures"].append("WeChat: Anti-bot verification")
                    print("⚠ Anti-bot verification detected")
                
            except Exception as e:
                error_msg = str(e)
                print(f"✗ Error accessing article: {error_msg}")
                results["direct_wechat_access"]["errors"].append(error_msg)
        else:
            print("⚠ No article URLs found from Sogou search to test")
            results["direct_wechat_access"]["status"] = "no_test_data"
        
        await browser.close()

async def test_wechat_mp_platform():
    """Test 3: WeChat MP Platform search"""
    print("\n" + "=" * 60)
    print("Test 3: WeChat MP Platform (mp.weixin.qq.com)")
    print("=" * 60)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            print("\n[Step 1] Accessing mp.weixin.qq.com...")
            await page.goto("https://mp.weixin.qq.com/", wait_until="networkidle", timeout=30000)
            await asyncio.sleep(2)
            
            await page.screenshot(path="kimi/test3_mp_platform.png")
            
            page_info = await page.evaluate("""
                () => ({
                    url: window.location.href,
                    title: document.title,
                    hasLogin: !!document.querySelector('input[type=password], .login'),
                    bodyText: document.body.innerText.substring(0, 500)
                })
            """)
            
            print(f"✓ Loaded: {page_info.get('title')}")
            print(f"  URL: {page_info.get('url')}")
            print(f"  Has login form: {page_info.get('hasLogin')}")
            
            # Check if there's a search functionality
            has_search = await page.evaluate("""
                () => !!document.querySelector('input[type=search], input[name=query], .search')
            """)
            
            if has_search:
                print("  Has search functionality: Yes")
            else:
                print("  Has search functionality: No (login required)")
                results["anti_scraping_measures"].append("MP Platform: Login required for search")
            
            results["mp_platform_test"] = {
                "accessible": True,
                "requires_login": page_info.get("hasLogin"),
                "has_search": has_search
            }
            
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            results["mp_platform_test"] = {
                "accessible": False,
                "error": str(e)
            }
        
        finally:
            await browser.close()

async def main():
    """Main test runner"""
    import datetime
    results["test_timestamp"] = datetime.datetime.now().isoformat()
    
    print("\n" + "=" * 60)
    print("WeChat Public Account Scraping Feasibility Test")
    print("Target: Shandong First Medical University (山东第一医科大学)")
    print("=" * 60)
    
    # Run all tests
    await test_sogou_wechat_search()
    await test_direct_wechat_access()
    await test_wechat_mp_platform()
    
    # Save results
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Results saved to: {OUTPUT_FILE}")
    
    # Print summary
    print("\n[Sogou WeChat Search]")
    print(f"  Status: {results['sogou_search']['status']}")
    print(f"  Accounts found: {len(results['sogou_search']['accounts_found'])}")
    print(f"  Articles found: {len(results['sogou_search']['articles_found'])}")
    
    print("\n[Direct WeChat Access]")
    print(f"  Status: {results['direct_wechat_access']['status']}")
    print(f"  Articles tested: {len(results['direct_wechat_access']['tested_articles'])}")
    
    print("\n[Anti-Scraping Measures Detected]")
    for measure in results["anti_scraping_measures"]:
        print(f"  - {measure}")
    if not results["anti_scraping_measures"]:
        print("  None detected")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
