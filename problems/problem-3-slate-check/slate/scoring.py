from collections import Counter
from .schema import FIELDS


def score(rows, threshold):
    counts, flags, modes = {}, {}, {}
    for field in FIELDS:
        counts[field] = Counter(r[field] for r in rows)
        known = {k: n for k, n in counts[field].items() if k != "unknown"}
        total = sum(known.values())
        flags[field] = {k for k, n in known.items() if n > threshold * total}
        modes[field] = {k for k, n in known.items() if n == max(known.values())}

    # Publish one reproducible modal pair on ties, showing every tied candidate.
    twist = min(modes["twist_type"], default=None)
    role = min(modes["hero_role_group"], default=None)
    hits = [r["number"] for r in rows if r["twist_type"] == twist and r["hero_role_group"] == role]
    priority = {r["number"]: sum(r[f] in flags[f] for f in FIELDS) for r in rows}
    eligible = sorted((n for n in priority if priority[n]), key=lambda n: (-priority[n], n))
    return counts, flags, modes, (twist, role), hits, eligible
