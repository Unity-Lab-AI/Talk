"""Regression tests for validating the structure and scripts of Talk to Unity."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import unittest


class _DependencyParser(HTMLParser):
    """Collects dependency checklist items and status containers from the landing page."""

    def __init__(self) -> None:
        super().__init__()
        self.dependencies: list[dict[str, str]] = []
        self.status_regions: list[dict[str, str]] = []
        self._current_dependency: dict[str, str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {name: value or "" for name, value in attrs}
        class_attr = attr_map.get("class", "")

        if tag == "li" and "dependency-item" in class_attr:
            self.dependencies.append(attr_map)
            self._current_dependency = attr_map
        elif tag == "div" and attr_map.get("role") == "status":
            self.status_regions.append(attr_map)

        if tag == "span" and "dependency-status" in class_attr and self._current_dependency is not None:
            # Record that we saw a visible status element for the dependency
            self._current_dependency.setdefault("has_status_element", "true")

    def handle_endtag(self, tag: str) -> None:
        if tag == "li":
            self._current_dependency = None


class LandingPageDependencyTests(unittest.TestCase):
    """Ensures the dependency checklist is wired up with the required semantics."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.index_html = Path("index.html").read_text(encoding="utf-8")
        parser = _DependencyParser()
        parser.feed(cls.index_html)
        cls.parser = parser

    def test_expected_dependency_items_present(self) -> None:
        """The landing checklist should cover the four major readiness items."""

        dependency_ids = {item.get("data-dependency", "") for item in self.parser.dependencies}
        self.assertSetEqual(
            dependency_ids,
            {"secure-context", "speech-recognition", "speech-synthesis", "microphone"},
            "Unexpected dependency checklist items detected.",
        )

    def test_dependency_items_define_user_friendly_status(self) -> None:
        """Each checklist item needs both success and failure messaging."""

        for dependency in self.parser.dependencies:
            with self.subTest(dependency=dependency.get("data-dependency")):
                self.assertIn("data-pass-status", dependency)
                self.assertIn("data-fail-status", dependency)
                self.assertIn("has_status_element", dependency, "Missing visible status span for dependency.")

    def test_status_regions_are_accessible(self) -> None:
        """Status messaging should be exposed to assistive technologies."""

        status_roles = [region.get("role") for region in self.parser.status_regions]
        self.assertGreaterEqual(len(status_roles), 1, "No live status region detected in the layout.")


class LandingJavaScriptStructureTests(unittest.TestCase):
    """Validates key behaviors baked into ``landing.js``."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.source = Path("landing.js").read_text(encoding="utf-8")

    def test_dependency_checks_cover_required_fields(self) -> None:
        """The dependencyChecks array should enumerate the major readiness checks."""

        for identifier in ("secure-context", "speech-recognition", "speech-synthesis", "microphone"):
            self.assertIn(f"id: '{identifier}'", self.source)

    def test_bootstrap_sets_up_event_handlers(self) -> None:
        """Landing bootstrap should register DOM events for launch and recheck flows."""

        self.assertIn(
            "document.addEventListener('DOMContentLoaded', bootstrapLandingExperience);",
            self.source,
        )
        self.assertIn("launchButton?.addEventListener('click', handleLaunchButtonClick);", self.source)
        self.assertIn("recheckButton?.addEventListener('click', handleRecheckClick);", self.source)

    def test_launch_event_dispatch_includes_custom_event(self) -> None:
        """The landing page should dispatch a rich custom event for the app shell."""

        pattern = re.compile(r"CustomEvent\('[\w-]+:launch'", re.MULTILINE)
        self.assertRegex(self.source, pattern)

    def test_resolve_app_launch_url_targets_ai_bundle(self) -> None:
        """The launch URL resolver should always land on the AI bundle entry point."""

        self.assertIn("return new URL('./AI/index.html', base || window.location.href).toString();", self.source)


if __name__ == "__main__":  # pragma: no cover
    unittest.main(verbosity=2)
