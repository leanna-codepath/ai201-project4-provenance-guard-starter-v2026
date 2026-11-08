#!/usr/bin/env python3
"""
Unit 9: test the five criteria in criteria.md, three trials each.

    python app.py                                    # terminal 1 (restart it first, see below)
    python run_eval_unit9.py --label after           # terminal 2: criteria 1-4

Criterion 5 needs the model to fail, so you set that up by hand:

    1. Stop app.py.
    2. Point the detector at a model that doesn't exist. Either edit config.py:
           DETECTOR_MODEL = os.getenv("AI201_DETECTOR_MODEL", "not-a-real-model")
       or leave config.py alone and set the env var (PowerShell):
           $env:AI201_DETECTOR_MODEL = "not-a-real-model"
    3. Start app.py again.
    4. python run_eval_unit9.py --criteria 5 --label model_down
    5. Put DETECTOR_MODEL back (or `Remove-Item Env:AI201_DETECTOR_MODEL`)
       and restart app.py.

Unlike run_eval.py, this script decides pass/fail itself, because each Unit 9
criterion can be checked in code. A criterion passes only if all three trials
pass.

Restart app.py before running. Rate limits are kept in memory. Requests
without a usable creator_id (malformed JSON, a bad creator_id) all count
against your IP: 5 a minute, 50 a day. When one gets a 429, this script waits
61 seconds and retries. That makes a run take a few minutes, but the limiter
stays on, so you're testing the real system. The 429s are recorded too, and
criterion 1 checks that they were logged.
"""

import argparse
import datetime as dt
import json
import sys
import time

import config

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass

try:
    import requests
except ImportError:
    print("The `requests` package isn't installed.\nRun: pip install -r requirements.txt",
          file=sys.stderr)
    sys.exit(1)


DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"
RATE_LIMIT_WAIT_S = 61
MAX_429_RETRIES = 2

TARGETS = {
    1: "Every /submit and /appeal call is logged (100%)",
    2: "Too-short and too-long text rejected (100%)",
    3: "Every submission has a valid creator_id or an error (100%)",
    4: "Non-prose text rejected in at least 4 of 5 cases (>= 80%)",
    5: "Model failure: 5xx JSON error, error logged, /health then 200",
}

NAMES = {
    1: "every call is logged",
    2: "length limits",
    3: "creator_id",
    4: "non-prose rejected",
    5: "model failure",
}

# Ordinary prose that should pass validation and reach the model.
PROSE = ("I spent most of Saturday repotting the plants on my balcony, and somehow "
         "ended up with more soil on me than in any of the pots.")


