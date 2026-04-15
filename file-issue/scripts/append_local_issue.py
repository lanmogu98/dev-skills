#!/usr/bin/env python3
"""Append a new issue row to a local ISSUES.md Active table.

Handles the deterministic mechanics the file-issue skill would otherwise
re-derive on every invocation: parsing the prefix declaration in the
footer, scanning Active rows for the highest existing ID with a given
prefix, and appending a correctly-formatted row.

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


def max_id_for_prefix(lines: list[str], prefix: str, header_idx: int, end_idx: int) -> int:
    """Return the max numeric suffix for `prefix` in the Active table, or 0."""
    max_n = 0
    for line in lines[header_idx:end_idx]:
        m = ID_RE.match(line)
        if m and m.group(1) == prefix:
            max_n = max(max_n, int(m.group(2)))
    return max_n


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
    next_n = max_id_for_prefix(lines, args.prefix, header_idx, insert_idx) + 1
    issue_id = f"{args.prefix}-{next_n:03d}"
    row = format_row(issue_id, args.priority, args.title, args.status, args.assigned)

    new_lines = lines[:insert_idx] + [row] + lines[insert_idx:]
    new_content = "".join(new_lines)

    if args.dry_run:
        print(f"would insert at line {insert_idx + 1}:")
        print(row, end="")
        return 0

    args.issues_md.write_text(new_content)
    print(issue_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
