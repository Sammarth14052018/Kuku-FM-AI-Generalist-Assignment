import argparse
import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

from .pipeline import analyze
from .provider import ask
from .report import render

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def replay(prompt, data):
    saved = json.loads((EXAMPLES / "annotations.json").read_text())
    if "lines" in data:
        by_line = {r["logline"]: r for r in saved["rows"]}
        return {"rows": [by_line[line] for line in data["lines"]]}
    return {"fixes": saved["fixes"][str(data["row"]["number"])]}


def main():
    p = argparse.ArgumentParser(description="Audit a microdrama slate before commissioning.")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--demo", action="store_true", help="Run the original sample with saved AI annotations")
    g.add_argument("--input", type=Path, help="UTF-8 text with one pitch per line")
    p.add_argument("--script", type=Path, action="append", default=[])
    p.add_argument("--output", type=Path)
    p.add_argument("--threshold", default="0.30")
    p.add_argument("--slate-size", type=int, default=20)
    a = p.parse_args()
    try:
        t = Decimal(a.threshold)
        if not t.is_finite() or not 0 <= t <= 1 or a.slate_size < 1:
            p.error("Use a threshold in [0,1] and a positive slate size.")
        if a.demo and (a.script or t != Decimal(".30")):
            p.error("The recorded demo uses the default threshold and loglines only.")
        path = EXAMPLES / "slate.txt" if a.demo else a.input
        lines = [s for s in path.read_text(encoding="utf-8").splitlines() if s.strip()] if path else []
        scripts = {str(f): f.read_text(encoding="utf-8") for f in a.script}
        report = render(*analyze(lines, scripts, a.slate_size, t, replay if a.demo else ask))
        if a.output:
            a.output.write_text(report, encoding="utf-8")
        else:
            sys.stdout.write(report)
    except (ValueError, InvalidOperation, OSError, KeyError, TypeError, IndexError) as exc:
        p.exit(1, f"Analysis failed: {exc}\n")


if __name__ == "__main__":
    main()
