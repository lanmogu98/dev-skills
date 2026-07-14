#!/usr/bin/env python3
"""Regression tests for append_local_issue.py — issue #9 (ID reuse).

Standalone assert-based test (no pytest dependency, per repo convention: no
general test suite). Run directly:

    python3 file-issue/scripts/test_append_local_issue.py

The core regression: when a completed issue moves from the Active table to
the Done table (the template's documented status flow), the next-ID logic
must NOT re-hand-out the moved ID. It also must survive Done-table cleanup,
which is what the monotonic Next-ID footer watermark guarantees.
"""
from __future__ import annotations

import atexit
import importlib.util
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("append_local_issue.py")

# Temp dirs created during the run, swept on exit so the suite leaves nothing
# behind under $TMPDIR (each test invokes the script as a subprocess against a
# real file, so an in-scope `with TemporaryDirectory()` would delete it early).
_TMPDIRS: list[Path] = []


@atexit.register
def _cleanup_tmpdirs() -> None:
    for d in _TMPDIRS:
        shutil.rmtree(d, ignore_errors=True)


# --- fixtures ---------------------------------------------------------------

def make_issues(active_rows: list[str], done_rows: list[str], footer: list[str]) -> str:
    """Render an ISSUES.md string from row/footer parts."""
    active = "".join(r if r.endswith("\n") else r + "\n" for r in active_rows)
    done = "".join(r if r.endswith("\n") else r + "\n" for r in done_rows)
    footer_block = "".join(l if l.endswith("\n") else l + "\n" for l in footer)
    return (
        "# Issues\n\n"
        "> Active work items.\n\n"
        "## Active\n\n"
        "| ID | Priority | Item | Status | Assigned |\n"
        "|----|----------|------|--------|----------|\n"
        f"{active}"
        "\n## Done (recent)\n\n"
        "| ID | Item | Completed | Note |\n"
        "|----|------|-----------|------|\n"
        f"{done}"
        "\n---\n\n"
        f"{footer_block}"
    )


SINGLE_FOOTER = [
    "Status flow: `Pending` → `In Progress` → `Done`",
    "Prefix: `T`",
    "Priority: `p1` (this week) · `p2` (this quarter) · `p3` (later)",
    "*Details for complex items: `docs/ISSUE_DETAILS.md`*",
]

MULTI_FOOTER = [
    "Status flow: `Pending` → `In Progress` → `Done`",
    "Prefixes: `SEC` (security) · `CFG` (config)",
    "Priority: `p1` · `p2` · `p3`",
    "*Details for complex items: `docs/ISSUE_DETAILS.md`*",
]


