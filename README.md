# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

This project has 7 steps: an API endpoint that recieves a user's text, an input validation that confirms the text
meets any requirements, detector.py which reads the text for meaning and scores how predictable the text is, 
stylometry.py which measures the text format, a scoring logic that combines the measurements from the two signals,
classification logic that chooses a label for the text, and an API response returned to the user.

---

## Signals and Scoring

### Signal one — the model signal

**What it measures:**
Reads the text's meaning and measures how predictable it is, i.e. its perplexity. It returns a score from 0-1 with a 
higher score means it's more likely AI.

**Why that might differ between human and AI writing:**
AI writing is often more predictable while human writing is usually less so, with more odd word turns, abrupt turns, etc.

**What it can't see:**
The signal rewards common words in short sentences. It cannot see if this is just the author's natural way of writing. It also
can't see if someone has prompted an AI to write in more flowery prose, which is often deemed more human.

### Signal two — the style signal

**What it measures:**
This signal measures the text itself, including how much the sentences vary in length, how repetitive the vocabulary is,
and how varied the punctuation is.

**Why that might differ between human and AI writing:**
AI writing tends to have more even structure and a less diverse vocab, while human writing is less even and has more
diversity.

**What it can't see:**
The signal can't see what the text says. If the text structure changes in a way that does not match the content, it can't
tell the difference.

### The combining rule

**The rule:**

The system is weighted slightly more towards the model than the style, putting the content of the text ocer the style/text format.
If the two signals disagree by more than 0.4, lean toward the more-human of the two, because a false accusation costs more than a miss.

**The numbers:**
The weighted average is (model 0.6, style 0.4). If abs(model_score - style_score) > 0.4, lean towards the more human measurement.

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**

A case where the two split is on the text "I think a lot of the time, we overcomplicate things. Sometimes you just need to take a step back, figure out what actually matters, and go from there. It’s not always that deep."

In this case, the model would lean towards the style score, as that's the more human score.

---

## Label Variants


| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00-0.35 | This text was most likely written by a human |
| unsure | 0.35-0.60 | This text shares both human writing characteristics and AI-written characteristics. It could be human-written or AI-written |
| high-confidence AI | 0.60-1.00 | This text was most likely written by an AI. If this is incorrect, it can be appealed. |

**Why I worded the "unsure" one this way:**
I worded the "unsure" label in a succient, straightforward way as to minimize any accusations or blame.


---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "The purpose of this statement is to provide a clear, concise, and formal overview of the subject under consideration. All information is presented in a consistent manner, maintaining a uniform tone, precise wording, and professional structure throughout the paragraph.", "creator_id": "11"}'
```

```json
{
  "confidence": 0.6265,
  "content_id": "983d1fd5-4f87-49d2-b5dd-0b26a7c77058",
  "guess": "ai",
  "label": "This text was most likely written by an AI. If this is incorrect, it can be appealed.",
  "model_score": 0.7599,
  "style_score": 0.4265
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "983d1fd5-4f87-49d2-b5dd-0b26a7c77058", "reasoning": "I wrote this myself. It is my own casual writing style."}'
```

```json
{
  "content_id": "983d1fd5-4f87-49d2-b5dd-0b26a7c77058",
  "message": "Thanks. Your appeal was received, and a person will review this decision.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{                                                                                                                                                                                                                                                                                                                                                            
  "count": 3,
  "entries": [
    {
      "combined_score": 0.6265,
      "content_id": "a807a05d-8a1c-4333-8a10-344b4b3afe9b",
      "creator_id": "10",
      "guess": "ph",
      "label": "ph",
      "model_score": 0.7599,
      "status": "decided",
      "style_score": 0.4265,
      "timestamp": "2026-10-23T22:13:58+00:00"
    },
    {
      "combined_score": 0.6265,
      "content_id": "983d1fd5-4f87-49d2-b5dd-0b26a7c77058",
      "creator_id": "11",
      "guess": "ai",
      "label": "This text was most likely written by an AI. If this is incorrect, it can be appealed.",
      "model_score": 0.7599,
      "status": "decided",
      "style_score": 0.4265,
      "timestamp": "2026-10-23T22:28:29+00:00"
    },
    {
      "content_id": "983d1fd5-4f87-49d2-b5dd-0b26a7c77058",
      "creator_id": "11",
      "event": "appeal",
      "reasoning": "I wrote this myself. It is my own casual writing style.",
      "status": "under_review",
      "timestamp": "2026-10-23T22:30:33+00:00"
    }
  ]
}
```
---

## How I Used AI

**Moment 1**

- *What I asked for:* I asked for general guidance on how the style signal should analyze the text.
- *What came back:* The model gave me instructions on how to analyze the sentence structure.
- *What I changed:* The model didn't consider different human writing styles, such as run on sentences, so I had to add those cases.

**Moment 2**

- *What I asked for:* I asked whether the thresholds for my labels seemed correct.
- *What came back:* The AI confirmed that they seemed fine.
- *What I changed:* I thought the AI label threshol seemed to high, especially since my style signal was changed to lean more human, so I lowered it.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day

**Why those numbers and not others:**


**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
15 submissions as 'flood_tester' against http://127.0.0.1:5000
The first one is slow while the model loads.

  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 429
  [ 7/15] 429
  [ 8/15] 429
  [ 9/15] 429
  [10/15] 429
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429

============================================================
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
============================================================
```

