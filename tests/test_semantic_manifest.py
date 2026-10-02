"""The semantic block and the reference-form data_schema.

Requirement FR-010; rows TC-089, TC-093, TC-094, TC-096, TC-128, TC-135.
"""

from __future__ import annotations

import shutil

import pytest
from conftest import (
    MANIFEST_PATH,
    REPO_ROOT,
    SCHEMAS_DIR,
    artifact_type_names,
)

ADMITTED_SEMANTIC_KEYS = {
    "contract_version",
    "semantic_core",
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


@pytest.mark.trace("TC-089")
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


@pytest.mark.trace("TC-093")
def test_the_module_loads_with_every_declared_archetype(quire_engine):
    """A `semantic` key the loader cannot parse empties the whole model silently
    (agent-ix/quire-rs#221), so the archetype set is compared, not merely counted."""
    current = quire_engine.Registry.load_from([str(REPO_ROOT)]).archetype_names()
    assert set(artifact_type_names()) <= set(current)


@pytest.mark.trace("TC-094")
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
        "FR-010-AC-9. quire refuses an unknown `semantic` key "
        "SILENTLY: no diagnostic names the key or the path "
        "(agent-ix/quire-rs#221). This row is red by design and "
        "turns green the day the engine names them. It is never skipped, because a "
        "skipped row is not coverage."
    ),
)
@pytest.mark.trace("TC-135")
def test_the_refusal_names_the_offending_key(quire_engine, tmp_path, capfd):
    module = tmp_path / "spec_artifacts_process"
    module.mkdir(parents=True)
    (module / "manifest.yaml").write_text(
        MANIFEST_PATH.read_text().replace("semantic:\n", "semantic:\n  foo: bar\n", 1)
    )
    shutil.copytree(SCHEMAS_DIR, module / "schemas")
    try:
        quire_engine.Registry.load_from([str(tmp_path)]).archetype_names()
        diagnostic = capfd.readouterr()
        message = diagnostic.out + diagnostic.err
    except Exception as error:
        message = str(error)
    assert "foo" in message


@pytest.mark.trace("TC-096")
def test_the_standard_object_type_keeps_its_inline_schema(manifest):
    """`Standard` (artifact type) and `standard` (object type) are two
    declarations. A document is dispatched on frontmatter `type:`, so
    `type: Standard` resolves to the artifact type; the object type is reached
    only through `object: standard`."""
    now = by_name(manifest["object_types"])["standard"]
    assert "properties" in now["data_schema"], "the object type keeps the INLINE form"


@pytest.mark.trace("TC-128")
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
