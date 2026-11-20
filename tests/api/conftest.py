import os

import pytest
import requests

# Public practice API: no key needed, safe to hit with functional tests.
# (Not for load testing: use load/ against QuickPizza or the local app.)
DEFAULT_API_BASE = "https://jsonplaceholder.typicode.com"

# Response-time budget in seconds. Kept in one place so it's easy to tune.
LATENCY_BUDGET_S = float(os.getenv("LATENCY_BUDGET_S", "1.0"))


@pytest.fixture(scope="session")
def api_base_url():
    return os.getenv("API_BASE_URL", DEFAULT_API_BASE)


@pytest.fixture(scope="session")
def api(api_base_url):
    """A shared session: reuses connections, one place to add headers/auth."""
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})

    def get(path, **kwargs):
        return session.get(f"{api_base_url}{path}", timeout=10, **kwargs)

    def post(path, **kwargs):
        return session.post(f"{api_base_url}{path}", timeout=10, **kwargs)

    session.get_path = get
    session.post_path = post
    yield session
    session.close()


@pytest.fixture
def latency_budget():
    return LATENCY_BUDGET_S
