# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-10-30 19:40
- Auto-marked BROKE (5xx, crash, no response): **2**
- Left for you to judge: **54**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `4471d767-1552-473d-9db2-ba62497aef5c` | unsure | 0.370 | HELD |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `734d9340-cfdf-4c94-8675-60ad0176e01e` | unsure | 0.429 | HELD |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `0b7fba72-6a03-4d50-b071-cf4a7ea61ead` | unsure | 0.525 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `a5190adb-7c05-4808-9fa5-f55c22cbd1cc` | unsure | 0.554 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `73fa62f6-4460-4d89-b8a2-f052fbe637a1` | human | 0.295 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `d5f78231-e885-472e-959b-bee4a3b45505` | unsure | 0.447 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | `e237ce1b-1c8d-4193-a0a2-ad90fdaaa213` | human | 0.313 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `3bfb05f1-d5ee-45de-85bb-74c771710f85` | unsure | 0.412 | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `54de37d4-0b33-41e4-a047-cee8e9e839e9` | unsure | 0.538 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `c8518426-9cfd-4cd9-a13e-566086e1a713` | ai | 0.842 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `f7d97858-5892-4f0d-a855-becf1c44afd3` | unsure | 0.569 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `450ac9a4-0d61-4552-9489-6154466a4613` | ai | 0.681 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `2c6d57ff-86bf-40f2-9974-ecdec9e08a98` | ai | 0.705 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `e27aea59-e5c2-4a3c-aef9-3f7a9b60ab9b` | ai | 0.674 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `b0ac175c-5354-44ed-9f04-a0580ef962bf` | ai | 0.705 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `1da64918-588b-425a-8693-c3f846822adb` | ai | 0.674 | BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `e8e9f84c-aa06-4350-b53c-1a8ac5f7badc` | ai | 0.654 | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `2148a074-b06a-488b-9b17-eaf178fb9bb0` | unsure | 0.412 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `6400b8af-33ea-4778-bde3-bfca887682b1` | unsure | 0.435 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `271843b8-8cbd-4e0e-a54d-aebf16f75b7b` | human | 0.263 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `96fd6d5a-f009-43b8-aa44-9b1c3c58c440` | unsure | 0.505 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `95c32c92-4f29-4f73-9cdf-6e70ef804da5` | unsure | 0.430 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `f54e5a82-bee4-4773-b326-850ccfa16aaf` | human | 0.348 | BROKE |
| PI06 | prompt_injection | instruction plus real human text | 200 | `356d23b2-5241-4aae-be03-316708063ed7` | unsure | 0.548 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `f52911a5-2fae-404f-b40c-6b1dcd245ee2` | human | 0.200 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `370a0523-e329-4229-bfd0-a1ab9d444299` | human | 0.211 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | `54a3104c-65d7-45ae-9bea-6a6c6021169a` | ai | 0.700 | BROKE |
| MF06 | malformed | text is emoji only | 200 | `697b4827-0d1f-4ec3-83c5-113396417b81` | ai | 0.999 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `79ec1eed-8771-4a6b-92d3-80ee71905144` | ai | 0.958 | BROKE |
| MF08 | malformed | text is 60,000 characters | 200 | `f6524eba-5c23-4bfe-8f63-a877d01e6897` | ai | 0.871 | BROKE |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | `dc6ca12b-43e4-4ae7-8148-d203abf822a0` | unsure | 0.383 | BROKE |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 200 | `8421e258-7418-4a8b-8646-277168dba949` | human | 0.249 | BROKE |
| RQ07 | malformed | body is a JSON array, not an object | 500 | `—` | — | — | BROKE |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d1d6f898-22c6-4446-8c26-d56119154327` | human | 0.229 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f72b8d18-6d96-442f-9c62-b9cfa6e4de23` | human | 0.229 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5e6d7468-77c0-452f-aa97-320bcf51619c` | human | 0.229 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `fb74e752-8470-4001-8750-d5712a4dab14` | human | 0.229 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `27ff9f2c-97d3-49f9-ad14-5553cbdce1a7` | human | 0.229 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 2 | 18 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "4471d767-1552-473d-9db2-ba62497aef5c",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.3696,
  "model_score": 0.1635,
  "style_score": 0.5383,
  "label": "This text shares both human writing characteristics and AI-written characteristics. It could be human-written or AI-written.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "734d9340-cfdf-4c94-8675-60ad0176e01e",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4293,
  "model_score": 0.5943,
  "style_score": 0.2943,
  "label": "This text shares both human writing characteristics and AI-written characteristics. It could be human-written or AI-written.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "0b7fba72-6a03-4d50-b071-cf4a7ea61ead",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5251,
  "model_score": 0.6662,
  "style_score": 0.4096,
  "label": "This text shares both human writing characteristics and AI-written characteristics. It could be human-written or AI-written.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "a5190adb-7c05-4808-9fa5-f55c22cbd1cc",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5543,
  "model_score": 0.6114,
  "style_score": 0.5076,
  "label": "This text shares both human writing characteristics and AI-written characteristics. It could be human-written or AI-written.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "73fa62f6-4460-4d89-b8a2-f052fbe637a1",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2946,
  "model_score": 0.3212,
  "style_score": 0.2728,
  "label": "This text was most likely written by a human",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "d5f78231-e885-472e-959b-bee4a3b45505",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.447,
  "model_score": 0.5727,
  "style_score": 0.3442,
  "label": "This text shares both human writing characteristics and AI-written characteristics. It could be human-written or AI-written.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "e237ce1b-1c8d-4193-a0a2-ad90fdaaa213",
  "creator_id": "attacker_EV07",
  "guess": "human",
  "confidence": 0.3134,
  "model_score": 0.5862,
  "style_score": 0.1134,
  "label": "This text was most likely written by a human",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "3bfb05f1-d5ee-45de-85bb-74c771710f85",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.4122,
  "model_score": 0.2452,
  "style_score": 0.5488,
  "label": "This text shares both human writing characteristics and AI-written characteristics. It could be human-written or AI-written.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "54de37d4-0b33-41e4-a047-cee8e9e839e9",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5384,
  "model_score": 0.7042,
  "style_score": 0.4028,
  "label": "This text shares both human writing characteristics and AI-written characteristics. It could be human-written or AI-written.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "c8518426-9cfd-4cd9-a13e-566086e1a713",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8416,
  "model_score": 0.9792,
  "style_score": 0.729,
  "label": "This text was most likely written by an AI. If this is incorrect, it can be appealed.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "f7d97858-5892-4f0d-a855-becf1c44afd3",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5694,
  "model_score": 0.6175,
  "style_score": 0.53,
  "label": "This text shares both human writing characteristics and AI-written characteristics. It could be human-written or AI-written.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "450ac9a4-0d61-4552-9489-6154466a4613",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.681,
  "model_score": 0.7387,
  "style_score": 0.6338,
  "label": "This text was most likely written by an AI. If this is incorrect, it can be appealed.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "2c6d57ff-86bf-40f2-9974-ecdec9e08a98",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7046,
  "model_score": 0.8051,
  "style_score": 0.6223,
  "label": "This text was most likely written by an AI. If this is incorrect, it can be appealed.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "e27aea59-e5c2-4a3c-aef9-3f7a9b60ab9b",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.6745,
  "model_score": 0.8329,
  "style_score": 0.5449,
  "label": "This text was most likely written by an AI. If this is incorrect, it can be appealed.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "b0ac175c-5354-44ed-9f04-a0580ef962bf",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7045,
  "model_score": 0.8005,
  "style_score": 0.6259,
  "label": "This text was most likely written by an AI. If this is incorrect, it can be appealed.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "1da64918-588b-425a-8693-c3f846822adb",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.6739,
  "model_score": 0.8814,
  "style_score": 0.5042,
  "label": "This text was most likely written by an AI. If this is incorrect, it can be appealed.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "e8e9f84c-aa06-4350-b53c-1a8ac5f7badc",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.6539,
  "model_score": 0.8816,
  "style_score": 0.4676,
  "label": "This text was most likely written by an AI. If this is incorrect, it can be appealed.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "2148a074-b06a-488b-9b17-eaf178fb9bb0",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.4124,
  "model_score": 0.3223,
  "style_score": 0.4862,
  "label": "This text shares both human writing characteristics and AI-written characteristics. It could be human-written or AI-written.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "6400b8af-33ea-4778-bde3-bfca887682b1",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4352,
  "model_score": 0.4625,
  "style_score": 0.4128,
  "label": "This text shares both human writing characteristics and AI-written characteristics. It could be human-written or AI-written.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "271843b8-8cbd-4e0e-a54d-aebf16f75b7b",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2631,
  "model_score": 0.2044,
  "style_score": 0.3111,
  "label": "This text was most likely written by a human",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "96fd6d5a-f009-43b8-aa44-9b1c3c58c440",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5055,
  "model_score": 0.5943,
  "style_score": 0.4328,
  "label": "This text shares both human writing characteristics and AI-written characteristics. It could be human-written or AI-written.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "95c32c92-4f29-4f73-9cdf-6e70ef804da5",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.43,
  "model_score": 0.4998,
  "style_score": 0.3728,
  "label": "This text shares both human writing characteristics and AI-written characteristics. It could be human-written or AI-written.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "f54e5a82-bee4-4773-b326-850ccfa16aaf",
  "creator_id": "attacker_PI05",
  "guess": "human",
  "confidence": 0.348,
  "model_score": 0.6401,
  "style_score": 0.148,
  "label": "This text was most likely written by a human",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "356d23b2-5241-4aae-be03-316708063ed7",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5477,
  "model_score": 0.5583,
  "style_score": 0.5391,
  "label": "This text shares both human writing characteristics and AI-written characteristics. It could be human-written or AI-written.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "f52911a5-2fae-404f-b40c-6b1dcd245ee2",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.2,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "This text was most likely written by a human",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "370a0523-e329-4229-bfd0-a1ab9d444299",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.2112,
  "model_score": 0.0112,
  "style_score": 1.0,
  "label": "This text was most likely written by a human",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "54a3104c-65d7-45ae-9bea-6a6c6021169a",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.7,
  "model_score": 0.9976,
  "style_score": 0.5,
  "label": "This text was most likely written by an AI. If this is incorrect, it can be appealed.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "697b4827-0d1f-4ec3-83c5-113396417b81",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.9986,
  "model_score": 0.9969,
  "style_score": 1.0,
  "label": "This text was most likely written by an AI. If this is incorrect, it can be appealed.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "79ec1eed-8771-4a6b-92d3-80ee71905144",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9579,
  "model_score": 0.9064,
  "style_score": 1.0,
  "label": "This text was most likely written by an AI. If this is incorrect, it can be appealed.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "f6524eba-5c23-4bfe-8f63-a877d01e6897",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.8714,
  "model_score": 0.9876,
  "style_score": 0.7763,
  "label": "This text was most likely written by an AI. If this is incorrect, it can be appealed.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "dc6ca12b-43e4-4ae7-8148-d203abf822a0",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.3828,
  "model_score": 0.2395,
  "style_score": 0.5,
  "label": "This text shares both human writing characteristics and AI-written characteristics. It could be human-written or AI-written.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "8421e258-7418-4a8b-8646-277168dba949",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.2492,
  "model_score": 0.0492,
  "style_score": 0.5,
  "label": "This text was most likely written by a human",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 500,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>AttributeError: &#39;list&#39; object has no attribute &#39;get&#39;\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes",
  "verdict": "BROKE"
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "d1d6f898-22c6-4446-8c26-d56119154327",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2287,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This text was most likely written by a human",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "f72b8d18-6d96-442f-9c62-b9cfa6e4de23",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2287,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This text was most likely written by a human",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "5e6d7468-77c0-452f-aa97-320bcf51619c",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2287,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This text was most likely written by a human",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "fb74e752-8470-4001-8750-d5712a4dab14",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2287,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This text was most likely written by a human",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "27ff9f2c-97d3-49f9-ad14-5553cbdce1a7",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2287,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This text was most likely written by a human",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
