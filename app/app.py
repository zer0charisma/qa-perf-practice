"""Tiny local app for Project 4: find and fix a bottleneck.

Run:  python app/app.py   (serves on http://localhost:5000)
Then: k6 run -e BASE_URL=http://localhost:5000 load/smoke.js

/fast is fine. /slow has a deliberate performance bug. Load test it, watch
p95 latency, find the cause, fix it, re-run, and record before/after numbers.
"""
import time

from flask import Flask, jsonify

app = Flask(__name__)

PRODUCTS = [{"id": i, "name": f"item-{i}"} for i in range(2000)]


def lookup_product(product_id):
    # Simulates a slow per-item lookup (think: one DB query per row).
    time.sleep(0.0005)
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    return None


@app.route("/")
def index():
    return jsonify(status="ok")


@app.route("/fast")
def fast():
    return jsonify(count=len(PRODUCTS))


@app.route("/slow")
def slow():
    # TODO (you): this is the bottleneck. Why is it slow, and how would you fix it?
    ids = range(0, 2000, 10)
    items = [lookup_product(i) for i in ids]
    return jsonify(count=len(items))


if __name__ == "__main__":
    app.run(port=5000)
