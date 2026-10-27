"""The blank as-is workbook passes the rubric gate (canonical/FOUNDATION.md section 7, requirement 1.1).

Builds the workbook from tools/build_asis_modern.py into a temp directory and runs the gate
criteria of tools/rubric.py against it. Skipped when LibreOffice is not installed.
"""
import json
import pathlib
import shutil
import sys
import tempfile

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_asis_modern as builder  # noqa: E402
import rubric  # noqa: E402

pytestmark = pytest.mark.skipif(shutil.which("soffice") is None, reason="LibreOffice not installed")


@pytest.fixture(scope="module")
def results():
    with tempfile.TemporaryDirectory() as td:
        out = pathlib.Path(td) / "model.xlsx"
        builder.main(out)
        res = rubric.run(out, out.with_suffix(".manifest.json"), None)
    return {r.cid: r for r in res}


def test_gate_passes(results):
    failing = [f"{cid}: {results[cid].measured}" for cid in ("G1", "G2", "G3", "G4") if results[cid].score != 2]
    assert not failing, "\n".join(failing)


def test_blank_workbook_has_no_errors(results):
    assert results["B4"].score == 2, results["B4"].measured


def test_automatic_criteria_do_not_regress(results):
    """The score at acceptance. Lowering any automatic criterion fails the build."""
    accepted = json.loads((ROOT / "workbook" / "Sales_Capacity_Model.score.json").read_text())
    accepted = {r["cid"]: r["score"] for r in accepted if r["method"] == "AUTO" and r["score"] is not None}
    regressions = [f"{cid}: {accepted[cid]} -> {results[cid].score}" for cid in accepted
                   if cid in results and results[cid].score is not None and results[cid].score < accepted[cid]]
    assert not regressions, "\n".join(regressions)
