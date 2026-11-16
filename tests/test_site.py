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

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        for attribute in ("href", "src"):
            value = attributes.get(attribute, "")
            parsed = urlparse(value)
            if value and not parsed.scheme and not value.startswith(("#", "data:")):
                self.local_assets.append(unquote(value.split("?", 1)[0]))
        if tag == "img" and "alt" not in attributes:
            self.images_without_alt.append(attributes.get("src", "(unnamed image)"))


class StaticSiteTests(unittest.TestCase):
    """Guard the entry page against missing assets and basic accessibility regressions."""

    def setUp(self):
        self.index_path = ROOT / "index.html"
        self.parser = AssetParser()
        self.parser.feed(self.index_path.read_text(encoding="utf-8"))

    def test_entry_point_exists(self):
        self.assertTrue(self.index_path.is_file())

    def test_local_references_resolve(self):
        missing = [
            path for path in self.parser.local_assets
            if not (ROOT / path.lstrip("/")).exists()
        ]
        self.assertEqual(missing, [], f"Missing local assets: {missing}")

    def test_all_images_have_alt_text(self):
        self.assertEqual(self.parser.images_without_alt, [])

    def test_document_has_language_and_primary_landmarks(self):
        html = self.index_path.read_text(encoding="utf-8")
        self.assertIn('<html lang="en">', html)
        self.assertIn('<main id="main">', html)
        self.assertIn('href="#main"', html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
