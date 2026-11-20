import os

import pytest

pytestmark = pytest.mark.browser

PAGE_URL = os.getenv("PAGE_URL", "https://quickpizza.grafana.com/")

# Budgets in milliseconds. Tune after you've measured a baseline.
DOM_CONTENT_LOADED_BUDGET_MS = 3000
LOAD_EVENT_BUDGET_MS = 5000


def navigation_timing(page):
    """Read the browser's own Navigation Timing entry (same data as DevTools)."""
    return page.evaluate(
        "() => JSON.parse(JSON.stringify(performance.getEntriesByType('navigation')[0]))"
    )


def test_page_load_within_budget(page):
    page.goto(PAGE_URL, wait_until="load")
    nav = navigation_timing(page)

    print(
        f"\nTTFB={nav['responseStart']:.0f}ms "
        f"DCL={nav['domContentLoadedEventEnd']:.0f}ms "
        f"load={nav['loadEventEnd']:.0f}ms"
    )
    assert nav["domContentLoadedEventEnd"] < DOM_CONTENT_LOADED_BUDGET_MS
    assert nav["loadEventEnd"] < LOAD_EVENT_BUDGET_MS


# TODO (you):
# - run the same test on a throttled network (CDP session:
#   page.context.new_cdp_session(page) -> "Network.emulateNetworkConditions")
#   and compare the numbers
# - count requests and total bytes with page.on("response", ...) and set a budget
