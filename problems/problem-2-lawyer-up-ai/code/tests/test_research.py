import unittest

from research import Answer, Research, Source, demo_answer


class ResearchTests(unittest.TestCase):
    def test_demo_cannot_present_arbitrary_text_as_live_guidance(self):
        answer = demo_answer("A new question")
        self.assertEqual(answer.status, "demo")
        self.assertEqual(answer.sources, ())

    def test_weak_retrieval_does_not_generate_an_answer(self):
        source = Source("Example", "A passage", score=0.2)
        engine = Research(lambda _: [source], lambda _: [], self.unexpected_generation)
        self.assertEqual(engine.answer("Question").status, "insufficient")

    def test_web_snippets_are_research_leads_only(self):
        lead = Source("Official resource", "Search snippet", url="https://nalsa.gov.in/")
        engine = Research(lambda _: [], lambda _: [lead], self.unexpected_generation)
        answer = engine.answer("Question")
        self.assertEqual(answer.status, "insufficient")
        self.assertEqual(answer.sources, (lead,))

    def test_indexed_evidence_is_returned_alongside_the_answer(self):
        strong = Source("Example act", "A passage", page=4, score=0.8)
        weak = Source("Unrelated act", "A weak match", score=0.1)
        engine = Research(lambda _: [strong, weak], lambda _: [], lambda prompt: (
            "Grounded answer [1]" if "A passage" in prompt and "A weak match" not in prompt else ""
        ))
        self.assertEqual(
            engine.answer("Question"),
            Answer("answered", "Grounded answer [1]", (strong,)),
        )

    def test_answer_requires_a_valid_source_reference(self):
        source = Source("Example act", "A passage", score=0.8)
        for draft in ("An uncited answer", "An invalid citation [2]", "INSUFFICIENT"):
            with self.subTest(draft=draft):
                engine = Research(lambda _: [source], lambda _: [], lambda _: draft)
                self.assertEqual(engine.answer("Question").status, "insufficient")

    @staticmethod
    def unexpected_generation(_):
        raise AssertionError("Generation must require indexed evidence")


if __name__ == "__main__":
    unittest.main()
