#!/usr/bin/env python3
"""
Measure the cost of one /submit: seconds of compute on this machine.

One warm-up request (loads the model, not counted), then 10 timed runs on the
same fixed text. Each run uses its own creator_id so the rate limiter never
trips. Reports both the server's own duration_ms (read back from the audit
log) and the client-side round trip.
"""

import json
import statistics
import time
import urllib.request

URL = "http://127.0.0.1:5000"
RUNS = 10
TEXT = (
    "The library on our street closes at six, which never seemed early until "
    "I started working late. Most evenings I get there with ten minutes to "
    "spare, grab whatever is on the returns cart, and read it on the bus home. "
    "Last month that meant a book about bridge engineering, a cookbook from "
    "the seventies, and a novel I abandoned halfway through because the "
    "narrator kept apologising to the reader. I liked the bridges best. There "
    "is something calming about people who worry carefully about weight and "
    "wind so that everyone else can stop thinking about it."
)


def post(path, body):
    req = urllib.request.Request(
        URL + path,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def get_log():
    with urllib.request.urlopen(URL + "/log") as r:
        return json.load(r)["entries"]


def main():
    stamp = int(time.time())

    t = time.perf_counter()
    post("/submit", {"text": TEXT, "creator_id": f"cost_warmup_{stamp}"})
    print(f"warm-up (cold start, not counted): {time.perf_counter() - t:.2f}s")

    ids, client_ms = [], []
    for i in range(RUNS):
        t = time.perf_counter()
        resp = post("/submit", {"text": TEXT, "creator_id": f"cost_{stamp}_{i}"})
        client_ms.append((time.perf_counter() - t) * 1000)
        ids.append(resp["content_id"])

    by_id = {e.get("content_id"): e for e in get_log()}
    server_ms = [by_id[c]["duration_ms"] for c in ids]

    print(f"\n{'run':>3}  {'server_ms':>10}  {'client_ms':>10}")
    for i, (s, c) in enumerate(zip(server_ms, client_ms), 1):
        print(f"{i:>3}  {s:>10.1f}  {c:>10.1f}")

    print(f"\ntext: {len(TEXT)} chars, {len(TEXT.split())} words, {RUNS} runs")
    print(f"server duration_ms  mean {statistics.mean(server_ms):.1f}  "
          f"median {statistics.median(server_ms):.1f}  "
          f"min {min(server_ms):.1f}  max {max(server_ms):.1f}")
    print(f"client round trip   mean {statistics.mean(client_ms):.1f} ms")


if __name__ == "__main__":
    main()