---

## Attack Run — Before

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `f2ee2484-cfed-43ae-a313-d64b70efe4db` | human | 0.313 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `dc98c02e-e58f-4404-944f-d5f17e2b92e5` | unsure | 0.474 | HELD |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `9128043d-4c52-4bfe-9c42-c1af7b58c710` | unsure | 0.564 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `95c4437a-136a-47f6-8d42-01bb3f13b80c` | unsure | 0.570 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `04a109b3-0f2f-4405-9f05-77f419ef80ae` | human | 0.302 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `866add3f-9abb-419a-a08d-14933c3405f9` | unsure | 0.481 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | `1df25e1d-01dc-4c6c-befa-79008b3b789b` | human | 0.313 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `68e1ee6a-154f-4632-9773-fff575300a58` | unsure | 0.367 | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `94664725-3d15-4eae-8474-9c05352a50fb` | unsure | 0.584 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `c25c2ed6-7342-43b9-b615-a4132b1c1cc8` | ai | 0.879 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `e670c245-fdad-425b-a888-9c51e8b87da8` | unsure | 0.583 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `0cb52340-c24e-4544-ba8b-196644769cad` | ai | 0.697 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `4a7ca2f6-0e52-4b13-8a25-9391003c709a` | ai | 0.732 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `d60ea707-0be7-466a-a2be-5e68313eb3b7` | ai | 0.718 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `b559b7a8-b162-45d7-b2b8-8c5e1686d79c` | ai | 0.731 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `fd83d9d9-3a73-45b7-9402-ca931c9fe1a6` | ai | 0.731 | BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `d99eac3e-4900-48ba-a124-058760e10fec` | ai | 0.668 | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `b2515285-9592-47ba-99a7-ecd57197fc33` | unsure | 0.388 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `666abd2c-44db-45bc-b7ea-b530987b9580` | unsure | 0.443 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `e48258e7-5830-4e98-8f90-3c47299cb557` | human | 0.247 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `f38fea0f-0e18-4aca-85d2-e2e88f5228b2` | unsure | 0.530 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `5bfd1d40-544c-4e0e-a400-ff80d62671ca` | unsure | 0.449 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `0c1b2952-e6e4-479e-9060-44d0ed509ffa` | human | 0.348 | BROKE |
| PI06 | prompt_injection | instruction plus real human text | 200 | `f0dbedfd-2db4-4f71-8804-fdd1b0932ea1` | unsure | 0.551 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `fde61a54-2a88-4613-b1f9-9662fe91400c` | human | 0.200 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `4526bc7f-eda0-41e6-a675-361bf4cac8b0` | human | 0.211 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | `540fa4e0-4dea-4c0f-a132-5493c9fd8a15` | ai | 0.700 | HELD |
| MF06 | malformed | text is emoji only | 200 | `a578a0c2-83e6-48eb-b9dc-a6756b9c7d3b` | ai | 0.998 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `4e558144-99c0-494e-993e-921cfaa22232` | ai | 0.944 | BROKE |
| MF08 | malformed | text is 60,000 characters | 200 | `90435e7a-cb1a-4c7f-93fe-2deb82536bf7` | ai | 0.903 | BROKE |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | `9a07ac29-d12f-4c70-b3cd-dd60c293a795` | human | 0.344 | BROKE |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 200 | `ebd40349-9445-43ea-baed-c61a8fc2c969` | human | 0.230 | BROKE |
| RQ07 | malformed | body is a JSON array, not an object | 500 | `—` | — | — | BROKE |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `43814808-3d7f-4a48-b072-41c815f2093f` | human | 0.217 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e903dbc5-3829-4707-85da-b69dd3a49496` | human | 0.217 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `6ff9e673-4a94-4c67-8c25-644726e1efe7` | human | 0.217 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9e5b6368-21d8-44dd-ae4f-62f0a9600b23` | human | 0.217 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b9e5231d-c146-48af-8ab3-2230d647ccb7` | human | 0.217 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |



**Ten audit log entries from the run**

```json
{"timestamp": "2026-10-30T21:32:05+00:00", "content_id": "f2ee2484-cfed-43ae-a313-d64b70efe4db", "creator_id": "attacker_EV01", "guess": "human", "model_score": 0.1635, "style_score": 0.5383, "combined_score": 0.3134, "label": "This text was most likely written by a human", "status": "decided"}
{"timestamp": "2026-10-30T21:32:09+00:00", "content_id": "4a7ca2f6-0e52-4b13-8a25-9391003c709a", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.6223, "combined_score": 0.732, "label": "This text was most likely written by an AI. If this is incorrect, it can be appealed.", "status": "decided"}
{"timestamp": "2026-10-30T21:32:09+00:00", "content_id": "d60ea707-0be7-466a-a2be-5e68313eb3b7", "creator_id": "attacker_FP04", "guess": "ai", "model_score": 0.8329, "style_score": 0.5449, "combined_score": 0.7177, "label": "This text was most likely written by an AI. If this is incorrect, it can be appealed.", "status": "decided"}
{"timestamp": "2026-10-30T21:32:10+00:00", "content_id": "e48258e7-5830-4e98-8f90-3c47299cb557", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.3111, "combined_score": 0.2471, "label": "This text was most likely written by a human", "status": "decided"}
{"timestamp": "2026-10-30T21:32:11+00:00", "content_id": "0c1b2952-e6e4-479e-9060-44d0ed509ffa", "creator_id": "attacker_PI05", "guess": "human", "model_score": 0.6401, "style_score": 0.148, "combined_score": 0.348, "label": "This text was most likely written by a human", "status": "decided"}
{"timestamp": "2026-10-30T21:32:11+00:00", "content_id": "fde61a54-2a88-4613-b1f9-9662fe91400c", "creator_id": "attacker_MF03", "guess": "human", "model_score": 0.0, "style_score": 0.5, "combined_score": 0.2, "label": "This text was most likely written by a human", "status": "decided"}
{"timestamp": "2026-10-30T21:32:11+00:00", "content_id": "4526bc7f-eda0-41e6-a675-361bf4cac8b0", "creator_id": "attacker_MF04", "guess": "human", "model_score": 0.0112, "style_score": 1.0, "combined_score": 0.2112, "label": "This text was most likely written by a human", "status": "decided"}
{"timestamp": "2026-10-30T21:32:13+00:00", "content_id": "4e558144-99c0-494e-993e-921cfaa22232", "creator_id": "attacker_MF07", "guess": "ai", "model_score": 0.9064, "style_score": 1.0, "combined_score": 0.9438, "label": "This text was most likely written by an AI. If this is incorrect, it can be appealed.", "status": "decided"}
{"timestamp": "2026-10-30T21:32:14+00:00", "content_id": "ebd40349-9445-43ea-baed-c61a8fc2c969", "creator_id": {"id": "x"}, "guess": "human", "model_score": 0.0492, "style_score": 0.5, "combined_score": 0.2295, "label": "This text was most likely written by a human", "status": "decided"}
{"timestamp": "2026-10-30T21:32:15+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:
The single worst outcome is that a text written carefully by a non-native English speaker was labelled as 'ai'.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
