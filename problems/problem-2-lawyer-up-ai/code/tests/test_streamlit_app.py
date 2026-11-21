from pathlib import Path
import unittest

try:
    from streamlit.testing.v1 import AppTest
except ImportError:
    AppTest = None


APP = str(Path(__file__).resolve().parents[1] / "streamlit_app.py")


@unittest.skipIf(AppTest is None, "Install Streamlit to run UI tests")
class StreamlitAppTests(unittest.TestCase):
    def test_sample_populates_an_answer_and_a_source(self):
        app = AppTest.from_file(APP).run()
        self.assertFalse(app.exception)
        app.button(key="sample_0").click().run()
        self.assertFalse(app.exception)
        self.assertTrue(any("National Legal Services Authority" in item.value for item in app.text))
        self.assertEqual(len(app.get("link_button")), 2)

    def test_blank_question_shows_validation(self):
        app = AppTest.from_file(APP).run()
        next(button for button in app.button if button.label == "Research").click().run()
        self.assertFalse(app.exception)
        self.assertIn("Enter a question", app.warning[0].value)
