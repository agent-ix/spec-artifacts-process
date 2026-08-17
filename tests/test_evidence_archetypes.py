"""FR-006 — the evidence-layer archetypes (TC-040..TC-047).

Half manifest-data assertions and half behavioural: the behavioural half drives
the real `quire validate` against this module's manifest, so the contract is
asserted as an author experiences it rather than as a YAML shape.

Requires the `quire` CLI on PATH for the behavioural half; those tests are
skipped when it is absent, so a checkout without the toolchain still runs the
manifest assertions — which is the half that would silently rot otherwise.
"""

from __future__ import annotations

import pathlib
import shutil
import subprocess

import pytest
import yaml

import spec_artifacts_process as pack

MANIFEST_PATH = pack.MANIFEST_PATH
FIXTURES = pathlib.Path(__file__).parent / "fixtures" / "evidence"

needs_quire = pytest.mark.skipif(
    shutil.which("quire") is None,
    reason="the `quire` CLI is required to validate against the module manifest",
)


def _manifest() -> dict:
    return yaml.safe_load(MANIFEST_PATH.read_text())


def _archetype(name: str) -> dict:
    at = next(
        (a for a in _manifest().get("artifact_types", []) if a["name"] == name), None
    )
    assert at is not None, f"the manifest declares no `{name}` artifact_type"
    return at


def _assert_facet(archetype: str, key: str) -> dict:
    match = _archetype(archetype)["body_extraction"]["yield_pattern"]["match"]
    return match[key]["assert"]


def validate(fixture: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["quire", "validate", "--module", str(pack.PACK_ROOT), str(FIXTURES / fixture)],
        capture_output=True,
        text=True,
        check=False,
    )


def assert_valid(fixture: str) -> None:
    result = validate(fixture)
    assert (
        result.returncode == 0
    ), f"{fixture} must satisfy the contract\n{result.stdout}\n{result.stderr}"


def assert_invalid(fixture: str, *, mentions: str = "") -> None:
    result = validate(fixture)
    output = result.stdout + result.stderr
    assert result.returncode != 0, f"{fixture} must fail the contract\n{output}"
    if mentions:
        assert mentions in output, f"the diagnostic must name `{mentions}`\n{output}"


# ── Manifest data (FR-006-AC-1..AC-4) ───────────────────────────────────────


def test_tc040_suite_registry_archetype_declared() -> None:
    """TC-040 (FR-006-AC-1)."""
    at = _archetype("SuiteRegistry")
    assert (
        at["frontmatter_schema_ref"] == "schemas/suite-registry-frontmatter.schema.json"
    )

    facet = _assert_facet("SuiteRegistry", "suites")
    assert facet["columns"] == ["ID", "Name", "Command", "Tool", "Evidence Kind"]
    assert facet["min_rows"] == 1
    assert facet["id_column"] == "ID"
    # Structured and doc-scoped. A kebab slug here is what produced the 1,014
    # dead trace tags (quire-rs#72); everything joins on this id.
    assert facet["id_pattern"] == r"^SUITE-\d+$"


def test_tc041_inspections_archetype_declared() -> None:
    """TC-041 (FR-006-AC-2)."""
    at = _archetype("Inspections")
    assert at["frontmatter_schema_ref"] == "schemas/inspections-frontmatter.schema.json"

    facet = _assert_facet("Inspections", "inspections")
    assert facet["columns"] == [
        "ID",
        "Obligation",
        "Who",
        "Commit",
        "Verdict",
        "Note",
    ]
    # A passing inspection often has nothing to add, so the column may be
    # omitted rather than filled with a placeholder.
    assert facet["optional_columns"] == ["Note"]
    assert facet["min_rows"] == 1
    assert facet["id_pattern"] == r"^INSP-\d+$"
    assert facet["column_choices"]["Verdict"] == ["Pass", "Fail", "Waived"]


def test_tc042_evidence_kind_is_the_declared_test_type_vocabulary() -> None:
    """TC-042 (FR-006-AC-3): one vocabulary, three uses (CR-015).

    The registry restates `test_type` rather than referencing it, because
    `from_vocabulary` does not exist yet (quire-rs#146). This test IS the thing
    keeping the two copies honest until it does — if it is ever deleted, the
    duplication becomes silent.
    """
    manifest = _manifest()
    declared = manifest["traceability"]["vocabularies"]["test_type"]
    kinds = _assert_facet("SuiteRegistry", "suites")["column_choices"]["Evidence Kind"]
    assert kinds == declared, (
        "the suite registry's Evidence Kind vocabulary has drifted from the "
        "declared test_type vocabulary; they are the same vocabulary"
    )
    # The Test Matrix `Type` column is the third use of the same list.
    matrix_types = _assert_facet("TestMatrix", "test_cases")["column_choices"]["Type"]
    assert matrix_types == declared


