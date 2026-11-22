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
    // global: all requests
    http_req_duration: ['p(95)<800'],
    http_req_failed: ['rate<0.01'],
  
    // per endpoint
    'http_req_duration{name:home}': ['p(95)<900'],
    'http_req_duration{name:quotes}': ['p(95)<900'],
  },  
};

export default function () {
  const home = http.get(`${BASE_URL}/`, { tags: {name: 'home'} });
  check(home, { 'home status is 200': (r) => r.status === 200 });
  const quotes = http.get(`${BASE_URL}/api/quotes`, { tags: {name: 'quotes'} });
  check(quotes, { 'quotes status is 200': (r) => r.status === 200 });
  sleep(1);
}