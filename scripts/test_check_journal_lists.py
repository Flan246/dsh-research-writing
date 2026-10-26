import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("check-journal-lists.py")
SPEC = importlib.util.spec_from_file_location("check_journal_lists", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
check_source = MODULE.check_source


def make_source(**kw):
    base = {"system": "CSSCI", "url": "https://example.com/", "current_version": "2025-2026"}
    base.update(kw)
    return base


class CheckSourceTest(unittest.TestCase):
    def test_unchanged_when_current_version_in_page(self):
        src = make_source()
        r = check_source(src, fetcher=lambda url: "CSSCI（2025-2026）来源期刊目录已发布")
        self.assertEqual(r["status"], "unchanged")

    def test_maybe_updated_when_current_version_missing_and_newer_year_present(self):
        src = make_source()
        r = check_source(src, fetcher=lambda url: "CSSCI（2027-2028）来源期刊目录已发布")
        self.assertEqual(r["status"], "maybe_updated")
        self.assertIn("2027-2028", r["detail"])

    def test_unknown_when_no_version_signals(self):
        src = make_source()
        r = check_source(src, fetcher=lambda url: "<html>页面改版，全是导航</html>")
        self.assertEqual(r["status"], "unknown")

    def test_unknown_on_fetch_failure(self):
        src = make_source()
        def boom(url):
            raise OSError("timeout")
        r = check_source(src, fetcher=boom)
        self.assertEqual(r["status"], "unknown")
        self.assertIn("timeout", r["detail"])

    def test_older_year_only_still_unchanged_when_current_present(self):
        src = make_source()
        r = check_source(src, fetcher=lambda url: "历史：2023-2024；现行：2025-2026")
        self.assertEqual(r["status"], "unchanged")


if __name__ == "__main__":
    unittest.main()
