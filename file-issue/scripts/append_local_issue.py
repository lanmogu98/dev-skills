#!/usr/bin/env python3
"""Append a new issue row to a local ISSUES.md Active table.

Handles the deterministic mechanics the file-issue skill would otherwise
re-derive on every invocation: parsing the prefix declaration in the
footer, choosing the next never-before-used ID for a given prefix, and
appending a correctly-formatted row.

The next ID is a monotonic high-water mark — the larger of a full-file
scan (Active + Done) and a persisted ``Next-ID`` footer watermark — so a
completed issue that moves to the Done table, or is later pruned from it,
never has its ID handed out again (issue #9).

Multi-prefix *selection* (choosing which prefix fits an issue's subject
area) stays an LLM judgment call — pass the chosen prefix via --prefix.

Usage:
    append_local_issue.py <issues_md> --prefix P --title T --priority p1|p2|p3
                          [--status Pending] [--assigned -]
                          [--dry-run]

Exits non-zero with a clear error if:
  - ISSUES.md has no prefix declaration and --prefix doesn't match the
    backward-compat fallback 'T'
  - The chosen prefix is not declared in a multi-prefix project
  - The Active table cannot be located
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PREFIX_SINGLE_RE = re.compile(r"^Prefix:\s*`([A-Za-z][A-Za-z0-9_-]*)`", re.MULTILINE)
PREFIX_MULTI_RE = re.compile(r"^Prefixes:\s*(.+)$", re.MULTILINE)
PREFIX_TOKEN_RE = re.compile(r"`([A-Za-z][A-Za-z0-9_-]*)`")
ACTIVE_HEADER_RE = re.compile(r"^##\s+Active\s*$", re.MULTILINE)
ID_RE = re.compile(r"^\s*\|\s*([A-Za-z][A-Za-z0-9_-]*)-(\d+)\s*\|")
NEXT_ID_LINE_RE = re.compile(r"^Next-ID:")
NEXT_ID_TOKEN_RE = re.compile(r"`([A-Za-z][A-Za-z0-9_-]*)-(\d+)`")
STATUS_FLOW_RE = re.compile(r"^Status flow:")
PREFIX_DECL_LINE_RE = re.compile(r"^Prefix(?:es)?:")


def parse_declared_prefixes(content: str) -> tuple[str, list[str]]:
    """Return (mode, prefixes). mode is 'single', 'multi', or 'fallback'."""
    if m := PREFIX_SINGLE_RE.search(content):
        return "single", [m.group(1)]
    if m := PREFIX_MULTI_RE.search(content):
        tokens = PREFIX_TOKEN_RE.findall(m.group(1))
        if tokens:
            return "multi", tokens
    return "fallback", ["T"]


def find_active_table_range(lines: list[str]) -> tuple[int, int]:
    """Return (header_line_idx, insert_line_idx) for the Active table.

    insert_line_idx is where the new row should be inserted (after the last
    existing data row in the Active table, or after the header separator if
    empty).
    """
    header_idx = None
    for i, line in enumerate(lines):
        if ACTIVE_HEADER_RE.match(line):
            header_idx = i
            break
    if header_idx is None:
        raise SystemExit("error: could not find '## Active' section in ISSUES.md")

    # Find the table header (| ID | Priority | ...) after the section header.
    table_start = None
    for i in range(header_idx + 1, len(lines)):
        if lines[i].lstrip().startswith("|"):
            table_start = i
            break
        if lines[i].startswith("## "):  # next section before table found
            raise SystemExit("error: '## Active' section has no table")
    if table_start is None:
        raise SystemExit("error: '## Active' section has no table")

    # table_start is the header row; table_start+1 is the separator; data
    # rows begin at table_start+2 and continue while lines start with '|'.
    insert_idx = table_start + 2
    while insert_idx < len(lines) and lines[insert_idx].lstrip().startswith("|"):
        insert_idx += 1
    return header_idx, insert_idx


def max_id_for_prefix(lines: list[str], prefix: str) -> int:
    """Return the max numeric suffix for `prefix` across the ENTIRE file, or 0.

    Scanning the whole file (Active *and* Done tables) — not just Active — is
    what prevents ID reuse when a completed issue is moved to the Done table.
    See issue #9.
    """
    max_n = 0
    for line in lines:
        m = ID_RE.match(line)
        if m and m.group(1) == prefix:
            max_n = max(max_n, int(m.group(2)))
    return max_n


def parse_next_id_counters(lines: list[str]) -> tuple[int | None, dict[str, int]]:
    """Parse the footer ``Next-ID`` watermark line.

    Returns ``(line_idx, counters)`` where ``line_idx`` is the index of the
    ``Next-ID`` line (or ``None`` if the file has none yet) and ``counters``
    maps each prefix to its next-to-allocate number. Insertion order of the
    tokens is preserved so a rewrite doesn't reshuffle existing entries.
    """
    for i, line in enumerate(lines):
        if NEXT_ID_LINE_RE.match(line):
            counters: dict[str, int] = {}
            for pfx, num in NEXT_ID_TOKEN_RE.findall(line):
                counters[pfx] = int(num)
            return i, counters
    return None, {}


def render_next_id_line(counters: dict[str, int]) -> str:
    """Render the footer watermark line from a prefix→next-number map."""
    tokens = " · ".join(f"`{pfx}-{num:03d}`" for pfx, num in counters.items())
    return f"Next-ID: {tokens}\n"


def find_next_id_insert_index(lines: list[str]) -> int:
    """Choose where to insert a ``Next-ID`` line in a file that lacks one.

    Prefer just after the prefix declaration; else after the ``Status flow``
    line; else end of file — keeping the watermark inside the footer block.
    """
    prefix_decl = None
    status_flow = None
    for i, line in enumerate(lines):
        if PREFIX_DECL_LINE_RE.match(line):
            prefix_decl = i
        elif STATUS_FLOW_RE.match(line):
            status_flow = i
    if prefix_decl is not None:
        return prefix_decl + 1
    if status_flow is not None:
        return status_flow + 1
    return len(lines)


def format_row(issue_id: str, priority: str, title: str, status: str, assigned: str) -> str:
    return f"| {issue_id} | {priority} | {title} | {status} | {assigned} |\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("issues_md", type=Path, help="Path to the project's ISSUES.md")
    ap.add_argument("--prefix", required=True, help="Chosen prefix (e.g., T, SEC, CFG)")
    ap.add_argument("--title", required=True, help="Issue title (short imperative)")
    ap.add_argument("--priority", required=True, choices=["p1", "p2", "p3"])
    ap.add_argument("--status", default="Pending")
    ap.add_argument("--assigned", default="—")
    ap.add_argument("--dry-run", action="store_true", help="Print the new row and resulting file content without writing")
    args = ap.parse_args()

    if not args.issues_md.exists():
        print(f"error: {args.issues_md} does not exist", file=sys.stderr)
        return 2

    content = args.issues_md.read_text()
    mode, declared = parse_declared_prefixes(content)

    if args.prefix not in declared:
        if mode == "fallback" and args.prefix == "T":
            pass  # legacy file without declaration
        else:
            print(
                f"error: prefix '{args.prefix}' not declared in ISSUES.md "
                f"(mode={mode}, declared={declared})",
                file=sys.stderr,
            )
            return 3

    lines = content.splitlines(keepends=True)
    header_idx, insert_idx = find_active_table_range(lines)

    # Next ID is a monotonic high-water mark: the larger of the footer
    # watermark (survives Done-table cleanup) and a full-file scan (survives a
    # missing or stale watermark). Neither alone is sufficient — see issue #9.
    counter_idx, counters = parse_next_id_counters(lines)
    next_n = max(counters.get(args.prefix, 0), max_id_for_prefix(lines, args.prefix) + 1)
    issue_id = f"{args.prefix}-{next_n:03d}"
    row = format_row(issue_id, args.priority, args.title, args.status, args.assigned)

    # Advance and persist the watermark for this prefix.
    counters[args.prefix] = next_n + 1
    counter_line = render_next_id_line(counters)

    if args.dry_run:
        watermark_verb = "update" if counter_idx is not None else "add"
        print(f"would insert at line {insert_idx + 1}:")
        print(row, end="")
        print(f"would {watermark_verb} watermark: {counter_line}", end="")
        return 0

    # Apply the footer edit first: the watermark line always sits after the
    # Active table, so editing it in place leaves insert_idx valid. When the
    # line is newly inserted at/above insert_idx, correct insert_idx for it.
    if counter_idx is not None:
        lines[counter_idx] = counter_line
    else:
        ins = find_next_id_insert_index(lines)
        if ins > 0 and not lines[ins - 1].endswith("\n"):
            lines[ins - 1] = lines[ins - 1] + "\n"
        lines.insert(ins, counter_line)
        if ins <= insert_idx:
            insert_idx += 1

    lines.insert(insert_idx, row)
    args.issues_md.write_text("".join(lines))
    print(issue_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
