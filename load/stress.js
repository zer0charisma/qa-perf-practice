// Stress test: ramps 10 -> 80 users to find where p95 breaks.
// Local app only:  python app/app.py, then  k6 run load/stress.js
import http from 'k6/http';
import { check, sleep } from 'k6';


const BASE_URL = __ENV.BASE_URL || 'http://localhost:5000';

export const options = {
  // Ramp up, hold, ramp down. Keep it small against a shared demo site.
  stages: [
    { duration: '30s', target: 10 },
    { duration: '30s', target: 20 },
    { duration: '30s', target: 40 },
    { duration: '30s', target: 80 },
    { duration: '10s', target: 0 },
  ],
  // Thresholds are the point: if they fail, k6 exits non-zero and CI goes red.
  thresholds: {
    // global: all requests
    http_req_duration: ['p(95)<800'],
    http_req_failed: ['rate<0.01'],
  
    // per endpoint: same 500ms promise for both. The question is which
    // endpoint breaks it first, and at how many users.
    'http_req_duration{name:fast}': ['p(95)<500'],
    'http_req_duration{name:slow}': ['p(95)<500'],

  },  
};

export default function () {
  const fast = http.get(`${BASE_URL}/fast`, { tags: {name: 'fast'} });
  check(fast, { 'fast status is 200': (r) => r.status === 200 });
  const slow = http.get(`${BASE_URL}/slow`, { tags: {name: 'slow'} });
  check(slow, { 'slow status is 200': (r) => r.status === 200 });
  sleep(1);
}
