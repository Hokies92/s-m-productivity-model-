"""source/ is evidence and is never modified (FILE_RULES.md section 2; canonical/FOUNDATION.md 1.1).

Fails if any file in source/ is changed, removed or added relative to tests/source.sha256.

© 2000–2026 Growth Enablement. All rights reserved.
"""
import hashlib
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_source_unchanged():
    expected = {}
    for line in (ROOT / "tests" / "source.sha256").read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        expected[name.strip()] = digest
    actual = {f"source/{p.name}": hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted((ROOT / "source").iterdir()) if p.is_file()}
    assert actual == expected, f"source/ differs from tests/source.sha256: {set(actual.items()) ^ set(expected.items())}"
