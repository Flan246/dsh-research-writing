import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

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


class MainExitCodeTest(unittest.TestCase):
    def run_main(self, statuses):
        results = [
            {"system": f"source-{index}", "status": status, "detail": "test"}
            for index, status in enumerate(statuses)
        ]
        sources = [
            {"system": result["system"], "url": "https://example.com/", "current_version": "2025"}
            for result in results
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "sources.json"
            path.write_text(json.dumps({"sources": sources}), encoding="utf-8")
            with mock.patch.object(MODULE.sys, "argv", ["check-journal-lists.py", str(path)]), \
                    mock.patch.object(MODULE, "check_source", side_effect=results), \
                    contextlib.redirect_stdout(io.StringIO()):
                return MODULE.main()

    def test_unchanged_and_unknown_returns_2(self):
        self.assertEqual(self.run_main(["unchanged", "unknown"]), 2)

    def test_maybe_updated_and_unknown_returns_1(self):
        self.assertEqual(self.run_main(["maybe_updated", "unknown"]), 1)

    def test_all_unchanged_returns_0(self):
        self.assertEqual(self.run_main(["unchanged", "unchanged"]), 0)

    def test_all_unknown_returns_2(self):
        self.assertEqual(self.run_main(["unknown", "unknown"]), 2)


if __name__ == "__main__":
    unittest.main()
