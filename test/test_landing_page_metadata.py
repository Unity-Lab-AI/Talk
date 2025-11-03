"""Smoke tests for validating the landing page metadata used in pull requests."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import unittest


class _HeadStructureParser(HTMLParser):
    """Minimal HTML parser that records metadata inside the document head."""

    def __init__(self) -> None:
        super().__init__()
        self._in_head = False
        self._in_title = False
        self._in_noscript = False
        self._current_title: list[str] = []
        self.titles: list[str] = []
        self.meta_tags: list[dict[str, str]] = []
        self.scripts: list[dict[str, str]] = []
        self.noscript_styles: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {name: value or "" for name, value in attrs}
        if tag == "head":
            self._in_head = True
        elif tag == "title" and self._in_head:
            self._in_title = True
            self._current_title.clear()

        if self._in_head:
            if tag == "meta":
                self.meta_tags.append(attr_map)
            elif tag == "script":
                self.scripts.append(attr_map)
            elif tag == "noscript":
                self._in_noscript = True

        if self._in_noscript and tag == "link" and attr_map.get("rel") == "stylesheet":
            self.noscript_styles.append(attr_map)

    def handle_endtag(self, tag: str) -> None:
        if tag == "head":
            self._in_head = False
        elif tag == "title" and self._in_title:
            title = "".join(self._current_title).strip()
            if title:
                self.titles.append(title)
            self._in_title = False
        elif tag == "noscript" and self._in_noscript:
            self._in_noscript = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._current_title.append(data)


class LandingPageHeadTests(unittest.TestCase):
    """Validates the metadata embedded in ``index.html``."""

    @classmethod
    def setUpClass(cls) -> None:  # noqa: D401 - required by unittest
        """Load and parse the landing page once for the entire suite."""

        cls.index_html = Path("index.html").read_text(encoding="utf-8")
        parser = _HeadStructureParser()
        parser.feed(cls.index_html)
        cls.parser = parser

    def test_document_title_mentions_unity_voice_lab(self) -> None:
        """The page title should advertise the Unity Voice Lab system check."""

        self.assertGreater(len(self.parser.titles), 0, "No <title> element was parsed from the head.")
        self.assertTrue(
            any("Unity Voice Lab" in title for title in self.parser.titles),
            f"Expected 'Unity Voice Lab' in titles, found {self.parser.titles}",
        )

    def test_viewport_meta_is_present(self) -> None:
        """Mobile viewport metadata keeps the layout responsive."""

        viewport_metas = [tag for tag in self.parser.meta_tags if tag.get("name") == "viewport"]
        self.assertEqual(len(viewport_metas), 1, "The responsive viewport <meta> tag is missing or duplicated.")
        self.assertIn("width=device-width", viewport_metas[0].get("content", ""))

    def test_required_scripts_are_loaded_in_head(self) -> None:
        """Critical JavaScript bundles must be referenced before the body."""

        script_sources = {tag.get("src", "") for tag in self.parser.scripts}
        self.assertIn("landing.js?v=20240606", script_sources)
        self.assertIn("AI/app.js", script_sources)

    def test_noscript_stylesheet_fallbacks_are_available(self) -> None:
        """Users without JavaScript still need usable styling."""

        self.assertGreaterEqual(
            len(self.parser.noscript_styles),
            2,
            "Expected the <noscript> block to include at least two stylesheet fallbacks.",
        )

    def test_body_has_accessibility_state(self) -> None:
        """The body element should advertise the landing state for assistive tech."""

        self.assertRegex(
            self.index_html,
            r"<body[^>]*data-app-state=\"landing\"",
            "The landing body state attribute is missing.",
        )


if __name__ == "__main__":  # pragma: no cover - convenience for local runs
    unittest.main(verbosity=2)
