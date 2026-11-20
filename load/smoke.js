// k6 load test. Run:  k6 run load/smoke.js
// Target QuickPizza (Grafana's demo app built for load testing) or the local
// app in app/.  Never load test a site you don't own or that hasn't invited it.
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'https://quickpizza.grafana.com';

export const options = {
  // Ramp up, hold, ramp down. Keep it small against a shared demo site.
  stages: [
    { duration: '15s', target: 5 },
    { duration: '30s', target: 5 },
    { duration: '10s', target: 0 },
  ],
  // Thresholds are the point: if they fail, k6 exits non-zero and CI goes red.
  thresholds: {
    http_req_duration: ['p(95)<800'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get(`${BASE_URL}/`);
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);
}

// TODO (you):
// - add a second request to an API endpoint and tag it so you get per-endpoint stats
// - make a stress.js that keeps ramping until p95 breaks; note where it breaks
