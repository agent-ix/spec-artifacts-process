"""Rewrite every `data_schema.digest` in manifest.yaml from the shipped bytes.

FR-010: each declared artifact type binds its emitted JSON Schema by path and
digest. This script recomputes the digests from the file each `data_schema.schema`
names, and rewrites **only** those values.

The rewrite is textual on purpose. A YAML round-trip would reformat the whole
file and drop every comment, and this manifest's comments carry the reasoning
behind vocabularies the whole ecosystem validates against — losing them to a
digest refresh would be the worst kind of silent damage.
"""

from __future__ import annotations

import hashlib
import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
MODULE_ROOT = REPO_ROOT / "spec_artifacts_process"
MANIFEST = MODULE_ROOT / "manifest.yaml"

# `data_schema:` followed by a `schema:` line and a `digest:` line, in that order
# and at one indentation. Anything else is not the reference form this module
# writes, and is left alone rather than guessed at.
ENTRY = re.compile(
    r"(?P<head>^(?P<indent>[ ]+)data_schema:\n"
    r"(?P=indent)  schema: (?P<schema>\S+)\n"
    r"(?P=indent)  digest: )(?P<digest>sha256:[0-9a-f]{64})$",
    re.MULTILINE,
)


def digest_of(path: pathlib.Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def rewrite(text: str) -> tuple[str, list[str]]:
    changed: list[str] = []

    def replace(match: re.Match[str]) -> str:
        schema = match.group("schema")
        path = MODULE_ROOT / schema
        if not path.is_file():
            raise SystemExit(
                f"manifest references {schema}, which does not exist at {path}"
            )
        current = digest_of(path)
        if current != match.group("digest"):
            changed.append(schema)
        return f"{match.group('head')}{current}"

    return ENTRY.sub(replace, text), changed


def main() -> int:
    original = MANIFEST.read_text()
    updated, changed = rewrite(original)
    if updated == original:
        print("manifest digests are up to date")
        return 0
    MANIFEST.write_text(updated)
    for schema in changed:
        print(f"rewrote digest for {schema}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
