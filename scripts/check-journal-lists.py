#!/usr/bin/env python3
"""季度期刊名单核验：只查官方名单是否换版，不爬名单。

退出码：0=全部 unchanged；1=存在 maybe_updated（提醒主人）；2=全部 unknown。
用法：python scripts/check-journal-lists.py [path-to-journal-sources.json]
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

VERSION_RE = re.compile(r"20\d{2}(?:\s*[-–—]\s*20\d{2})?")


def fetch_url(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "journal-whitelist-check/0.1"})
    with urllib.request.urlopen(req, timeout=20) as resp:  # urllib 自动读 HTTPS_PROXY
        return resp.read().decode("utf-8", errors="replace")


def check_source(source: dict, fetcher=fetch_url) -> dict:
    """返回 {system, status, detail}；status ∈ unchanged/maybe_updated/unknown。"""
    system = source["system"]
    try:
        page = fetcher(source["url"])
    except Exception as exc:  # 网络失败一律 unknown，不误判
        return {"system": system, "status": "unknown", "detail": f"fetch failed: {exc}"}
    if source["current_version"] in page:
        return {"system": system, "status": "unchanged", "detail": f"page still mentions {source['current_version']}"}
    versions = sorted(set(VERSION_RE.findall(page)))
    if versions:
        return {"system": system, "status": "maybe_updated",
                "detail": f"current {source['current_version']} not found; page mentions {versions}"}
    return {"system": system, "status": "unknown", "detail": "no version signals on page (structure changed?)"}


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "data" / "journal-sources.json"
    sources = json.loads(path.read_text(encoding="utf-8"))["sources"]
    results = [check_source(s) for s in sources]
    for r in results:
        print(f"[{r['status']:>13}] {r['system']}: {r['detail']}")
    statuses = {r["status"] for r in results}
    if "maybe_updated" in statuses:
        return 1
    if statuses == {"unknown"}:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