def test_tc043_suite_and_inspection_are_trace_targets() -> None:
    """TC-043 (FR-006-AC-4): declaring them as targets is what makes SUITE-N and
    INSP-N referenceable id classes, so FR-049's dangling-reference check covers
    them for free."""
    targets = {t["name"]: t for t in _manifest()["traceability"]["trace_targets"]}

    suite = targets.get("suite")
    assert suite is not None, "no `suite` trace target"
    assert suite["archetype"] == "SuiteRegistry"
    assert suite["section"] == "Suites"
    assert suite["id_column"] == "ID"
    # CR-062: archetype binding only; a `document:` key no longer loads.
    assert "document" not in suite

    inspection = targets.get("inspection")
    assert inspection is not None, "no `inspection` trace target"
    assert inspection["archetype"] == "Inspections"
    assert inspection["section"] == "Inspections"

    # The obligation cell is a declared reference, so a typo dangles rather
    # than recording an act against nothing.
    refs = {r["name"]: r for r in _manifest()["traceability"]["document_references"]}
    obligation = refs.get("inspection-obligation")
    assert obligation is not None, "no `inspection-obligation` document reference"
    assert obligation["archetype"] == "Inspections"
    assert obligation["column"] == "Obligation"
    assert set(obligation["targets"]) == {
        "acceptance-criterion",
        "nfr-acceptance-criterion",
    }


# ── Behaviour (FR-006-AC-5..AC-8) ───────────────────────────────────────────


@needs_quire
def test_tc044_suite_registry_contract_is_enforced() -> None:
    """TC-044 (FR-006-AC-5)."""
    assert_valid("suites-valid.md")
    # A kebab slug where a structured id belongs.
    assert_invalid("suites-bad-id.md", mentions="assert")
    # A dropped required column.
    assert_invalid("suites-missing-column.md", mentions="assert")
    # An evidence kind outside the declared vocabulary. `SAST` is a real
    # method-class an author would reach for, which is exactly why the closed
    # vocabulary has to reject it rather than absorb it.
    assert_invalid("suites-bad-kind.md", mentions="assert")


@needs_quire
def test_tc045_inspection_contract_is_enforced() -> None:
    """TC-045 (FR-006-AC-6)."""
    assert_valid("inspections-valid.md")
    # `Note` is optional: omitting the column entirely still validates.
    assert_valid("inspections-no-note.md")
    assert_invalid("inspections-bad-verdict.md", mentions="assert")


@needs_quire
def test_tc046_shipped_skeletons_validate() -> None:
    """TC-046 (FR-006-AC-7): the shipped authoring path produces a conformant
    document. A skeleton that does not validate against its own archetype sends
    every author who copies it into a failure."""
    for skeleton in ("SuiteRegistry.md", "Inspections.md"):
        path = pack.PACK_ROOT / "skeletons" / skeleton
        assert path.is_file(), f"no skeleton shipped for {skeleton}"
        result = subprocess.run(
            ["quire", "validate", "--module", str(pack.PACK_ROOT), str(path)],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, (
            f"the shipped {skeleton} skeleton does not satisfy its own archetype\n"
            f"{result.stdout}\n{result.stderr}"
        )


@needs_quire
def test_tc047_adoption_is_optional(tmp_path: pathlib.Path) -> None:
    """TC-047 (FR-006-AC-8): a repository that declares neither document is
    unaffected. Adding archetypes must not make an existing corpus incomplete."""
    spec = tmp_path / "spec"
    spec.mkdir()
    (spec / "FR-001.md").write_text(
        "---\nid: FR-001\ntype: FR\ntitle: A requirement\n---\n\n"
        "## Acceptance Criteria\n\n"
        "| ID | Criteria | Verification |\n|----|----------|--------------|\n"
        "| FR-001-AC-1 | The engine emits one record per row. | Test (TC-001) |\n"
    )
    result = subprocess.run(
        [
            "quire",
            "coverage",
            "--scope",
            str(tmp_path),
            "--module",
            str(pack.PACK_ROOT),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"{result.stdout}\n{result.stderr}"
    output = result.stdout + result.stderr
    # Narrow deliberately: the assertion is that the evidence layer is SILENT
    # for a non-adopting repo — no scan diagnostic, no group, no document row.
    # (It also happens that neither archetype declares `allowed_links`, so
    # neither adds an `UnknownEdgeType` line to the module's existing noise.)
    for absent in ("SuiteRegistry", "Inspections", "suites.md", "inspections.md"):
        assert absent not in output, (
            f"a repo declaring no evidence layer must not hear "
            f"about `{absent}`\n{output}"
        )
