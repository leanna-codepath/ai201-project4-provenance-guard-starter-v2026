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

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



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
