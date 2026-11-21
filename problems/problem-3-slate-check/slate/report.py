import csv
import io
from .schema import COLUMNS


def table(header, rows):
    def line(values):
        return "| " + " | ".join(str(x).replace("|", r"\|").replace("\n", " ") for x in values) + " |"
    return "\n".join([line(header), line(["---"] * len(header)), *(line(r) for r in rows)])


def render(rows, stats, fixes, exposition):
    counts, flags, modes, pair, hits, eligible = stats
    out = ["## 1. Extraction table", table(COLUMNS, ([r[k] for k in COLUMNS] for r in rows)), "## 2. Distributions"]
    for f, values in counts.items():
        known = len(rows) - values["unknown"]
        data = [(k, n, f"{n/known:.1%}", "FLAG" if k in flags[f] else "") for k, n in values.most_common() if k != "unknown"]
        out.extend([f"### {f} ({known} known)", table(["Value","Count","Share","Mark"], [*data, ("unknown",values["unknown"],"excluded","")])])
    out.extend(["## 3. Sameness Score", f"Modal pair: {pair[0] or 'unavailable'} × {pair[1] or 'unavailable'}. "
                f"Matching rows: {', '.join(map(str, hits)) or 'none'}. **{len(hits)}/{len(rows)} = {len(hits)/len(rows):.1%}**."])
    for f in ("twist_type", "hero_role_group"):
        if len(modes[f]) > 1:
            out.append(f"Tied {f}: {', '.join(sorted(modes[f]))}. Alphabetical order breaks the tie.")
    out.append("## 4. Exposition check")
    if not exposition:
        out.append("Not applicable, loglines only.")
    for name, quotes in exposition.items():
        out.extend([f"### {name}", "\n".join("- " + q for q in quotes) or "No qualifying lines."])
    out.append("## 5. Fix suggestions")
    for number, variants in fixes.items():
        keys = ("field", "changed_to", "new_logline", "why_fresh")
        out.extend([f"### Logline {number}", table(keys, ([v[k] for k in keys] for v in variants))])
    if not fixes:
        out.append("No flagged pitches.")
    if eligible[5:]:
        out.append("Skipped loglines: " + ", ".join(map(str, eligible[5:])))
    doubts = [f"- #{r['number']} {r['doubt']}" for r in rows if r.get("doubt")]
    out.extend(["## 6. Self-check", "\n".join(doubts[:5]) or "No uncertain extractions reported.",
                "- A small slate can cross the threshold after one edit.\n- A shared trope can serve different emotional conflicts."
                "\n- Missing cities inflate shares among known cities.", "## 7. CSV"])
    buffer = io.StringIO()
    w = csv.DictWriter(buffer, COLUMNS, extrasaction="ignore", lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return "\n\n".join(out) + "\n\n```csv\n" + buffer.getvalue() + "```\n"