def run_script(issues_path: Path, prefix: str, title: str = "x", priority: str = "p2") -> str:
    """Invoke the script; return its stdout (the allocated ID), asserting exit 0."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(issues_path),
         "--prefix", prefix, "--title", title, "--priority", priority],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, (
        f"expected exit 0, got {result.returncode}\nstderr: {result.stderr}"
    )
    return result.stdout.strip()


def write_tmp(content: str) -> Path:
    d = Path(tempfile.mkdtemp(prefix="issues_test_"))
    _TMPDIRS.append(d)
    p = d / "ISSUES.md"
    p.write_text(content)
    return p


# --- regression tests -------------------------------------------------------

def test_done_move_does_not_reuse_id():
    """THE bug (#9): a completed issue moved Active→Done must not free its ID.

    Setup mirrors the issue report: T-005 was the highest ID; it has been
    completed and moved to the Done table, so Active now tops out at T-004.
    The buggy version scanned only Active and re-emitted T-005 (a collision
    with the completed T-005). The fix scans the whole file → T-006.
    """
    content = make_issues(
        active_rows=[
            "| T-001 | p1 | first | Done | — |",
            "| T-002 | p2 | second | Pending | — |",
            "| T-003 | p2 | third | Pending | — |",
            "| T-004 | p3 | fourth | Pending | — |",
        ],
        done_rows=[
            "| T-005 | fifth (completed) | 2026-07-14 | — |",
        ],
        footer=SINGLE_FOOTER,  # legacy: no Next-ID watermark yet
    )
    p = write_tmp(content)
    got = run_script(p, "T")
    assert got != "T-005", "REGRESSION: reused the completed ID T-005"
    assert got == "T-006", f"expected T-006, got {got}"


def test_survives_done_cleanup_via_watermark():
    """After Done is pruned, the Next-ID watermark still blocks reuse.

    Active and Done are both empty, but the footer watermark records that
    T-006 is next (T-001..T-005 were allocated then cleaned). A pure
    full-file scan would fall back to T-001 (reuse!); the watermark forces
    T-006, then T-007.
    """
    footer = [
        "Status flow: `Pending` → `In Progress` → `Done`",
        "Prefix: `T`",
        "Next-ID: `T-006`",
        "Priority: `p1` · `p2` · `p3`",
        "*Details for complex items: `docs/ISSUE_DETAILS.md`*",
    ]
    content = make_issues(active_rows=[], done_rows=[], footer=footer)
    p = write_tmp(content)
    first = run_script(p, "T")
    assert first == "T-006", f"watermark not honored: expected T-006, got {first}"
    second = run_script(p, "T")
    assert second == "T-007", f"watermark not monotonic: expected T-007, got {second}"


def test_watermark_written_back_on_legacy_file():
    """A legacy file (no Next-ID line) is upgraded in place on first write."""
    content = make_issues(
        active_rows=["| T-002 | p2 | seed | Pending | — |"],
        done_rows=[],
        footer=SINGLE_FOOTER,
    )
    p = write_tmp(content)
    got = run_script(p, "T")
    assert got == "T-003", f"expected T-003, got {got}"
    text = p.read_text()
    assert "Next-ID:" in text, "watermark line was not written back"
    assert "`T-004`" in text, f"watermark not advanced to T-004:\n{text}"


def test_full_lifecycle_never_reuses():
    """Allocate → complete/move → clean → allocate again must not reuse."""
    content = make_issues(
        active_rows=["| T-001 | p1 | one | Pending | — |"],
        done_rows=[],
        footer=SINGLE_FOOTER,
    )
    p = write_tmp(content)
    a = run_script(p, "T")            # T-002
    b = run_script(p, "T")            # T-003
    assert (a, b) == ("T-002", "T-003"), (a, b)
    # Simulate: complete everything, then prune Done entirely, keeping only
    # the footer watermark the script maintained.
    lines = p.read_text().splitlines(keepends=True)
    kept = [l for l in lines if not l.lstrip().startswith("| T-")]
    p.write_text("".join(kept))
    c = run_script(p, "T")            # must be T-004, never T-001/002/003
    assert c == "T-004", f"reused an ID after cleanup: got {c}"


def test_multi_prefix_sequences_independent():
    """Multi-prefix mode keeps per-prefix sequences and multi-token watermark."""
    content = make_issues(
        active_rows=[
            "| SEC-001 | p1 | sec one | Pending | — |",
            "| CFG-001 | p2 | cfg one | Pending | — |",
            "| CFG-002 | p2 | cfg two | Pending | — |",
        ],
        done_rows=[],
        footer=MULTI_FOOTER,
    )
    p = write_tmp(content)
    assert run_script(p, "CFG") == "CFG-003"
    assert run_script(p, "SEC") == "SEC-002"
    text = p.read_text()
    assert "`CFG-004`" in text and "`SEC-003`" in text, (
        f"multi-prefix watermark wrong:\n{text}"
    )


def test_fallback_prefix_and_undeclared_rejected():
    """No declaration → 'T' fallback works; an undeclared prefix is rejected."""
    content = make_issues(
        active_rows=[],
        done_rows=[],
        footer=[
            "Status flow: `Pending` → `In Progress` → `Done`",
            "Priority: `p1` · `p2` · `p3`",
        ],
    )
    p = write_tmp(content)
    assert run_script(p, "T") == "T-001"
    # An undeclared, non-fallback prefix must be rejected (exit 3).
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(p),
         "--prefix", "SEC", "--title", "x", "--priority", "p2"],
        capture_output=True, text=True,
    )
    assert result.returncode == 3, f"expected exit 3, got {result.returncode}"


def test_unit_helpers():
    """Direct checks on the pure helpers (localize failures)."""
    spec = importlib.util.spec_from_file_location("ali", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # Full-file scan sees IDs in BOTH tables.
    lines = make_issues(
        active_rows=["| T-002 | p2 | a | Pending | — |"],
        done_rows=["| T-009 | done | 2026-01-01 | — |"],
        footer=SINGLE_FOOTER,
    ).splitlines(keepends=True)
    assert mod.max_id_for_prefix(lines, "T") == 9, "scan must include Done table"

    # Watermark parse/round-trip.
    idx, counters = mod.parse_next_id_counters(
        ["Next-ID: `T-006` · `SEC-002`\n"]
    )
    assert idx == 0 and counters == {"T": 6, "SEC": 2}, counters
    rendered = mod.render_next_id_line({"T": 7})
    assert rendered.strip() == "Next-ID: `T-007`", rendered


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {t.__name__}: {e}")
        except Exception as e:  # noqa: BLE001 - surface any error as a failure
            failed += 1
            print(f"ERROR {t.__name__}: {type(e).__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
