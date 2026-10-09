#!/usr/bin/env python3
"""Look up author profiles in Open Library and print a Markdown report."""

from __future__ import annotations

import html
import json
import re
import sys
import time
import unicodedata
from html.parser import HTMLParser
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


AUTHORS = (
    "Fernando Aramburu",
    "Isaac Asimov",
    "Agustina María Bazterrica",
    "Roberto Bolaño",
    "Ray Bradbury",
    "Pierce Brown",
    "Liu Cixin",
    "Blake Crouch",
    "Joan Didion",
    "Matt Dinniman",
    "Elena Ferrante",
    "Jacqueline Harpman",
    "Frank Herbert",
    "Kazuo Ishiguro",
    "Hilary Mantel",
    "Cormac McCarthy",
    "Haruki Murakami",
    "Gabriel García Márquez",
    "Brandon Sanderson",
    "Andy Weir",
)

# Open Library stores Liu Cixin under his Chinese name, so pin the supplied record.
AUTHOR_ID_OVERRIDES = {"Liu Cixin": "OL7044246A"}

API_ROOT = "https://openlibrary.org"
USER_AGENT = "OpenLibraryAuthorLookup/1.0 (one-time personal library lookup)"
REQUEST_TIMEOUT_SECONDS = 10
MIN_REQUEST_INTERVAL_SECONDS = 1.0
MAX_RETRIES = 3

_response_cache: dict[str, Any] = {}
_last_request_at = 0.0


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def normalize_name(value: str) -> str:
    """Normalize Unicode and whitespace, while retaining accents and punctuation."""
    return " ".join(unicodedata.normalize("NFC", value).casefold().split())


def plain_text(value: Any) -> str:
    if isinstance(value, dict):
        value = value.get("value", "")
    if not isinstance(value, str):
        return ""

    extractor = _TextExtractor()
    extractor.feed(html.unescape(value))
    text = " ".join(" ".join(extractor.parts).split())
    # Keep table output readable and prevent source text from adding Markdown cells.
    return text.replace("|", "\\|")


def _wait_for_rate_limit() -> None:
    global _last_request_at
    now = time.monotonic()
    delay = MIN_REQUEST_INTERVAL_SECONDS - (now - _last_request_at)
    if delay > 0:
        time.sleep(delay)
    _last_request_at = time.monotonic()


def fetch_json(url: str) -> Any:
    if url in _response_cache:
        return _response_cache[url]

    last_error: Exception | None = None
    for attempt in range(MAX_RETRIES):
        _wait_for_rate_limit()
        request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        try:
            with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
                data = json.load(response)
            _response_cache[url] = data
            return data
        except HTTPError as error:
            last_error = error
            if error.code != 429 and error.code < 500:
                raise
            retry_after = error.headers.get("Retry-After")
            pause = float(retry_after) if retry_after and retry_after.isdigit() else 2**attempt
        except (URLError, TimeoutError, json.JSONDecodeError) as error:
            last_error = error
            pause = 2**attempt

        if attempt + 1 < MAX_RETRIES:
            time.sleep(pause)

    assert last_error is not None
    raise last_error


def author_record(name: str) -> tuple[str, dict[str, Any] | None, str | None]:
    author_id = AUTHOR_ID_OVERRIDES.get(name)
    if author_id:
        record = fetch_json(f"{API_ROOT}/authors/{author_id}.json")
        return "Matched via supplied Open Library ID", record, author_id

    query = urlencode({"q": name, "limit": 100, "fields": "key,name"})
    search_url = f"{API_ROOT}/search/authors.json?{query}"
    search_result = fetch_json(search_url)
    exact_matches_by_key = {
        str(record.get("key", "")).rsplit("/", 1)[-1]: record
        for record in search_result.get("docs", [])
        if record.get("key")
        and normalize_name(str(record.get("name", ""))) == normalize_name(name)
    }
    exact_matches = list(exact_matches_by_key.values())

    if not exact_matches:
        return "Not found", None, None
    if len(exact_matches) != 1:
        candidate_ids = ", ".join(sorted(exact_matches_by_key))
        return f"Ambiguous exact-name match: {candidate_ids}", None, None

    author_id = str(exact_matches[0].get("key", "")).rsplit("/", 1)[-1]
    if not re.fullmatch(r"OL[0-9]+A", author_id):
        return "Invalid Open Library author key", None, None

    record = fetch_json(f"{API_ROOT}/authors/{author_id}.json")
    return "Matched", record, author_id


def photo_url(record: dict[str, Any]) -> str:
    photos = record.get("photos") or []
    photo_id = next((photo for photo in photos if isinstance(photo, int) and photo > 0), None)
    if photo_id is None:
        return ""
    return f"https://covers.openlibrary.org/a/id/{photo_id}-M.jpg?default=false"


def profile_url(author_id: str | None) -> str:
    return f"{API_ROOT}/authors/{author_id}" if author_id else ""


def markdown_link(label: str, url: str) -> str:
    if not url:
        return ""
    safe_url = url.replace("(", "%28").replace(")", "%29").replace(" ", "%20")
    return f"[{label}]({safe_url})"


def markdown_cell(value: str) -> str:
    return value.replace("\n", " ").replace("\r", " ").strip()


def lookup(name: str) -> dict[str, str]:
    try:
        status, record, author_id = author_record(name)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, ValueError) as error:
        return {"name": name, "status": f"Error: {error}", "id": "", "dates": "", "bio": "", "photo": "", "photo_url": "", "profile": ""}

    if record is None or author_id is None:
        return {"name": name, "status": status, "id": "", "dates": "", "bio": "", "photo": "", "photo_url": "", "profile": ""}

    born = plain_text(record.get("birth_date"))
    died = plain_text(record.get("death_date"))
    dates = " — ".join(part for part in (born, died) if part)
    image = photo_url(record)
    return {
        "name": name,
        "status": status,
        "id": author_id,
        "dates": dates,
        "bio": plain_text(record.get("bio")),
        "photo": "Yes" if image else "No",
        "photo_url": markdown_link("Photo", image),
        "profile": markdown_link("Open Library", profile_url(author_id)),
    }


def main() -> int:
    rows = [lookup(name) for name in AUTHORS]
    headers = ("Author", "Lookup", "OL ID", "Born — died", "Biography", "Photo?", "Photo URL", "Profile")
    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        values = (
            row["name"], row["status"], row["id"], row["dates"], row["bio"],
            row["photo"], row["photo_url"], row["profile"],
        )
        print("| " + " | ".join(markdown_cell(value) for value in values) + " |")

    return 1 if any(row["status"].startswith("Error:") for row in rows) else 0


if __name__ == "__main__":
    sys.exit(main())
