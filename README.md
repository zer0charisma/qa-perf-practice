# qa-perf-practice

Practice repo for API, browser-performance and load testing, wired into CI.

| Area | Tool | Where | Runs in CI |
|---|---|---|---|
| API functional + latency | pytest, requests, jsonschema | `tests/api/` | every push |
| Browser performance budgets | Playwright (Python) | `tests/browser/` | every push |
| Load test with pass/fail thresholds | k6 | `load/` | manual (`workflow_dispatch`) |
| Bottleneck hunt | Flask app + k6 | `app/` | local |

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
brew install k6
```

## Run

```bash
pytest -m api                 # API tests
pytest -m browser -s          # page-load budgets (-s prints the timings)
k6 run load/smoke.js          # load test against QuickPizza

python app/app.py             # in one terminal
k6 run -e BASE_URL=http://localhost:5000 load/smoke.js   # in another
```

## Design choices
- **Budgets and thresholds fail the build.** Performance is a gate, not a report.
- **Config in one place.** Base URLs and budgets come from env vars with defaults.
- **Schemas separate from tests.** Tests stay short and schemas are reusable.
- **Load tests run manually in CI.** Shared demo sites shouldn't take load on every push.

## Results log
Record baselines and before/after numbers here as you go.

| Date | Test | p95 / timing | Notes |
|---|---|---|---|
| 2026-11-22 | smoke.js (QuickPizza, 5 VUs) | home 115ms, quotes 121ms | 0% errors. Thresholds set to 350ms (~3x baseline) |
| 2026-11-22 | stress.js (local, 10→80 VUs), baseline | /fast 2.2ms, /slow 150ms | No break at 80 VUs. /slow is per-request cost, not capacity |
| 2026-11-22 | stress.js (local, 10→320 VUs), baseline | /fast 2.1ms, /slow 147ms | No breaking point up to 320 VUs on local hardware |
| 2026-11-22 | stress.js (local, 10→80 VUs), fix 1: dict lookup | /fast 1.8ms, /slow 132ms | −12%. Removed the list scan; 200 round trips were still the main cost |
| 2026-11-22 | stress.js (local, 10→80 VUs), fix 2: batched lookup | /fast 3.3ms, /slow 3.7ms | −98% vs baseline (~40x). One lookup instead of 200 (N+1 fix). Output unchanged (count 200), 0% errors |

