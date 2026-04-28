from playwright.sync_api import Page

class LoginPage:
    """
    登录页面类，封装了登录页面的所有元素定位器和相关业务操作。
    """
    def __init__(self, page: Page):
        self.page = page
        
        # 定义定位器 (Locators)
        # 首页或全局的 "My account" 按钮
        self.my_account_menu = page.get_by_role("button", name=" My account")
        # 邮箱输入框
        self.email_input = page.get_by_role("textbox", name="E-Mail Address")
        # 密码输入框
        self.password_input = page.get_by_role("textbox", name="Password")
        # 登录按钮
        self.login_button = page.get_by_role("button", name="Login")

    def navigate(self):
        """跳转到首页"""
        self.page.goto("https://ecommerce-playground.lambdatest.io/")

    def click_my_account(self):
        """点击顶部菜单的 My Account"""
        self.my_account_menu.click()

    def login(self, email, password):
        """
        封装登录业务逻辑
        1. 输入邮箱
        2. 输入密码
        3. 点击登录
        """
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()
