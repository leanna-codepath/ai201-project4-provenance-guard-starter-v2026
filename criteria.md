# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1.

Of 10 pieces I wrote myself, at most 1 is labeled high-confidence AI.


**Why this target:**

Since false accusations can be detremential to a human writer's reputation, I want to limit how often false positives occur.
1 is still allowed because it adds flexibility.

---

## 2.

Text I judge borderline scores between 0.4 and 0.6 in at least 4 of 5 cases.

**Why this target:**

If a text is borderline, then that means there should be a 50/50 chance of it being either label. This criteria judges if the
AI has this capability.

---

## 3.

When given test inputs that clearly fall under the three labels, the system should be able to produce each of these labels in
3/3 trials.


**Why this target:**
If a label can never be reached that implies the classficiation thresholds are poorly chosen or the scoring logic is broken.
Being able to reach all three labels means more confident conclusions when one is chosen over another.

---

## 4.

If the given input text is missing, empty, or over the maximum character limit, it should be rejected everytime.


**Why this target:**
Invalid input is one that cannot be judged, and letting it through introduces more problems along the line.

---

## 5.

All valid appeal tests much change status to appealed and get recorded in the system.

**Why this target:**

In a system that can make mistakes, there should always be a way to fix said mistakes. Including a record also
ensures that these changes can be tracked.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
