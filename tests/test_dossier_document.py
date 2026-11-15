"""The DossierDocument archetype and its fixtures (FR-018)."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
from conftest import (
    EXAMPLES_DIR,
    REPO_ROOT,
    SCHEMAS_DIR,
    SKELETONS_DIR,
    frontmatter,
    quire_validate,
)

FIXTURES = REPO_ROOT / "tests" / "fixtures" / "dossier"
VALID = FIXTURES / "valid"
INVALID = FIXTURES / "invalid"

# FR-018-AC-5: a member whose name contains one of these records where or when
# a document came from, which the commit that holds it already does.
FORBIDDEN_NAME_PARTS = ("digest", "hash", "sha", "revision", "provenance")


def validate(*paths: Path) -> subprocess.CompletedProcess:
    return quire_validate(*paths, scope=FIXTURES)


def messages(result: subprocess.CompletedProcess, path: Path) -> list[str]:
    """The diagnostics of one document with its path removed.

    Every line starts with the document path, and a fixture's file name can
    contain the field under test (`missing-version.md`), so a substring check on
    the whole line would hold whatever the diagnostic says.
    """
    prefix = f"{path}: "
    return [
        line[len(prefix) :]
        for line in result.stderr.splitlines()
        if line.startswith(prefix)
    ]


def fails_naming(path: Path, field: str) -> None:
    result = validate(path)
    assert result.returncode != 0, result.stderr
    found = messages(result, path)
    assert found, result.stderr
    assert any(
        f'"{field}"' in m or f"at {field})" in m or f"'{field}'" in m for m in found
    ), found


def schema(name: str) -> dict:
    return json.loads((SCHEMAS_DIR / name).read_text())


def bad_names(names) -> list[str]:
    return [n for n in names if any(p in n.lower() for p in FORBIDDEN_NAME_PARTS)]


@pytest.mark.trace("FR-018-AC-1", "TC-230")
@pytest.mark.parametrize("name", ["srs", "srs-with-as-of", "rmm"])
def test_valid_fixture_validates(name: str):
    result = validate(VALID / f"{name}.md")
    assert result.returncode == 0, result.stderr


@pytest.mark.trace("FR-018-AC-1", "TC-230")
def test_the_as_of_fixture_differs_from_the_plain_one_only_by_as_of():
    plain = frontmatter((VALID / "srs.md").read_text())
    carried = frontmatter((VALID / "srs-with-as-of.md").read_text())
    assert "as_of" not in plain and "as_of" in carried
    assert {k: v for k, v in carried.items() if k != "as_of"} == plain


@pytest.mark.trace("FR-018-AC-2", "TC-231")
@pytest.mark.parametrize("name", ["missing-version", "empty-version"])
def test_missing_or_empty_version_fails_naming_version(name: str):
    fails_naming(INVALID / f"{name}.md", "version")


@pytest.mark.trace("FR-018-AC-3", "TC-232")
def test_document_kind_outside_enum_fails_naming_document_kind():
    fails_naming(INVALID / "bad-kind.md", "document_kind")


@pytest.mark.trace("FR-018-AC-4", "TC-233")
@pytest.mark.parametrize("name", ["bad-generator", "missing-generator"])
def test_generated_by_must_be_quoin_dossier(name: str):
    fails_naming(INVALID / f"{name}.md", "generated_by")


@pytest.mark.trace("FR-018-AC-5", "TC-234")
def test_the_archetype_declares_no_digest_hash_revision_or_provenance(mappings):
    frontmatter_names = schema("dossier-document-frontmatter.schema.json")["properties"]
    record = schema("DossierDocument.json")
    mapped = mappings["models"]["DossierDocument"]["properties"]
    golden = json.loads((EXAMPLES_DIR / "DossierDocument.record.json").read_text())
    for names in (frontmatter_names, record["properties"], mapped, golden):
        assert names, "an empty name set would pass the check vacuously"
        assert bad_names(names) == []
    assert "Provenance.json" not in json.dumps(record)


@pytest.mark.trace("FR-018-AC-5", "TC-234")
def test_the_name_check_flags_each_forbidden_part():
    assert bad_names(
        ["sourceDigest", "contentHash", "sha256", "gitRevision", "provenance"]
    ) == [
        "sourceDigest",
        "contentHash",
        "sha256",
        "gitRevision",
        "provenance",
    ]
    assert bad_names(["id", "title", "asOf", "documentKind"]) == []


@pytest.mark.trace("FR-018-AC-6", "TC-235")
def test_skeleton_validates():
    result = validate(SKELETONS_DIR / "DossierDocument.md")
    assert result.returncode == 0, result.stderr


@pytest.mark.trace("FR-018-AC-8", "TC-237")
def test_rmm_requires_as_of():
    fails_naming(INVALID / "rmm-no-as-of.md", "as_of")
    assert validate(VALID / "rmm.md").returncode == 0


@pytest.mark.trace("FR-018-AC-9", "TC-238")
def test_as_of_must_be_an_rfc_3339_instant():
    fails_naming(INVALID / "bad-as-of.md", "as_of")


@pytest.mark.trace("FR-018-AC-10", "TC-239")
def test_id_is_non_empty_text_with_no_minted_default(manifest):
    assert validate(VALID / "custom-id.md").returncode == 0
    fails_naming(INVALID / "empty-id.md", "id")
    declared = next(
        t for t in manifest["artifact_types"] if t["name"] == "DossierDocument"
    )
    assert "id_pattern" not in (declared.get("defaults") or {})


@pytest.mark.trace("FR-018-AC-11", "TC-240")
def test_vocabularies_are_declared_once_per_schema_and_not_in_the_manifest(manifest):
    front = schema("dossier-document-frontmatter.schema.json")["properties"]
    record = schema("DossierDocument.json")["properties"]
    kinds = schema("DossierKind.json")
    assert sorted(front["document_kind"]["enum"]) == sorted(kinds["enum"])
    assert front["generated_by"]["const"] == record["generatedBy"]["const"]
    declared = next(
        t for t in manifest["artifact_types"] if t["name"] == "DossierDocument"
    )
    match = declared["body_extraction"]["yield_pattern"]["match"]
    for key in ("document_kind", "generated_by"):
        assert "assert" not in match[key], key


@pytest.mark.trace("FR-018-AC-13", "TC-242")
def test_record_schema_requires_as_of_for_an_rmm(schema_registry):
    golden = json.loads((EXAMPLES_DIR / "DossierDocument.record.json").read_text())
    rmm = {**golden, "documentKind": "rmm"}
    validator = schema_registry("DossierDocument")
    assert list(validator.iter_errors(golden)) == []
    assert list(validator.iter_errors(rmm)) != []
    assert list(validator.iter_errors({**rmm, "asOf": "2026-11-01T00:00:00Z"})) == []
    assert list(validator.iter_errors({**rmm, "asOf": "2026-11-01"})) != []
