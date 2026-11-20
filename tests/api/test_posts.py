import pytest
from jsonschema import validate

from schemas import POST_SCHEMA

pytestmark = pytest.mark.api


def test_get_post_returns_valid_post(api, latency_budget):
    r = api.get_path("/posts/1")

    assert r.status_code == 200
    validate(instance=r.json(), schema=POST_SCHEMA)
    assert r.elapsed.total_seconds() < latency_budget, (
        f"took {r.elapsed.total_seconds():.2f}s, budget {latency_budget}s"
    )


def test_missing_post_returns_404(api):
    r = api.get_path("/posts/999999")
    assert r.status_code == 404


# TODO (you): write these yourself. They're the practice.
# - POST /posts creates a post: assert 201, echoed fields, schema
# - GET /posts?userId=1: every item belongs to user 1
# - parametrize the 404 test over several bad ids with @pytest.mark.parametrize
# - a test that GET /posts (100 items) stays under the latency budget
