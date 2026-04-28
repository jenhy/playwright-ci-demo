import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.baidu.com/")
    page.get_by_role("textbox", name="“特朗普承认自己吹牛了”").click()
    page.get_by_role("textbox", name="“特朗普承认自己吹牛了”").click()
    page.get_by_role("textbox", name="“特朗普承认自己吹牛了”").fill("测试")
    page.get_by_role("button", name="百度一下").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
