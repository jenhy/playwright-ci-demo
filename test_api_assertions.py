import pytest
from typing import Generator
from playwright.sync_api import Playwright, APIRequestContext, expect

# --- 定义 Fixture ---
@pytest.fixture(scope="session")
def api_context(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    # 创建 API 请求上下文，并配置基础 URL
    context = playwright.request.new_context(base_url="https://jsonplaceholder.typicode.com")
    yield context
    context.dispose()

# --- 测试用例 ---

def test_get_post_with_assertions(api_context: APIRequestContext):
    """使用 expect 断言 API 响应"""
    response = api_context.get("/posts/1")
    
    # 1. 核心 API 断言：验证响应是否成功 (状态码 200-299)
    # 如果失败，它会打印出具体的状态码和返回内容
    expect(response).to_be_ok()
    
    # 2. 验证特定的状态码
    assert response.status == 200
    
    # 3. 验证 JSON 内容（结合原生断言）
    result = response.json()
    # print(f"result:{result}")
    assert result["id"] == 1
    assert len(result["title"]) > 0

def test_create_post_and_validate(api_context: APIRequestContext):
    """创建资源并使用断言"""
    payload = {
        "title": "Asserting with Playwright",
        "body": "Better error messages",
        "userId": 1
    }
    response = api_context.post("/posts", data=payload)
    
    # 断言请求成功
    expect(response).to_be_ok()
    
    # 断言创建成功的状态码是 201
    assert response.status == 201
    
    # 验证返回的数据包含我们发送的内容
    # print(f"payload:{payload['title']}")
    # print(f"response:{response.json()['title']}")
    assert response.json()["title"] == payload["title"]

def test_negative_cases(api_context: APIRequestContext):
    """测试负面场景：资源不存在"""
    # 访问一个不存在的 ID
    response = api_context.get("/posts/9999")
    
    # 断言响应不成功 (Not OK)
    expect(response).not_to_be_ok()
    
    # 验证状态码为 404
    assert response.status == 404