import pytest
from typing import Generator
from playwright.sync_api import Playwright, APIRequestContext

# --- 第一部分：定义 Fixture ---

@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    """
    创建一个全局的 API 请求上下文。
    设置 base_url 后，后续请求只需要写路径（如 /posts）。
    """
    # 可以在这里设置通用的 Header，比如 Authorization
    headers = {
        "Content-type": "application/json; charset=UTF-8",
    }
    
    # 创建请求上下文
    request_context = playwright.request.new_context(
        base_url="https://jsonplaceholder.typicode.com",
        extra_http_headers=headers
    )
    
    yield request_context
    
    # 测试结束后销毁上下文
    request_context.dispose()


# --- 第二部分：编写测试用例 ---

def test_get_user_and_validate(api_request_context: APIRequestContext):
    """测试 GET 请求：获取 ID 为 1 的帖子"""
    response = api_request_context.get("/posts/1")
    
    # 验证状态码
    assert response.ok  # 状态码在 200-299 之间
    assert response.status == 200
    
    # 验证返回的内容
    body = response.json()
    assert body["id"] == 1
    assert "userId" in body
    print(f"\nGET 返回结果: {body['title']}")


def test_create_post(api_request_context: APIRequestContext):
    """测试 POST 请求：创建一个新帖子"""
    new_post_data = {
        "title": "Playwright API 测试",
        "body": "这是使用 Playwright 发送的内容",
        "userId": 1
    }
    
    response = api_request_context.post("/posts", data=new_post_data)
    
    # 验证创建成功（201 Created）
    assert response.status == 201
    
    body = response.json()
    assert body["title"] == new_post_data["title"]
    assert body["id"] is not None  # 确保返回了新生成的 ID
    print(f"\nPOST 成功，生成 ID: {body['id']}")


def test_update_post(api_request_context: APIRequestContext):
    """测试 PUT 请求：修改已有的帖子"""
    updated_data = {
        "id": 1,
        "title": "修改后的标题",
        "body": "修改后的内容",
        "userId": 1
    }
    
    response = api_request_context.put("/posts/1", data=updated_data)
    
    assert response.status == 200
    assert response.json()["title"] == "修改后的标题"


def test_delete_post(api_request_context: APIRequestContext):
    """测试 DELETE 请求：删除帖子"""
    response = api_request_context.delete("/posts/1")
    
    # 验证删除成功（200 或 204）
    assert response.status == 200
    print("\nDELETE 成功")