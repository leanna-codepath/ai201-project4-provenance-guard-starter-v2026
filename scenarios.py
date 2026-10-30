"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        "texts": [
            "I often question why ten paragraphs is the accepted number. Seriously, how much time do I have to dedicate to these things. How long should these paragraphs be too, one sentence, three, five!?",
            "Dogs are some of the cutest creatures in existence. They come in so many shapes and sizes too! Fluffy, smooth, tall, short, etc. It's a wonder how much a diverse group of animals all apparently stemmed from wolves; human ingenuity is amazing.",
            "Streaming has become somewhat controversial as of late. It used to be something people subscribed to because they wanted to avoid the normal ads on television. Now they've added tiers, introducing their own ads and defeating the whole point of an already paid service.",
            "Speaking of, I'm tired of how many services require a subscription nowadays. Seriously, why does nothing accept a one-time payment anymore? It's irritating and becomes confusing for the general audience. An overall predatory practice.",
            "I guess this could be considered a creative writing exercise. I don't often have opportunities to just write my thoughts out these days. It does become a bit dull when I don't have much to write about, however.",
            "The first thing the user did upon entering the site was click the search bar, at which point she clicked on one of the trending searches that appeared: 'Restaurants.' After the search had loaded, she tried to change the location to be closer to her, but had difficulties, as typing in the zip code or a shortened version of the address didn’t result in any changes. ",
            "The scene during New Year's Eve where we are witness to the juxtaposition of both The Prospector staring mournful from his lonely cabin and the cheerful scene of Aula being sung as the Dancing Hall. While we have spent the first half of the movie laughing at his endeavors, his plights, and his disasters, we have also become connected to the man. Especially when it was set right after a dream where The Prospector only wants to have some fun/have people to laugh with and the audience must feel for him. ",
            "Edit the color palette of the Styles section. I used my previous website as the basis and ended up with the following colors: 673AB7, 6A3ADB, A384D8, 772E9B, F6F3FB, 006633, FFCC33, 51A37D. These should be added to the Color Styles section of the Design Styles for easier access. ",
            "Environmental science is an admirable field of study, where students dedicate themselves to better understanding the world around them. Often, this also results in them looking for ways to benefit and save our nature. In another world, I like to imagine I was one of these adventurers.",
            "And so we come to our finale. There is more to be done, but in this instance I will have to say goodbye. My best wishes to you. I am sure we will meet again some day, where there shines a brighter sun."
        ],
    },
        {
        "name": "borderline falls between 0.4 and 0.6",
        "criterion": 2,
        "texts": [
           "I wanted to make something meaningful, but I wasn't really sure where to start. So I just went with the first idea that felt right.",
           "Technology has made our lives easier in many ways, but it has also made it harder to disconnect and enjoy the little things.",
           "I think sometimes we get so caught up in planning for the future that we forget to appreciate what's happening right now."
        ],
    }, 
    {
        "name": "label coverage",
        "criterion": 3,
        "texts": [
            "Greetings, esteemed individual! I hope this message finds you well. In today's rapidly evolving digital landscape, it is imperative to recognize the transformative potential of artificial intelligence. By leveraging innovative solutions, embracing cutting-edge technologies, and fostering a culture of continuous improvement, we can unlock unprecedented opportunities and drive meaningful outcomes. Ultimately, the possibilities are limitless, and the future is brighter than ever!",
            "I liked to dance with the waves and enjoy myself on sunny days. When clouds appear, I instead cuddle up inside, trying to bide my time. Waiting for another sunny day.",
            "The importance of effective communication in the workplace cannot be overstated. Really. Teams that communicate clearly are better positioned to achieve their objectives and avoid costly misunderstandings. Really. There are several strategies organisations can adopt to improve this. Really. First — establishing regular check-ins ensures that information flows consistently between team members. Really. Second — documenting decisions provides a reference point that reduces ambiguity. Really. Finally — encouraging an environment where questions are welcomed helps surface issues early. Really. Implementing these approaches can lead to meaningful improvements in team performance and overall satisfaction.",
        ],
    },    
    {
        "name": "bad input",
        "criterion": 4,
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"creator_id": "eval_bad_missing"},
            {"text": "word " * 50000, "creator_id": "eval_bad_huge"},
            {"text": None, "creator_id": "eval_bad_null"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")
        appeals = scenario.get("appeals")

        if sum(bool(x) for x in (texts, bodies, appeals)) > 1:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has more than one of "
                f"texts, bodies and appeals — pick one"
            )
            continue

        if appeals:
            for j, appeal in enumerate(appeals, 1):
                if not isinstance(appeal, dict) or not str(appeal.get("text") or "").strip() \
                        or not str(appeal.get("reasoning") or "").strip():
                    problems.append(
                        f"scenario {i}, appeal {j} needs a non-empty 'text' and "
                        f"'reasoning', like {{'text': '...', 'reasoning': '...'}}"
                    )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
