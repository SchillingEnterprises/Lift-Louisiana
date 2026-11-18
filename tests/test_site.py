"""Dependency-free checks for the published static website."""

from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]


class AssetParser(HTMLParser):
    """Collect local assets, links, and image accessibility attributes."""

    def __init__(self):
        super().__init__()
        self.local_assets = []
        self.images_without_alt = []
        self.external_blank_links = []

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        for attribute in ("href", "src"):
            value = attributes.get(attribute, "")
            parsed = urlparse(value)
            if value and not parsed.scheme and not value.startswith(("#", "data:")):
                self.local_assets.append(unquote(value.split("?", 1)[0]))
        if tag == "img" and "alt" not in attributes:
            self.images_without_alt.append(attributes.get("src", "(unnamed image)"))
        if tag == "a" and attributes.get("target", "").lower() == "_blank":
            self.external_blank_links.append(attributes)


class StaticSiteTests(unittest.TestCase):
    """Guard the entry page against missing assets and basic accessibility regressions."""

    def setUp(self):
        self.index_path = ROOT / "index.html"
        self.parser = AssetParser()
        self.parser.feed(self.index_path.read_text(encoding="utf-8"))

    def test_entry_point_exists(self):
        self.assertTrue(self.index_path.is_file())
        self.assertTrue((ROOT / "404.html").is_file())
        self.assertTrue((ROOT / "robots.txt").is_file())

    def test_local_references_resolve(self):
        missing = [
            path for path in self.parser.local_assets
            if not (ROOT / path.lstrip("/")).exists()
        ]
        self.assertEqual(missing, [], f"Missing local assets: {missing}")

    def test_stylesheet_local_asset_references_resolve(self):
        import re

        missing = []
        stylesheets = sorted((ROOT / "src").rglob("*.css"))
        self.assertTrue(stylesheets, "Expected at least one project stylesheet.")

        for stylesheet in stylesheets:
            source = stylesheet.read_text(encoding="utf-8")
            for reference in re.findall(r"url\(\s*(['"]?)(.*?)\1\s*\)", source, re.IGNORECASE):
                value = reference[1].strip()
                parsed = urlparse(value)
                if not value or parsed.scheme or value.startswith(("#", "//")):
                    continue
                target = (stylesheet.parent / unquote(parsed.path)).resolve()
                if not target.is_file():
                    missing.append(
                        f"{stylesheet.relative_to(ROOT)} -> {value}"
                    )

        self.assertEqual(
            missing,
            [],
            f"Missing local stylesheet assets: {missing}",
        )

    def test_mobile_navigation_has_accessible_control_relationship(self):
        html = self.index_path.read_text(encoding="utf-8")
        self.assertIn('aria-controls="primary-nav"', html)
        self.assertIn('aria-expanded="false"', html)
        self.assertIn('id="primary-nav"', html)
        self.assertIn('class="sr-only">Open navigation</span>', html)

    def test_mobile_navigation_supports_keyboard_dismissal_and_label_updates(self):
        script = (ROOT / "src" / "js" / "site.js").read_text(encoding="utf-8")
        self.assertIn('event.key === "Escape"', script)
        self.assertIn('buttonLabel.textContent = "Close navigation"', script)
        self.assertIn('buttonLabel.textContent = "Open navigation"', script)
        self.assertIn("restoreFocus: true", script)

    def test_all_images_have_alt_text(self):
        self.assertEqual(self.parser.images_without_alt, [])

    def test_external_new_tab_links_prevent_opener_access(self):
        failures = []
        for link in self.parser.external_blank_links:
            rel = set(link.get("rel", "").lower().split())
            if not {"noopener", "noreferrer"}.issubset(rel):
                failures.append(link.get("href", "(missing href)"))
        self.assertEqual(
            failures,
            [],
            f"External links opening new tabs need rel=noopener noreferrer: {failures}",
        )

    def test_branded_404_has_accessible_landmarks_and_home_links(self):
        page = (ROOT / "404.html").read_text(encoding="utf-8")
        self.assertIn('<html lang="en">', page)
        self.assertIn('<main id="main">', page)
        self.assertIn('href="./index.html"', page)
        self.assertIn("Page not found", page)

    def test_document_has_language_and_primary_landmarks(self):
        html = self.index_path.read_text(encoding="utf-8")
        self.assertIn('<html lang="en">', html)
        self.assertIn('<main id="main">', html)
        self.assertIn('href="#main"', html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
