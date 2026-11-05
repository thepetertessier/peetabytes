"""Run with: python -m unittest discover -s scripts"""

import unittest
from pathlib import Path

from send_to_buttondown import parse_post, prepare_body, separate_lists


class EmailFormattingTests(unittest.TestCase):
    def test_list_after_paragraph(self):
        for marker in ("-", "+", "*", "1."):
            body = f"Intro:\n{marker} First\n{marker} Second"
            self.assertEqual(separate_lists(body), body.replace("Intro:\n", "Intro:\n\n"))

    def test_preserves_other_blocks(self):
        for body in (
            "Intro:\n\n- One\n  - Nested\n- Two",
            "```md\nIntro:\n- literal\n```",
            "~~~~\nIntro:\n- literal\n~~~~",
            "Heading\n---\n\n* * *",
            "    Intro:\n    - code",
            "- One\n  continued\n- Two",
        ):
            self.assertEqual(separate_lists(body), body)

    def test_actual_post(self):
        post = Path(__file__).resolve().parents[1] / "_posts/2026-11-04-how-far-can-you-go.md"
        _, body = parse_post(post)
        prepared = prepare_body(body)
        self.assertIn("speed are:\n\n- **Abolish PRs.**", prepared)
        self.assertIn("https://blog.petertessier.com/assets/img/peter-steinberger-quote.png", prepared)
        self.assertEqual(prepare_body(prepared), prepared)


if __name__ == "__main__":
    unittest.main()
