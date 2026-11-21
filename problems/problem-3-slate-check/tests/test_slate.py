import csv
import io
import unittest
from decimal import Decimal
from pathlib import Path

from slate.__main__ import EXAMPLES, replay
from slate.pipeline import analyze
from slate.report import render
from slate.schema import validate
from slate.scoring import score


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.lines = (EXAMPLES / "slate.txt").read_text().splitlines()
        self.result = analyze(self.lines, {}, 20, Decimal(".30"), replay)

    def test_sample(self):
        rows, stats, fixes, _ = self.result
        counts, flags, modes, pair, hits, order = stats
        self.assertEqual(hits, [1, 2, 3])
        self.assertEqual(counts["city"]["unknown"], 3)
        self.assertEqual(flags["city"], {"Seattle", "Chicago"})
        self.assertEqual(order, [1, 2, 3])
        self.assertEqual(sum(map(len, fixes.values())), 9)
        csv_text = render(*self.result).split("```csv\n")[1].split("```")[0]
        self.assertEqual([r["logline"] for r in csv.DictReader(io.StringIO(csv_text))], self.lines)

    def test_exact_boundary_and_ties(self):
        rows = self.result[0]
        stats = score(rows, Decimal(".5"))
        self.assertFalse(stats[1]["twist_type"])
        tied = score([rows[0], rows[-1]], Decimal(".5"))
        self.assertEqual(len(tied[2]["twist_type"]), 2)
        self.assertEqual(tied[3], ("betrayal_by_ally", "creative_artist"))

    def test_evidence_and_missing_labels(self):
        with self.assertRaises(ValueError):
            validate(dict(self.result[0][0], evidence="fabricated"))
        unknown = dict.fromkeys(self.result[0][0], "unknown")
        stats = score([unknown], Decimal("0"))
        self.assertEqual(stats[-1], [])
        self.assertEqual(stats[4], [])

    def test_generation_and_scripts(self):
        speech = " ".join(["backstory"] * 31)
        def model(prompt, data):
            if isinstance(data, list):
                return {"quotes": [speech]}
            if "count" in data:
                return {"lines": self.lines}
            return replay(prompt, data)
        result = analyze([], {"scene": speech}, 6, Decimal(".30"), model)
        self.assertEqual(result[-1]["scene"], [speech])


if __name__ == "__main__":
    unittest.main()
