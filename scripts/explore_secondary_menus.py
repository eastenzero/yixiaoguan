"""
Explore secondary menus and sub-sites of sdfmu.edu.cn
Generate report for KB expansion task.
"""
import asyncio
from playwright.async_api import async_playwright
import json

# Storage for findings
findings = {
    "main_nav": {},
    "sub_sites": [],
    "footer_links": [],
    "quick_links": [],
    "new_discoveries": []
}

async def explore_main_site():
    """Explore main website navigation"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        
        print("=" * 60)
        print("Exploring https://www.sdfmu.edu.cn/")
        print("=" * 60)
        
        try:
            await page.goto("https://www.sdfmu.edu.cn/", timeout=30000)
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(2)  # Wait for JS to load
            
            # Take screenshot for reference
            await page.screenshot(path="kimi/report-8-main-page.png")
            print("Screenshot saved: report-8-main-page.png")
            
            # Extract all links and structure
            page_info = await page.evaluate("""
                () => {
                    const result = {
                        title: document.title,
                        url: window.location.href,
                        menuStructure: {},
                        allLinks: [],
                        footerLinks: [],
                        quickLinks: [],
                        subdomains: new Set()
                    };
                    
                    // Find main navigation - try multiple patterns
                    const menuPatterns = [
                        { container: '.mainnav', items: '.mainnav > ul > li' },
                        { container: '.nav-collapse', items: '.nav-collapse li' },
                        { container: '#menu', items: '#menu > li' },
                        { container: '.navbar', items: '.navbar li' },
                        { container: 'nav', items: 'nav li' }
                    ];
                    
                    let foundMenu = null;
                    for (const pattern of menuPatterns) {
                        const container = document.querySelector(pattern.container);
                        if (container) {
                            const items = container.querySelectorAll(pattern.items);
                            if (items.length >= 5) {
                                foundMenu = { container, items };
                                break;
                            }
                        }
                    }
                    
                    // If still not found, look for any UL with many LI items
                    if (!foundMenu) {
                        const allUls = document.querySelectorAll('ul');
                        for (const ul of allUls) {
                            const directLis = ul.querySelectorAll(':scope > li');
                            if (directLis.length >= 5 && directLis.length <= 20) {
                                // Check if it contains navigation-like links
                                const hasNavLinks = Array.from(directLis).some(li => {
                                    const a = li.querySelector('a');
                                    return a && a.textContent.trim().length < 20;
                                });
                                if (hasNavLinks) {
                                    foundMenu = { container: ul, items: directLis };
                                    break;
                                }
                            }
                        }
                    }
                    
                    if (foundMenu) {
                        foundMenu.items.forEach((item, idx) => {
                            const mainLink = item.querySelector(':scope > a') || item.querySelector('a');
                            if (!mainLink) return;
                            
                            const mainText = mainLink.textContent?.trim() || `Item-${idx}`;
                            const subItems = [];
                            
                            // Find submenu (could be nested UL or dropdown)
                            const subUl = item.querySelector('ul, .dropdown-menu, .sub-menu, .dropdown');
                            if (subUl) {
                                const subLinks = subUl.querySelectorAll('a');
                                subLinks.forEach(sub => {
                                    const text = sub.textContent?.trim() || '';
                                    const href = sub.href || '';
                                    if (text) {
                                        subItems.push({ text, href });
                                    }
                                });
                            }
                            
                            result.menuStructure[mainText] = {
                                href: mainLink.href || '',
                                subItems: subItems
                            };
                        });
                    }
                    
                    // Get all links for subdomain analysis
                    const allLinks = document.querySelectorAll('a[href]');
                    allLinks.forEach(a => {
                        const href = a.href;
                        const text = a.textContent?.trim() || '';
                        if (href) {
                            result.allLinks.push({ text: text.slice(0, 50), href });
                            // Extract subdomains
                            try {
                                const url = new URL(href);
                                if (url.hostname.includes('sdfmu.edu.cn')) {
                                    result.subdomains.add(url.hostname);
                                }
                            } catch(e) {}
                        }
                    });
                    
                    // Footer links
                    const footer = document.querySelector('footer, .footer, #footer, .foot');
                    if (footer) {
                        footer.querySelectorAll('a').forEach(a => {
                            result.footerLinks.push({
                                text: a.textContent?.trim()?.slice(0, 50) || '',
                                href: a.href || ''
                            });
                        });
                    }
                    
                    // Quick links section
                    const quickLinkSections = document.querySelectorAll('.quick-links, .link-box, .fastlink, .quick-menu');
                    quickLinkSections.forEach(section => {
                        section.querySelectorAll('a').forEach(a => {
                            result.quickLinks.push({
                                text: a.textContent?.trim()?.slice(0, 50) || '',
                                href: a.href || ''
                            });
                        });
                    });
                    
                    result.subdomains = Array.from(result.subdomains);
                    return result;
                }
            """)
            
            findings["page_info"] = page_info
            
            print(f"\nPage title: {page_info.get('title', 'N/A')}")
            print(f"\nMenu structure found: {len(page_info.get('menuStructure', {}))} main items")
            
            # Print menu structure
            for menu, data in page_info.get('menuStructure', {}).items():
                print(f"\n📁 {menu}")
                if data.get('subItems'):
                    for sub in data['subItems']:
                        print(f"   └─ {sub['text'][:35]}: {sub['href'][:50]}")
                else:
                    print(f"   └─ (no submenu or link only)")
            
            print(f"\nSubdomains found: {len(page_info.get('subdomains', []))}")
            for sd in sorted(page_info.get('subdomains', [])):
                print(f"  - {sd}")
                
        except Exception as e:
            print(f"Error exploring main site: {e}")
            import traceback
            traceback.print_exc()
        
        await browser.close()

async def check_sub_sites():
    """Check known sub-sites with HTTPS"""
    sub_sites = [
        ("学生工作处", "https://xsc.sdfmu.edu.cn"),
        ("后勤管理处", "https://hqglc.sdfmu.edu.cn"),
        ("保卫处", "https://bwc.sdfmu.edu.cn"),
        ("团委", "https://tw.sdfmu.edu.cn"),
        ("研究生院", "https://yjsc.sdfmu.edu.cn"),
        ("国际交流处", "https://gjjlc.sdfmu.edu.cn"),
        ("财务处", "https://cwc.sdfmu.edu.cn"),
        ("人事处", "https://rsc.sdfmu.edu.cn"),
        ("科研处", "https://kyc.sdfmu.edu.cn"),
        ("实验管理中心", "https://syzx.sdfmu.edu.cn"),
        ("教师发展中心", "https://jsfzzx.sdfmu.edu.cn"),
        ("资产管理处", "https://zcglc.sdfmu.edu.cn"),
        ("审计处", "https://sjc.sdfmu.edu.cn"),
        ("离退休工作处", "https://ltgzc.sdfmu.edu.cn"),
        ("医院管理处", "https://yglc.sdfmu.edu.cn"),
        ("继续教育学院", "https://jxjy.sdfmu.edu.cn"),
        ("图书馆", "https://lib.sdfmu.edu.cn"),
    ]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        results = []
        for name, url in sub_sites:
            try:
                page = await browser.new_page()
                print(f"\nChecking {name}: {url}")
                response = await page.goto(url, timeout=15000, wait_until="domcontentloaded")
                await asyncio.sleep(1)
                
                if response:
                    status = response.status
                    title = await page.title()
                    final_url = page.url
                    print(f"  Status: {status}, Title: {title[:40] if title else 'N/A'}")
                    
                    # Get a brief content summary
                    content_preview = await page.evaluate("""
                        () => {
                            const main = document.querySelector('main, .main, #main, .content, #content');
                            const body = main || document.body;
                            return body.textContent?.slice(0, 200)?.replace(/\\s+/g, ' ') || '';
                        }
                    """)
                    
                    results.append({
                        "name": name,
                        "url": url,
                        "status": status,
                        "title": title,
                        "final_url": final_url,
                        "accessible": status == 200,
                        "content_preview": content_preview[:150]
                    })
                else:
                    results.append({
                        "name": name,
                        "url": url,
                        "status": 0,
                        "title": "",
                        "accessible": False
                    })
                
                await page.close()
            except Exception as e:
                error_msg = str(e)
                print(f"  Error: {error_msg[:80]}")
                results.append({
                    "name": name,
                    "url": url,
                    "status": 0,
                    "title": "",
                    "accessible": False,
                    "error": error_msg[:100]
                })
        
        findings["sub_sites"] = results
        await browser.close()

async def explore_discovered_subsites():
    """Explore newly discovered subdomains"""
    subs_to_check = [
        ("英文版", "https://english.sdfmu.edu.cn"),
        ("信息公开", "https://information.sdfmu.edu.cn"),
        ("人才招聘", "https://personnel.sdfmu.edu.cn"),
        ("医学教育研究中心", "https://sr.sdfmu.edu.cn"),
        ("校友会", "https://alumi.sdfmu.edu.cn"),
        ("党代会", "https://ddhzt.sdfmu.edu.cn"),
        ("党史学习教育", "https://dsxxjy.sdfmu.edu.cn"),
        ("大学文化", "https://dxwh.sdfmu.edu.cn"),
        ("综合立体督查", "https://discipline.sdfmu.edu.cn"),
        ("教学工作网", "https://metc.sdfmu.edu.cn"),
        ("科教融合", "https://wsdx.sdfmu.edu.cn"),
        ("毕业季专题", "https://byj.sdfmu.edu.cn"),
    ]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        results = []
        for name, url in subs_to_check:
            try:
                page = await browser.new_page()
                print(f"\nExploring {name}: {url}")
                response = await page.goto(url, timeout=15000)
                
                if response and response.status == 200:
                    title = await page.title()
                    print(f"  ✓ Accessible: {title[:40] if title else 'N/A'}")
                    
                    # Extract main navigation if any
                    nav_items = await page.evaluate("""
                        () => {
                            const nav = document.querySelector('nav, .nav, .menu');
                            if (!nav) return [];
                            return Array.from(nav.querySelectorAll('a')).slice(0, 10).map(a => ({
                                text: a.textContent?.trim()?.slice(0, 30) || '',
                                href: a.href || ''
                            }));
                        }
                    """)
                    
                    results.append({
                        "name": name,
                        "url": url,
                        "accessible": True,
                        "title": title,
                        "nav_items": nav_items
                    })
                else:
                    status = response.status if response else 0
                    print(f"  ✗ Not accessible (status: {status})")
                    results.append({
                        "name": name,
                        "url": url,
                        "accessible": False,
                        "status": status
                    })
                
                await page.close()
            except Exception as e:
                print(f"  ✗ Error: {str(e)[:60]}")
                results.append({
                    "name": name,
                    "url": url,
                    "accessible": False,
                    "error": str(e)[:80]
                })
        
        findings["additional_subsites"] = results
        await browser.close()

async def main():
    print("Starting exploration of sdfmu.edu.cn secondary menus...")
    
    await explore_main_site()
    await check_sub_sites()
    await explore_discovered_subsites()
    
    # Save findings to JSON for reference
    with open("kimi/report-8-findings.json", "w", encoding="utf-8") as f:
        json.dump(findings, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print("Exploration complete!")
    print("Findings saved to: kimi/report-8-findings.json")
    print("=" * 60)
    
    return findings

if __name__ == "__main__":
    result = asyncio.run(main())
