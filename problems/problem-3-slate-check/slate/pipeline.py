from .schema import FIELDS, LABELS, validate, check
from .scoring import score


def analyze(lines, scripts, size, threshold, ask):
    if not lines:
        lines = ask("Write natural two-sentence US vertical microdrama pitches for 1–2 minute episodes. "
                    "Use your default instincts without deliberately balancing tropes. Return {lines:[strings]}.",
                    {"count": size})["lines"]
        check(len(lines) == size and all(isinstance(s, str) and s.strip() for s in lines), "Invalid generated slate")
    rows = []
    for start in range(0, len(lines), 5):
        batch = lines[start:start + 5]
        items = ask("Return {rows:[objects]} in input order. Extract the categorical fields and city, hero_job, "
                    "villain, secret (six words maximum each), evidence (short verbatim phrase supporting twist), "
                    "doubt (a brief specific uncertainty or empty string). Use unknown for absent or ambiguous "
                    "information. City takes precedence over venue for setting_group. Use the final beat for cliffhanger.",
                    {"lines": batch, "labels": LABELS})["rows"]
        check(len(items) == len(batch), "Annotation count mismatch")
        for line, item in zip(batch, items):
            row = dict(item, number=len(rows) + 1, logline=line)
            validate(row)
            rows.append(row)
    stats = score(rows, threshold)
    flags, eligible = stats[1], stats[-1]
    fixes = {}
    for number in eligible[:5]:
        row = rows[number - 1]
        options = {f: sorted(flags[f]) for f in FIELDS if row[f] in flags[f]}
        variants = ask("Return {fixes:[{field,changed_to,new_logline,why_fresh}]}. Write three distinct alternatives. "
                       "Each changes exactly one eligible field to a known unflagged value, keeping every other field, "
                       "the premise, tone and stakes. why_fresh describes only that difference in <=15 words.",
                       {"row": row, "forbidden_by_eligible_field": options, "labels": LABELS})["fixes"]
        check(len(variants) == 3 and len({v["new_logline"] for v in variants}) == 3, "Expected three distinct rewrites")
        for v in variants:
            f, value = v["field"], v["changed_to"]
            check(f in options and value.strip() and value.casefold() not in
                  {s.casefold() for s in [*options[f], "unknown"]}, "Replacement is ineligible")
            check(f == "city" or value in LABELS[f], "Invalid replacement label")
            check(v["new_logline"].strip() and 1 <= len(v["why_fresh"].split()) <= 15, "Invalid rewrite")
        fixes[number] = variants
    exposition = {}
    for name, script in scripts.items():
        candidates = [s.strip() for s in script.splitlines() if len(s.split()) > 30]
        quotes = ask("Return {quotes:[strings]}. Select up to three exact lines with over 30 spoken words "
                     "explaining rules, processes, law or backstory instead of creating conflict. Exclude speaker "
                     "labels and stage directions when counting spoken words.", candidates)["quotes"] if candidates else []
        check(len(quotes) <= 3 and all(q in candidates for q in quotes), "Unsupported exposition quote")
        exposition[name] = quotes
    return rows, stats, fixes, exposition
