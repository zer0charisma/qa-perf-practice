import pytest
from jsonschema import validate

from schemas import POST_SCHEMA
from conftest import assert_within_budget

pytestmark = pytest.mark.api


def test_create_post(api, latency_budget):
    r = api.post_path("/posts", json={"title": "test", "body": "This is a test post", "userId": 1})
    assert r.status_code == 201, f"Expected status code 201, got {r.status_code}"
    body = r.json()
    assert body["title"] == "test", f"Expected title 'test', got {body['title']}"
    assert body["userId"] == 1
    assert isinstance(body["userId"], int), f"Expected user id to be an int, got {type(body['userId'])}"
    validate(instance=body, schema=POST_SCHEMA)
    assert_within_budget(r, latency_budget)

def test_get_post_returns_valid_post(api, latency_budget):
    r = api.get_path("/posts/1")
    assert r.status_code == 200, f"Expected status code 200, got {r.status_code}"
    post = r.json()
    assert post["userId"] == 1, f"Expected user id 1, got {post['userId']}"
    validate(instance=post, schema=POST_SCHEMA)
    assert_within_budget(r, latency_budget)


def test_get_post_by_one_user(api, latency_budget):
    r = api.get_path("/posts?userId=1")
    assert r.status_code == 200, f"Expected status code 200, got {r.status_code}"
    posts = r.json()
    assert posts, "Expected posts for user 1, got none"
    for post in posts:
        assert post["userId"] == 1, f"Post {post['id']} has userId {post['userId']}"
        validate(instance=post, schema=POST_SCHEMA)
    assert_within_budget(r, latency_budget)


@pytest.mark.parametrize ("bad_id", ["-1", "0", "1234567890"])
def test_missing_post_returns_404(api, bad_id, latency_budget):
    r = api.get_path(f"/posts/{bad_id}")
    assert r.status_code == 404, f"Expected status code 404, got {r.status_code}"
    assert_within_budget(r, latency_budget)


@pytest.mark.xfail(reason="API has no post limit yet (see ticket ABC-123)")
def test_cannot_exceed_post_limit(api):
    r = api.post_path("/posts", json={"title": "x", "body": "x", "userId": 1})
    assert r.status_code == 403, f"Expected status code 403, got {r.status_code}"
    assert_within_budget(r, latency_budget)
