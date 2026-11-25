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


def fails_naming(path: Path, field: str, *, scope: Path = FIXTURES) -> None:
    result = quire_validate(path, scope=scope)
    assert result.returncode != 0, result.stderr
    found = messages(result, path)
    assert found, result.stderr
    assert any(
        f'"{field}"' in m
        or f"at {field})" in m
        or f"at {field}." in m
        or f"'{field}'" in m
        for m in found
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


@pytest.mark.trace("FR-018-AC-20")
@pytest.mark.parametrize(
    "name",
    [
        "missing-producer-identity",
        "missing-producer-name",
        "missing-producer-version",
        "bad-producer-name",
        "empty-producer-version",
        "extra-producer-member",
    ],
)
def test_producer_identity_requires_exact_quoin_name_and_version(name: str):
    """Invalid or incomplete producer identities fail at the producer field."""
    fails_naming(INVALID / f"{name}.md", "producer_identity")


@pytest.mark.trace("FR-018-AC-21")
def test_producer_identity_is_preserved_in_the_projected_record(mapper):
    """The producer name and version map unchanged to the record."""
    text = (VALID / "srs.md").read_text()
    record = mapper.build("DossierDocument", text, "srs.md")
    identity = {"name": "quoin", "version": "0.36.8"}

    assert record["producerIdentity"] == identity


@pytest.mark.trace("FR-018-AC-22")
def test_projected_record_schema_requires_exact_producer_identity(
    mapper, schema_registry
):
    """The projected record schema rejects missing or extra identity members."""
    text = (VALID / "srs.md").read_text()
    record = mapper.build("DossierDocument", text, "srs.md")
    schema_validator = schema_registry("DossierDocument")

    assert list(schema_validator.iter_errors(record)) == []
    invalid_records = [
        {key: value for key, value in record.items() if key != "producerIdentity"},
        {**record, "producerIdentity": {"version": "0.36.8"}},
        {**record, "producerIdentity": {"name": "quoin"}},
        {
            **record,
            "producerIdentity": {
                "name": "quoin",
                "version": "0.36.8",
                "extra": "not allowed",
            },
        },
    ]

    for invalid_record in invalid_records:
        assert list(schema_validator.iter_errors(invalid_record))


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


@pytest.mark.trace("FR-018-AC-18", "TC-246")
def test_record_schema_only_omits_version_for_records_of_processing(schema_registry):
    golden = json.loads((EXAMPLES_DIR / "DossierDocument.record.json").read_text())
    validator = schema_registry("DossierDocument")
    processing = {key: value for key, value in golden.items() if key != "version"}
    processing["documentKind"] = "records-of-processing"
    assert list(validator.iter_errors(processing)) == []
    assert list(validator.iter_errors({**processing, "version": ""})) != []
    assert list(validator.iter_errors({**processing, "documentKind": "srs"})) != []
    assert "records-of-processing" in schema("DossierKind.json")["enum"]
    frontmatter_schema = schema("dossier-document-frontmatter.schema.json")
    assert (
        "records-of-processing"
        in frontmatter_schema["properties"]["document_kind"]["enum"]
    )
    assert list(schema_registry("DossierDocument").iter_errors(processing)) == []


M2_KINDS = (
    "verification-report",
    "soup",
    "anomalies",
    "risk-management",
    "risk-management-plan",
    "release-record",
)


def m2_document(kind: str, *, as_of: bool = False) -> str:
    instant = "as_of: 2026-11-01T00:00:00Z\n" if as_of else ""
    return (
        "---\n"
        "id: DOS-M2\n"
        "title: M2 document\n"
        "type: DossierDocument\n"
        'version: "1.0"\n'
        f"document_kind: {kind}\n"
        "generated_by: quoin dossier\n"
        "producer_identity:\n"
        "  name: quoin\n"
        '  version: "0.36.8"\n'
        f"{instant}"
        "---\n"
        "# M2 document\n"
    )


@pytest.mark.trace("FR-018-AC-14", "TC-243")
@pytest.mark.parametrize("kind", M2_KINDS)
def test_each_m2_kind_validates(kind: str, tmp_path: Path):
    document = tmp_path / "dossier.md"
    document.write_text(m2_document(kind, as_of=kind == "soup"))
    result = quire_validate(document, scope=tmp_path)
    assert result.returncode == 0, result.stderr


@pytest.mark.trace("FR-018-AC-18", "TC-246")
def test_records_of_processing_validates_without_a_version(tmp_path: Path):
    document = tmp_path / "records-of-processing.md"
    document.write_text(
        "---\n"
        "id: DOS-ROP\n"
        "title: Records of Processing\n"
        "type: DossierDocument\n"
        "document_kind: records-of-processing\n"
        "generated_by: quoin dossier\n"
        "producer_identity:\n"
        "  name: quoin\n"
        '  version: "0.36.8"\n'
        "---\n"
        "# Records of Processing\n"
    )
    result = quire_validate(document, scope=tmp_path)
    assert result.returncode == 0, result.stderr


@pytest.mark.trace("FR-018-AC-17", "TC-247")
def test_threat_model_validates_without_as_of(tmp_path: Path, schema_registry):
    document = tmp_path / "threat-model.md"
    document.write_text(m2_document("threat-model"))
    result = quire_validate(document, scope=tmp_path)
    assert result.returncode == 0, result.stderr
    golden = json.loads((EXAMPLES_DIR / "DossierDocument.record.json").read_text())
    assert (
        list(
            schema_registry("DossierDocument").iter_errors(
                {**golden, "documentKind": "threat-model"}
            )
        )
        == []
    )


@pytest.mark.trace("FR-018-AC-15", "TC-244")
def test_soup_frontmatter_accepts_gap_document_without_as_of(tmp_path: Path):
    document = tmp_path / "dossier.md"
    document.write_text(m2_document("soup"))
    result = quire_validate(document, scope=tmp_path)
    assert result.returncode == 0, result.stderr
    document.write_text(m2_document("soup", as_of=True))
    result = quire_validate(document, scope=tmp_path)
    assert result.returncode == 0, result.stderr
    malformed = m2_document("soup", as_of=True).replace(
        "2026-11-01T00:00:00Z", "2026-11-01"
    )
    document.write_text(malformed)
    fails_naming(document, "as_of", scope=tmp_path)


@pytest.mark.trace("FR-018-AC-16", "TC-245")
def test_soup_record_accepts_optional_as_of(schema_registry):
    golden = json.loads((EXAMPLES_DIR / "DossierDocument.record.json").read_text())
    soup = {**golden, "documentKind": "soup"}
    validator = schema_registry("DossierDocument")
    assert list(validator.iter_errors(soup)) == []
    assert list(validator.iter_errors({**soup, "asOf": "2026-11-01T00:00:00Z"})) == []
    assert list(validator.iter_errors({**soup, "asOf": "2026-11-01"})) != []


@pytest.mark.trace("FR-018-AC-19", "TC-248")
def test_vulnerability_management_plan_kind_is_valid_in_frontmatter_and_record(
    schema_registry,
):
    """The vulnerability-management plan kind validates in both document forms."""
    result = validate(VALID / "vulnerability-management-plan.md")
    assert result.returncode == 0, result.stderr

    kind = "vulnerability-management-plan"
    frontmatter_kinds = schema("dossier-document-frontmatter.schema.json")[
        "properties"
    ]["document_kind"]["enum"]
    record_kinds = schema("DossierKind.json")["enum"]
    assert kind in frontmatter_kinds
    assert kind in record_kinds

    golden = json.loads((EXAMPLES_DIR / "DossierDocument.record.json").read_text())
    plan = {**golden, "documentKind": kind}
    assert list(schema_registry("DossierDocument").iter_errors(plan)) == []