def make_prose(n_chars: int) -> str:
    """English prose exactly n_chars long, with no whitespace at either end."""
    sentence = ("The quick brown fox jumps over the lazy dog while the farmer "
                "watches quietly from the porch. ")
    text = (sentence * (n_chars // len(sentence) + 1))[:n_chars]
    if text[-1].isspace():
        text = text[:-1] + "."
    return text


# ── Talking to the service ────────────────────────────────────────────────────

class Client:
    """
    Sends requests and records every /submit and /appeal call in a ledger.

    Each call is wrapped in a before/after count of the audit log (taken from
    /health, which isn't logged itself). Criterion 1 is then a check that
    every row in the ledger produced exactly one matching log entry. That
    covers the calls made for every criterion, not only criterion 1's own.
    """

    def __init__(self, url: str, timeout: float):
        self.url = url
        self.timeout = timeout
        self.ledger: list[dict] = []
        self.trial = 0
        self._tag = dt.datetime.now().strftime("%H%M%S")
        self._n = 0

    def creator(self) -> str:
        """A fresh creator_id, so each valid request gets its own rate-limit bucket."""
        self._n += 1
        return f"u9_{self._tag}_{self._n}"

    def log_count(self) -> int:
        return requests.get(f"{self.url}/health", timeout=30).json()["log_entries"]

    def last_entries(self, n: int) -> list[dict]:
        if n <= 0:
            return []
        r = requests.get(f"{self.url}/log", params={"limit": n}, timeout=30)
        return r.json()["entries"]

    def call(self, path: str, body=None, *, raw: bytes | None = None,
             content_type: str = "application/json", method: str = "POST",
             note: str = "") -> dict:
        """One logical request. Retries after a 429, and every attempt goes in the ledger."""
        for attempt in range(MAX_429_RETRIES + 1):
            record = self._send_once(path, body, raw, content_type, method, note)
            if record["status"] != 429 or attempt == MAX_429_RETRIES:
                return record
            print(f"      rate limited ({note}); waiting {RATE_LIMIT_WAIT_S}s and retrying")
            time.sleep(RATE_LIMIT_WAIT_S)
        return record

    def _send_once(self, path, body, raw, content_type, method, note) -> dict:
        if raw is not None:
            data = raw
        elif method == "POST":
            # Serialize by hand so that a body of JSON `null` is really sent.
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        else:
            data = None
        headers = {"Content-Type": content_type} if data is not None else {}

        before = self.log_count()
        try:
            r = requests.request(method, self.url + path, data=data, headers=headers,
                                 timeout=self.timeout)
            status = r.status_code
            try:
                payload = r.json()
            except ValueError:
                payload = None
        except requests.RequestException as exc:
            status, payload = None, {"client_error": f"{type(exc).__name__}: {exc}"}
        after = self.log_count()

        new = self.last_entries(after - before)
        delta = after - before
        record = {
            "trial": self.trial,
            "method": method,
            "path": path,
            "sent": note,
            "status": status,
            "response": payload,
            "new_log_entries": delta,
            "log_entry": new[-1] if new else None,
        }
        record["logged"] = delta == 1 and _entry_matches(path, new[0])
        self.ledger.append(record)
        return record


def _entry_matches(path: str, entry: dict) -> bool:
    """Does this log entry plausibly belong to a call on `path`?"""
    if "path" in entry:
        return entry["path"] == path
    if entry.get("event") == "appeal":
        return path == "/appeal"
    if entry.get("reason") == "rate_limited":
        return path == "/submit"
    if "event" not in entry and "label" in entry:      # a decision
        return path == "/submit"
    return False


def _error_of(record: dict):
    resp = record.get("response")
    return resp.get("error") if isinstance(resp, dict) else None


def _is_rejection(record: dict) -> bool:
    s = record.get("status")
    return s is not None and 400 <= s < 500 and s != 429 and _error_of(record) is not None


# ── The criteria ──────────────────────────────────────────────────────────────
# Each returns {"passed": bool, "summary": str, "cases": [...]}. A case is
# {"case": name, "expected": str, "ok": bool, "record": ledger row}.

def criterion_1_calls(client: Client) -> list[dict]:
    """
    Make the calls criterion 1 needs on its own. The verdict comes later, over
    every call in the trial.
    """
    cases = []

    def case(name, expected, record):
        cases.append({"case": name, "expected": expected, "ok": record["logged"], "record": record})
        return record

    good = case("valid submit", "200, logged", client.call(
        "/submit", {"text": PROSE, "creator_id": client.creator()}, note="valid prose"))
    content_id = (good.get("response") or {}).get("content_id")

    case("submit: malformed JSON", "400, logged", client.call(
        "/submit", raw=b'{"text": "hello", ', note="{\"text\": \"hello\", (truncated)"))
    case("submit: form-encoded", "400, logged", client.call(
        "/submit", raw=b"text=hello&creator_id=x",
        content_type="application/x-www-form-urlencoded", note="form-encoded body"))
    case("submit: JSON list", "400, logged", client.call(
        "/submit", [PROSE], note="[\"...\"]"))
    case("submit: missing text", "400, logged", client.call(
        "/submit", {"creator_id": client.creator()}, note="no text field"))
    case("submit: GET", "405, logged", client.call(
        "/submit", method="GET", note="GET /submit"))

    if content_id:
        case("valid appeal", "200, logged", client.call(
            "/appeal", {"content_id": content_id, "reasoning": "I wrote this myself."},
            note="appeal on the valid submit"))
    else:
        print("      (valid submit failed, so the valid-appeal case was skipped)")
    case("appeal: unknown id", "404, logged", client.call(
        "/appeal", {"content_id": "00000000-0000-4000-8000-000000000000",
                    "reasoning": "This id was never issued."}, note="unknown uuid"))
    case("appeal: invalid id", "400, logged", client.call(
        "/appeal", {"content_id": "not-a-uuid", "reasoning": "x"}, note="not a uuid"))
    case("appeal: no reasoning", "400, logged", client.call(
        "/appeal", {"content_id": content_id or "00000000-0000-4000-8000-000000000000"},
        note="no reasoning"))
    case("appeal: malformed JSON", "400, logged", client.call(
        "/appeal", raw=b"{content_id:", note="{content_id: (malformed)"))
    case("appeal: GET", "405, logged", client.call(
        "/appeal", method="GET", note="GET /appeal"))
    return cases


def criterion_1_verdict(client: Client, own_cases: list[dict]) -> dict:
    rows = [r for r in client.ledger if r["trial"] == client.trial]
    missed = [r for r in rows if not r["logged"]]
    return {
        "passed": not missed and bool(rows),
        "summary": f"{len(rows) - len(missed)}/{len(rows)} logged",
        "cases": own_cases,
        "missed": missed,
    }


def criterion_2_length(client: Client) -> dict:
    should_reject = [
        ("empty", ""),
        ("whitespace only", "   \n\t  "),
        ("one word", "Hello"),
        ("four words", "This is too short."),
        (f"{config.MAX_TEXT_CHARS + 1:,} chars", make_prose(config.MAX_TEXT_CHARS + 1)),
        ("10,000 chars", make_prose(10_000)),
        ("100,000 chars", make_prose(100_000)),
    ]
    # Controls: right on the limits, so these should be accepted. They show the
    # limits are where config.py says, rather than "everything is rejected".
    # They're reported but don't count toward the verdict.
    controls = [
        (f"exactly {config.MIN_TEXT_WORDS} words", "This sentence has five words."),
        (f"exactly {config.MAX_TEXT_CHARS:,} chars", make_prose(config.MAX_TEXT_CHARS)),
    ]

    cases = []
    for name, text in should_reject:
        r = client.call("/submit", {"text": text, "creator_id": client.creator()}, note=name)
        cases.append({"case": name, "expected": "4xx rejection", "ok": _is_rejection(r), "record": r})
    rejected = sum(c["ok"] for c in cases)

    control_ok = 0
    for name, text in controls:
        r = client.call("/submit", {"text": text, "creator_id": client.creator()}, note=name)
        ok = r["status"] == 200
        control_ok += ok
        cases.append({"case": f"(control) {name}", "expected": "200 accepted", "ok": ok,
                      "record": r, "control": True})

    return {
        "passed": rejected == len(should_reject),
        "summary": f"{rejected}/{len(should_reject)} rejected · controls {control_ok}/{len(controls)}",
        "cases": cases,
    }


def criterion_3_creator(client: Client) -> dict:
    bad = [
        ("no creator_id", {"text": PROSE}),
        ("creator_id null", {"text": PROSE, "creator_id": None}),
        ("creator_id empty", {"text": PROSE, "creator_id": ""}),
        ("creator_id whitespace", {"text": PROSE, "creator_id": "   "}),
        ("creator_id number", {"text": PROSE, "creator_id": 12345}),
        ("creator_id list", {"text": PROSE, "creator_id": ["abc"]}),
    ]
    cases = []
    for name, body in bad:
        r = client.call("/submit", body, note=name)
        cases.append({"case": name, "expected": "4xx error", "ok": _is_rejection(r), "record": r})

    plain, padded, accented = client.creator(), client.creator(), "créatrice_" + client.creator()
    good = [
        ("plain creator_id", plain, plain),
        ("padded creator_id", f"  {padded}  ", padded),
        ("accented creator_id", accented, accented),
    ]
    for name, sent, expected in good:
        r = client.call("/submit", {"text": PROSE, "creator_id": sent}, note=name)
        entry = r.get("log_entry") or {}
        cid = (r.get("response") or {}).get("content_id") if isinstance(r.get("response"), dict) else None
        ok = (r["status"] == 200 and cid is not None
              and entry.get("content_id") == cid
              and entry.get("creator_id") == expected)
        cases.append({"case": name, "expected": f"200, logged as {expected!r}", "ok": ok, "record": r})

    passed = sum(c["ok"] for c in cases)
    return {"passed": passed == len(cases), "summary": f"{passed}/{len(cases)} correct", "cases": cases}


NON_PROSE = [
    ("emoji", "emoji only (faces)", "😀😂🤣😍🥰😎🤩🥳😇🙃😉😊😋😜🤪😝🤑🤗🤭🤫"),
    ("emoji", "emoji only (spaced)", "🔥🔥🔥 💯 🙌🙌 👏👏👏 🎉🎉 ✨✨✨ 🚀🚀 😂😂 💀 🙏"),
    ("symbols", "ASCII symbols", "@#$%^&*()_+-=[]{}|;':\",./<>? ~~~ !!! ??? ### $$$ %%% &&& ***"),
    ("symbols", "unicode symbols", "→ ← ↑ ↓ ★ ☆ ♠ ♣ ♥ ♦ © ® ™ § ¶ † ‡ • … ‰ ∞ ≈ ≠ ≤ ≥"),
    ("non-English letters", "Russian (Cyrillic)",
     "Быстрая коричневая лиса прыгает через ленивую собаку. Это простое предложение для проверки системы."),
    ("non-English letters", "Vietnamese (accented Latin)",
     "Tôi đã đi chợ hôm qua và mua rất nhiều trái cây tươi ngon cho cả gia đình."),
    ("right-to-left", "Arabic",
     "الثعلب البني السريع يقفز فوق الكلب الكسول. هذه جملة بسيطة لاختبار النظام."),
    ("right-to-left", "Hebrew",
     "השועל החום המהיר קופץ מעל הכלב העצלן. זה משפט פשוט כדי לבדוק את המערכת."),
    ("code", "Python",
     "def score(text):\n    words = text.split()\n    if not words:\n        return 0\n"
     "    return sum(len(w) for w in words) / len(words)"),
    ("code", "JavaScript",
     "const items = [1, 2, 3];\nfor (let i = 0; i < items.length; i++) {\n"
     "  console.log(items[i] * 2);\n}"),
]


def criterion_4_non_prose(client: Client) -> dict:
    cases = []
    for category, name, text in NON_PROSE:
        r = client.call("/submit", {"text": text, "creator_id": client.creator()}, note=name)
        cases.append({"case": f"{category}: {name}", "expected": "4xx rejection",
                      "ok": _is_rejection(r), "record": r})
    rejected = sum(c["ok"] for c in cases)
    return {
        "passed": rejected / len(cases) >= 0.8,
        "summary": f"{rejected}/{len(cases)} rejected ({rejected / len(cases):.0%})",
        "cases": cases,
    }


def criterion_5_model_failure(client: Client) -> dict:
    r = client.call("/submit", {"text": PROSE, "creator_id": client.creator()},
                    note="valid prose, model broken")
    status = r["status"]
    entry = r.get("log_entry") or {}

    is_5xx = status is not None and 500 <= status < 600
    is_json_error = _error_of(r) is not None
    error_logged = r["new_log_entries"] == 1 and (
        entry.get("event") == "error" or (entry.get("http_status") or 0) >= 500)
    try:
        health_status = requests.get(f"{client.url}/health", timeout=30).status_code
    except requests.RequestException:
        health_status = None
    health_ok = health_status == 200

    if status == 200:
        print("      !! /submit returned 200. Is DETECTOR_MODEL actually broken, and was app.py restarted?")

    checks = [
        ("5xx status", f"got {status}", is_5xx),
        ("JSON error body", f"error={_error_of(r)!r}", is_json_error),
        ("error entry logged", f"event={entry.get('event')!r} http_status={entry.get('http_status')!r}",
         error_logged),
        ("/health afterwards", f"got {health_status}", health_ok),
    ]
    cases = [{"case": name, "expected": "", "ok": ok, "record": r, "detail": detail}
             for name, detail, ok in checks]
    passed = sum(ok for _, _, ok in checks)
    return {"passed": passed == len(checks), "summary": f"{passed}/{len(checks)} checks", "cases": cases}


RUNNERS = {2: criterion_2_length, 3: criterion_3_creator, 4: criterion_4_non_prose,
           5: criterion_5_model_failure}


# ── Running and reporting ─────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--criteria", default="1,2,3,4",
                        help="comma-separated, e.g. 1,2,3,4 (default) or 5")
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--timeout", type=float, default=120.0)
    args = parser.parse_args()

    try:
        selected = sorted({int(c) for c in args.criteria.split(",") if c.strip()})
    except ValueError:
        parser.error("--criteria takes numbers, e.g. 1,2,3,4")
    if not selected or any(c not in TARGETS for c in selected):
        parser.error("--criteria must be drawn from 1-5")

    try:
        health = requests.get(f"{args.url}/health", timeout=10).json()
    except Exception:  # noqa: BLE001
        print(f"Nothing answering at {args.url}. Start it:  python app.py", file=sys.stderr)
        sys.exit(1)
    print(f"Service up · detector_model={health.get('detector_model')!r} · "
          f"rate_limiting={health.get('rate_limiting')}")
    if 5 in selected and len(selected) > 1:
        print("!! Criterion 5 needs a broken model, and criteria 2-4 need a working one. "
              "Run 5 on its own.\n")
    if args.trials < 3:
        print(f"!! {args.trials} trial(s). The target has to hold across three.\n")

    client = Client(args.url, args.timeout)
    results = {c: [] for c in selected}

    for trial in range(1, args.trials + 1):
        client.trial = trial
        print(f"\nTrial {trial}")
        c1_cases = []
        for c in selected:
            print(f"  criterion {c}: {NAMES[c]}")
            if c == 1:
                c1_cases = criterion_1_calls(client)
                continue
            outcome = RUNNERS[c](client)
            results[c].append(outcome)
            print(f"    {'PASS' if outcome['passed'] else 'miss'}  {outcome['summary']}")
        if 1 in selected:
            # Judged last, so it covers every call this trial made for every criterion.
            outcome = criterion_1_verdict(client, c1_cases)
            results[1].append(outcome)
            print(f"  criterion 1 (all calls this trial): "
                  f"{'PASS' if outcome['passed'] else 'miss'}  {outcome['summary']}")

    print()
    for c in selected:
        verdict = "PASS" if all(t["passed"] for t in results[c]) else "MISS"
        print(f"  {c}. {NAMES[c]:<22} {verdict}   "
              + " | ".join(t["summary"] for t in results[c]))

    write_report(results, args, health)


def _cell(text) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def write_report(results: dict, args, health: dict):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"unit9_run_{stamp}{label}.md"

    n = args.trials
    lines = [
        f"# Unit 9 run log{f' ({args.label})' if args.label else ''}",
        "",
        "- Produced by: `run_eval_unit9.py`",
        f"- Service: {args.url} · detector_model `{health.get('detector_model')}` · "
        f"rate limiting {'on' if health.get('rate_limiting') else 'off'}",
        f"- {n} trials per criterion · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- A criterion passes only if every trial passes.",
        "",
        f"| Criterion | Target | {' | '.join(f'Run {i}' for i in range(1, n + 1))} | Verdict |",
        f"|---|---|{'|'.join(['---'] * n)}|---|",
    ]
    for c, trials in results.items():
        runs = " | ".join(f"{'✅' if t['passed'] else '❌'} {_cell(t['summary'])}" for t in trials)
        verdict = "**PASS**" if all(t["passed"] for t in trials) else "**MISS**"
        lines.append(f"| {c}. {NAMES[c]} | {_cell(TARGETS[c])} | {runs} | {verdict} |")

    lines += ["", "---", "", "## Case by case", ""]
    for c, trials in results.items():
        lines += [f"### {c}. {NAMES[c]}", ""]
        for i, t in enumerate(trials, 1):
            lines += [f"**Trial {i}**: {t['summary']}", "",
                      "| Case | Expected | Status | Error / detail | OK |",
                      "|---|---|---|---|---|"]
            for case in t["cases"]:
                rec = case["record"]
                detail = case.get("detail") or _error_of(rec) or ""
                lines.append(f"| {_cell(case['case'])} | {_cell(case['expected'])} | "
                             f"{rec['status']} | {_cell(detail)} | {'✅' if case['ok'] else '❌'} |")
            if c == 1:
                if t["missed"]:
                    lines += ["", "Calls in this trial **not** logged exactly once:", "",
                              "```json", json.dumps(t["missed"], indent=2, ensure_ascii=False), "```"]
                else:
                    lines += ["", f"Every /submit and /appeal call in trial {i}, across all "
                                  "criteria, added exactly one matching log entry."]
            lines.append("")

    lines += ["---", "", "## What actually came back", "",
              "Raw responses and the log entry each call produced, for the README.", ""]
    for c, trials in results.items():
        lines += [f"### {c}. {NAMES[c]}", ""]
        for i, t in enumerate(trials, 1):
            seen, rows = set(), []
            for case in t["cases"]:
                rec = case["record"]
                if id(rec) in seen:
                    continue
                seen.add(id(rec))
                rows.append({"case": case["case"], "status": rec["status"],
                             "response": rec["response"], "log_entry": rec["log_entry"]})
            lines += [f"**Trial {i}**", "", "```json",
                      json.dumps(rows, indent=2, ensure_ascii=False), "```", ""]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
