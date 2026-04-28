from playwright.sync_api import Page

class AccountPage:
    """
    个人账户页面类，封装了登录后的页面元素和操作。
    """
    def __init__(self, page: Page):
        self.page = page
        
        # 定义定位器 (Locators)
        # 登出链接
        self.logout_link = page.get_by_role("link", name=" Logout")

    def logout(self):
        """执行登出操作"""
        self.logout_link.click()
