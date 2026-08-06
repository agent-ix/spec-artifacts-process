#!/usr/bin/env python3
"""Run the FR-003 TestMatrix contract over every `spec/tests.md` in a corpus.

This is the harness behind `reports/2026-08-04-tests-md-sweep.md`. That run's
script was never committed, so the 171/177 figure could not be re-derived
without rebuilding it (agent-ix/spec-artifacts-process#12). It lives here now.

Read-only: it validates and reports, and never edits a document. The
normalization sweep it informs is user-gated by FR-003-CON-1.

Usage:

    python3 scripts/testmatrix_sweep.py --root ~/dev
    python3 scripts/testmatrix_sweep.py --root ~/dev --show-values Type

Requires a `quire` wheel exposing `validate_document` (quire-rs FR-032). It
validates through the real engine against this repo's `manifest.yaml`, so the
result is exactly what `quire validate` would say — not a reimplementation of
the contract that could drift from it.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import quire  # type: ignore[import-not-found]

ARCHETYPE = "TestMatrix"
MODULE = Path(__file__).resolve().parent.parent / "spec_artifacts_process"

SKIP_DIRS = {
    ".git",
    "node_modules",
    "target",
    "dist",
    "build",
    ".venv",
    "venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".next",
    "vendor",
    # Worktree checkouts are byte-copies of a repo already counted. Nested
    # ones matter most: `ecaz` alone carries 20 of them under `.worktrees/`
    # and `.claude/worktrees/`, so leaving them in multiplies that repo's
    # every diagnostic by 20 and makes one repo look like a corpus-wide trend.
    "worktrees",
    ".worktrees",
}

SUMMARY_HEADING = re.compile(r"^##\s+Test Case Summary\s*$", re.MULTILINE)
FR_COVERAGE_HEADING = re.compile(
    r"^##\s+Functional Requirement Coverage\s*$", re.MULTILINE
)
ID_COLUMN_TABLE = re.compile(r"^\|\s*(Test ID|TC ID|ID)\s*\|", re.MULTILINE)


def frontmatter_type(text: str) -> str | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    m = re.search(r"^type:\s*['\"]?([A-Za-z][A-Za-z0-9_-]*)", text[3:end], re.MULTILINE)
    return m.group(1) if m else None


def classify(text: str, errors: list[dict]) -> str:
    """Sort a failure into the three classes issue #12 asks to distinguish.

    * `missing-table`  — no Test Case Summary section at all. A different
      failure from a malformed one, and it wants a different remedy: the repo
      has to *author* a matrix, not fix one.
    * `renamable`      — no Test Case Summary heading, but an id-column table
      exists under some other heading. Candidate for a rename rather than
      authoring.
    * `malformed`      — the sections exist and the contract rejects their
      content. This is the class the normalization sweep addresses.
    """
    has_summary = bool(SUMMARY_HEADING.search(text))
    if not has_summary:
        return "renamable" if ID_COLUMN_TABLE.search(text) else "missing-table"
    return "malformed"


def reason_of(err: dict) -> str:
    """A stable cause label from the engine's diagnostic."""
    msg = err.get("message", "")
    if "is missing" in msg:
        m = re.search(r"required '([^']+)'", msg)
        return f"missing:{m.group(1)}" if m else "missing"
    for col in ("Type", "Priority", "Status", "Traces To", "Test ID"):
        if f"'{col}'" in msg or f"column '{col}'" in msg:
            return f"cell:{col}"
    if "columns" in msg:
        return "columns"
    if "id cell" in msg or "id_pattern" in msg:
        return "cell:Test ID"
    return err.get("reason", "other")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path.home() / "dev")
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument(
        "--show-values",
        metavar="COLUMN",
        default=None,
        help="print the distinct rejected values seen in COLUMN, with counts",
    )
    ap.add_argument(
        "--dedupe-worktrees",
        action="store_true",
        default=True,
        help="skip `worktrees/` and `<repo>-task<N>` checkouts (default)",
    )
    args = ap.parse_args()

    root = args.root.expanduser().resolve()
    module = str(MODULE)

    def real_repo(repo: str) -> bool:
        if not args.dedupe_worktrees:
            return True
        return not re.match(r"^.+-task\d+$", repo)

    docs, passing = [], []
    failures: list[dict] = []
    not_testmatrix = 0

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        if "tests.md" not in filenames or not dirpath.endswith("spec"):
            continue
        path = Path(dirpath) / "tests.md"
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        rel = path.relative_to(root)
        repo = rel.parts[0]
        if not real_repo(repo):
            continue
        if frontmatter_type(text) != ARCHETYPE:
            not_testmatrix += 1
            continue
        docs.append(repo)
        try:
            res = quire.validate_document(ARCHETYPE, module, text)
        except Exception as exc:
            print(f"skip {rel}: {exc}", file=sys.stderr)
            continue
        if res["is_valid"]:
            passing.append(repo)
            continue
        failures.append(
            {
                "repo": repo,
                "path": str(rel),
                "klass": classify(text, res["errors"]),
                "reasons": sorted({reason_of(e) for e in res["errors"]}),
                "errors": [e["message"] for e in res["errors"]],
            }
        )

    total = len(docs)
    print(
        f"TestMatrix documents : {total}   "
        f"(skipped {not_testmatrix} tests.md not typed TestMatrix)"
    )
    print(f"passing              : {len(passing)}  ({100 * len(passing) / total:.1f}%)")
    print(
        f"failing              : {len(failures)}  ({100 * len(failures) / total:.1f}%)"
    )

    print("\n── failure class (issue #12 work item 1) ──")
    by_class = Counter(f["klass"] for f in failures)
    for k, n in by_class.most_common():
        print(f"  {k:16} {n:4d}  {100 * n / total:5.1f}% of corpus")

    print("\n── cause (a document may have several) ──")
    causes: Counter[str] = Counter()
    cause_repos: defaultdict[str, set[str]] = defaultdict(set)
    for f in failures:
        for r in f["reasons"]:
            causes[r] += 1
            cause_repos[r].add(f["repo"])
    for c, n in causes.most_common():
        print(f"  {c:28} {n:4d} docs   {len(cause_repos[c]):4d} repos")

    if args.show_values:
        col = args.show_values
        print(f"\n── rejected `{col}` values ──")
        vals: Counter[str] = Counter()
        for f in failures:
            for msg in f["errors"]:
                m = re.search(rf"'{re.escape(col)}'.*?value '([^']*)'", msg)
                if m:
                    vals[m.group(1)] += 1
        for v, n in vals.most_common(40):
            print(f"  {n:5d}  {v!r}")

    if args.out:
        args.out.write_text(
            json.dumps(
                {"total": total, "passing": sorted(passing), "failures": failures},
                indent=1,
            )
        )
        print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
