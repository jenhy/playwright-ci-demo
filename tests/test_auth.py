import re
import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.account_page import AccountPage

def test_user_authentication(page: Page):
    """
    用户身份验证测试：登录并登出。
    
    此测试使用页面对象模型 (POM) 来分离页面元素和测试逻辑。
    """
    # 加载 .env 文件中的环境变量
    load_dotenv()
    
    # 1. 初始化 Page Object
    login_page = LoginPage(page)
    account_page = AccountPage(page)

    # 2. 访问首页
    login_page.navigate()

    # 3. 点击 My Account 菜单进入登录/注册入口
    login_page.click_my_account()

    # 4. 执行登录操作
    # 从环境变量中安全获取邮箱和密码
    email = os.getenv("email")
    password = os.getenv("passwd")
    
    if not email or not password:
        pytest.fail("请确保 .env 文件中配置了 email 和 passwd")
        
    login_page.login(email, password)

    # 5. 断言：验证是否成功进入账户页面 (Web-First 断言)
    # 检查 URL 是否包含 account 关键字，或者登出按钮是否可见
    expect(page).to_have_url(re.compile(r".*route=account/account"))
    expect(account_page.logout_link).to_be_visible()

    # 6. 执行登出操作
    account_page.logout()

    # 7. 断言：验证登出后是否跳转回成功页面或显示登录入口
    expect(page).to_have_url(re.compile(r".*route=account/logout"))
