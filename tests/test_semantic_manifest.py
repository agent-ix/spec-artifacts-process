"""The semantic block and the reference-form data_schema.

Requirement FR-010.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
import yaml
from conftest import (
    MANIFEST_PATH,
    REPO_ROOT,
    SCHEMAS_DIR,
    artifact_type_names,
    ix_module,
    run_quire,
)
from support.strict_yaml import load_yaml_strict

ADMITTED_SEMANTIC_KEYS = {
    "contract_version",
    "package",
    "exports",
    "imports",
    "targets",
    "mappings",
    "compatibility_posture",
    "legacy_forms",
}


def by_name(entries):
    return {e["name"]: e for e in entries}


@pytest.mark.trace("TC-089", "FR-010-AC-1", "FR-010-CON-1")
def test_semantic_block_carries_exactly_the_admitted_keys(semantic_block):
    assert set(semantic_block) == ADMITTED_SEMANTIC_KEYS
    assert semantic_block["contract_version"] == "1.0.0"
    assert semantic_block["package"] == "agent-ix/spec-artifacts-process"
    assert semantic_block["imports"] == {}
    assert semantic_block["targets"] == ["json-schema", "markdown"]
    assert semantic_block["compatibility_posture"] == "additive"
    assert semantic_block["legacy_forms"] == "warning"
    # Derived from the manifest, never a literal count: a type added later is
    # covered without editing this test (FR-009-CON-6).
    assert semantic_block["exports"] == artifact_type_names()


@pytest.mark.trace("TC-093", "FR-010-AC-5", "FR-004-AC-1", "FR-004-AC-23")
def test_the_module_loads_with_every_declared_archetype(manifest):
    """A `semantic` key the loader cannot parse empties the whole model silently
    (agent-ix/quire-rs#221), so every declared archetype must resolve through
    the supported CLI schema interface."""
    for artifact_type in manifest["artifact_types"]:
        name = artifact_type["name"]
        result = run_quire("schema", name)
        assert result.returncode == 0, result.stderr
        schema = json.loads(result.stdout)
        assert schema["archetype"] == name


@pytest.mark.trace("TC-152", "FR-010-AC-10")
def test_every_allowed_link_verb_is_registered(manifest):
    """Process owns its verbs; shared verbs resolve through their canonical modules."""
    allowed_verbs = {
        verb
        for artifact_type in manifest["artifact_types"]
        for verb in artifact_type.get("allowed_links", {})
    }
    external_owners = {
        "covers": "spec-artifacts-iso",
        "realizes_requirement": "spec-objects-architecture",
    }
    local_verbs = allowed_verbs - external_owners.keys()
    process_verbs = set(manifest.get("edge_types", {}))
    assert local_verbs <= process_verbs
    assert not (external_owners.keys() & process_verbs)

    resolved_manifests = {
        owner: load_yaml_strict((Path(ix_module(owner)) / "manifest.yaml").read_text())
        for owner in external_owners.values()
    }
    for verb, owner in external_owners.items():
        assert verb in resolved_manifests[owner].get(
            "edge_types", {}
        ), f"{owner} must own the canonical {verb!r} declaration"
        assert (
            sum(
                verb in owner_manifest.get("edge_types", {})
                for owner_manifest in resolved_manifests.values()
            )
            == 1
        )

    result = run_quire(
        "validate",
        str(REPO_ROOT / "tests" / "fixtures" / "adr" / "adr-realizes_requirement.md"),
        siblings=("spec-artifacts-iso", "spec-objects-architecture"),
    )
    assert result.returncode == 0, result.stderr
    assert "UnknownEdgeType:" not in result.stderr, result.stderr
    assert "DuplicateEdgeType:" not in result.stderr, result.stderr


@pytest.mark.trace("TC-094", "FR-010-AC-6")
def test_an_unknown_key_is_refused(quire_engine, tmp_path):
    """FR-010-AC-6: the refusal happens. Whether it *names* the offender is
    TC-135, which is a strict expected failure."""

    def load(mutate) -> list[str]:
        root = tmp_path / mutate.__name__
        module = root / "spec_artifacts_process"
        module.mkdir(parents=True)
        text = mutate(MANIFEST_PATH.read_text())
        (module / "manifest.yaml").write_text(text)
        shutil.copytree(SCHEMAS_DIR, module / "schemas")
        try:
            return quire_engine.Registry.load_from([str(root)]).archetype_names()
        except Exception:  # a raised refusal is still a refusal
            return []

    def unknown_key(text: str) -> str:
        return text.replace("semantic:\n", "semantic:\n  foo: bar\n", 1)

    good = quire_engine.Registry.load_from([str(REPO_ROOT)]).archetype_names()
    assert good, "the committed manifest must load"
    assert load(unknown_key) != good, "an unknown `semantic` key must be refused"
    # What does hold: the file the reference names must exist, which is the half
    # of the contract the loader does honour.
    assert load(lambda text: text) == good


@pytest.mark.xfail(
    strict=True,
    reason=(
        "FR-010-AC-9. quire-rs#221 silently drops a module with an unknown "
        "`semantic` key, so no diagnostic names the key. This strict expected "
        "failure turns green when the engine names it; it is never skipped."
    ),
)
@pytest.mark.trace("TC-135", "FR-010-AC-9")
def test_the_refusal_names_the_offending_key(quire_engine, tmp_path, capfd):
    # Keep the input loadable by the declared Quire wheel: these two unrelated
    # manifest forms landed after its supported schema version.
    manifest = load_yaml_strict(MANIFEST_PATH.read_text())
    manifest["traceability"]["trace_tags"].pop("formalizes", None)
    manifest["grammar_severity"] = {
        name: "off" if value is False else value
        for name, value in manifest["grammar_severity"].items()
    }

    valid_root = tmp_path / "valid"
    valid_module = valid_root / "spec_artifacts_process"
    valid_module.mkdir(parents=True)
    (valid_module / "manifest.yaml").write_text(
        yaml.safe_dump(manifest, sort_keys=False)
    )
    shutil.copytree(SCHEMAS_DIR, valid_module / "schemas")
    expected_names = quire_engine.Registry.load_from(
        [str(valid_root)]
    ).archetype_names()
    assert expected_names, "the control manifest must load before mutation"

    manifest["semantic"]["foo"] = "bar"
    invalid_root = tmp_path / "invalid"
    invalid_module = invalid_root / "spec_artifacts_process"
    invalid_module.mkdir(parents=True)
    (invalid_module / "manifest.yaml").write_text(
        yaml.safe_dump(manifest, sort_keys=False)
    )
    shutil.copytree(SCHEMAS_DIR, invalid_module / "schemas")
    try:
        quire_engine.Registry.load_from([str(invalid_root)]).archetype_names()
        diagnostic = capfd.readouterr()
        message = diagnostic.out + diagnostic.err
    except Exception as error:
        message = str(error)
    assert "foo" in message


@pytest.mark.trace("TC-096", "FR-010-AC-8")
def test_the_standard_object_type_is_governed_by_its_locator(manifest):
    """`Standard` (artifact type) and `standard` (object type) are two
    declarations. A document is dispatched on frontmatter `type:`, so
    `type: Standard` resolves to the artifact type; the object type is reached
    only through `object: standard`. The declaration record never holds a
    frontmatter field, so the object type carries no record schema, and its
    locator reads and requires `code` from frontmatter."""
    now = by_name(manifest["object_types"])["standard"]
    assert "data_schema" not in now
    code = now["body_extraction"]["yield_pattern"]["match"]["code"]
    assert code["from"] == "frontmatter_field"
    assert code["path"] == ["code"]
    assert code["required"] is True
    standard = by_name(manifest["artifact_types"])["Standard"]
    assert standard["data_schema"] == {"schema": "schemas/Standard.json"}


@pytest.mark.trace("TC-096", "FR-010-AC-8")
def test_the_engine_requires_code_on_a_standard(tmp_path):
    """A Standard with a string `code:` validates; one without it, or with an
    integer, is refused. The CLI checks the artifact type and object type."""

    def standard(code_line: str, *, object_type: bool = False) -> str:
        object_line = "object: standard\n" if object_type else ""
        return (
            '---\nid: Standard-201\ntitle: "a standard"\ntype: Standard\n'
            f"{object_line}{code_line}---\n"
            "# Standard-201: a standard\n\n## Description\n\nText.\n"
        )

    def validate(name: str, code_line: str, *, object_type: bool = False):
        document = tmp_path / f"{name}.md"
        document.write_text(standard(code_line, object_type=object_type))
        return run_quire(
            "validate",
            str(document),
            siblings=("spec-artifacts-iso", "spec-objects-architecture"),
        )

    artifact_valid = validate("artifact-valid", "code: abc\n")
    assert artifact_valid.returncode == 0, artifact_valid.stderr

    object_valid = validate("object-valid", "code: abc\n", object_type=True)
    assert object_valid.returncode == 0, object_valid.stderr

    missing_code = validate("missing-code", "", object_type=True)
    assert missing_code.returncode != 0
    diagnostics = missing_code.stdout + missing_code.stderr
    assert "[Standard]" in diagnostics
    assert "[standard]" in diagnostics
    assert "code" in diagnostics

    invalid_code = validate("invalid-code", "code: 12\n")
    assert invalid_code.returncode != 0
    assert "code" in invalid_code.stdout + invalid_code.stderr


@pytest.mark.trace("TC-128", "FR-010-CON-3")
def test_the_status_and_type_vocabularies_have_one_source(manifest):
    """CR-015/CR-031 restated: the three literal copies of the test-type
    vocabulary must agree, and the admitted status markers must be exactly the
    classed ones."""
    types = manifest["traceability"]["vocabularies"]["test_type"]
    matrix = by_name(manifest["artifact_types"])["TestMatrix"]["body_extraction"][
        "yield_pattern"
    ]["match"]
    suite = by_name(manifest["artifact_types"])["SuiteRegistry"]["body_extraction"][
        "yield_pattern"
    ]["match"]
    assert matrix["test_cases"]["assert"]["column_choices"]["Type"] == types
    assert suite["suites"]["assert"]["column_choices"]["Evidence Kind"] == types
    admitted = set("✅❌🚧⛔")
    status = manifest["traceability"]["status"]
    classed: set[str] = set()
    for key, value in status.items():
        if key == "column":  # names the matrix column, not a marker class
            continue
        classed |= set(value)
    # CR-031 made this the SAME SET rather than one containing the other: a
    # marker admitted by the pattern and classed by nothing is exempt from the
    # status-lie check by construction, which is exactly how `⚠️` hid six false
    # coverage claims.
    assert admitted == classed, f"admitted={sorted(admitted)} classed={sorted(classed)}"
