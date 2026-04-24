from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # 1. 启动时尝试隐藏自动化特征
        browser = p.chromium.launch(
            headless=False, 
            slow_mo=500,
            args=["--disable-blink-features=AutomationControlled"] # 尝试规避指纹检测
        )
        
        # 2. 设置一个大尺寸的视口
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        print("正在打开百度...")
        page.goto("https://www.baidu.com")
        
        # 3. 定位器
        search_input = page.locator("#kw")
        search_button = page.locator("#su")

        print("正在尝试输入搜索词（暴力模式）...")
        try:
            # 方案 A: 强制填充 (force=True)
            search_input.fill("Playwright", force=True)
        except:
            # 方案 B: 如果 A 失败，直接用 JS 操作 DOM（绝对会成功，除非 ID 变了）
            print("标准填充失败，执行 JS 注入...")
            search_input.evaluate('(el) => el.value = "Playwright"')

        print("正在尝试点击搜索（暴力模式）...")
        try:
            # 方案 A: 强制点击
            search_button.click(force=True)
        except:
            # 方案 B: 触发底层点击事件（绕开所有视觉遮挡检查）
            print("标准点击失败，触发底层事件...")
            search_button.dispatch_event("click")

        # 4. 验证结果
        print("等待结果渲染...")
        # 等待结果容器出现，不再等它“可见”，只要它“存在”就行
        page.wait_for_selector("#content_left", state="attached", timeout=10000)
        
        print(f"操作完成！当前页面标题: {page.title()}")
        
        # 截图留存看看到底搜出来没
        page.screenshot(path="baidu_result.png")
        print("已截图：baidu_result.png")
        
        browser.close()

if __name__ == "__main__":
    run()