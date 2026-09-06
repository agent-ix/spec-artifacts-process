"""The semantic block, the reference-form data_schema, and the 0.1.0 baseline.

Requirements FR-010 and NFR-001; rows TC-089..TC-096, TC-127..TC-129, TC-135, TC-136.

This module owns the archetypes every repository in the programme validates
against, so the compatibility claim here is a **structural diff over every
declaration class** rather than a spot check. The baseline is a byte copy taken
before any edit; a baseline you can regenerate is not a baseline.
"""

from __future__ import annotations

import shutil

import pytest
from conftest import (
    MANIFEST_PATH,
    PACKAGE_ROOT,
    REPO_ROOT,
    SCHEMAS_DIR,
    artifact_type_names,
    sha256_of,
)
from support.status_column_compatibility import without_reference_status_metadata

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

# The declaration classes the baseline diff covers. Named rather than derived,
# because a class the manifest gains later must be added here deliberately —
# silently widening the diff would weaken it.
DECLARATION_CLASSES = (
    "archetypes",
    "artifact_types",
    "object_types",
    "grammars",
    "doc_kinds",
    "lint_rules",
    "traceability",
    "verification_catalog",
)


def by_name(entries):
    return {e["name"]: e for e in entries}


@pytest.mark.trace("TC-089")
def test_semantic_block_carries_exactly_the_admitted_keys(semantic_block):
    assert set(semantic_block) == ADMITTED_SEMANTIC_KEYS
    assert semantic_block["contract_version"] == "1.0.0"
    assert semantic_block["semantic_core"] == "0.1.0"
    assert semantic_block["package"] == "agent-ix/spec-artifacts-process"
    assert semantic_block["imports"] == {}
    assert semantic_block["targets"] == ["json-schema", "markdown"]
    assert semantic_block["compatibility_posture"] == "additive"
    assert semantic_block["legacy_forms"] == "warning"
    # Derived from the manifest, never a literal count: a type added later is
    # covered without editing this test (FR-009-CON-6).
    assert semantic_block["exports"] == artifact_type_names()


@pytest.mark.trace("TC-090")
def test_every_artifact_type_binds_its_schema_by_path_and_digest(manifest):
    for entry in manifest["artifact_types"]:
        data_schema = entry.get("data_schema")
        assert data_schema is not None, f"{entry['name']} declares no data_schema"
        assert set(data_schema) == {
            "schema",
            "digest",
        }, f"{entry['name']} is not the reference form"
        path = PACKAGE_ROOT / data_schema["schema"]
        assert (
            path.is_file()
        ), f"{entry['name']} references a missing {data_schema['schema']}"
        assert data_schema["digest"] == sha256_of(path)


@pytest.mark.trace("TC-091")
def test_every_0_1_0_declaration_survives_unchanged(manifest, baseline):
    """The single normative baseline assertion. FR-013-AC-7 defers to it rather
    than carrying a second copy."""
    # #409 adds one explicit, separately approved metadata exception. This helper
    # requires its exact value and unique placement before removing it; the
    # historical baseline fixture and all other declaration comparisons stay intact.
    current = without_reference_status_metadata(manifest)
    # The three additions this ticket is allowed to make, removed before the diff.
    for entry in current["artifact_types"]:
        entry.pop("data_schema", None)
    standard = by_name(current["artifact_types"])["Standard"]
    added = (
        (standard.get("body_extraction") or {})
        .get("yield_pattern", {})
        .get("match", {})
    )
    assert set(added) == {
        "properties",
        "invariants",
    }, "Standard gained an unexpected locator"
    standard.pop("body_extraction", None)
    for key in DECLARATION_CLASSES:
        assert current.get(key) == baseline.get(
            key
        ), f"{key} changed against the 0.1.0 baseline"
    assert current["manifest_version"] == baseline["manifest_version"] == "1.0.0"
    assert baseline["version"] == "0.1.0" and manifest["version"] == "0.2.0"


@pytest.mark.trace("TC-092")
def test_no_declared_vocabulary_moved(manifest, baseline):
    """Every closed vocabulary this module publishes, byte-compared.

    `⚠️` is checked by name because it is the one value a well-meaning editor is
    most likely to re-add: the `quoin:spec-matrix` skill still documents it as a
    status. The skill is the defect (agent-ix/quoin#337); CR-031 retired the
    marker because `traceability.status` classed it as nothing, so every row
    carrying it was exempt from the status-lie check by construction.
    """

    def matrix(m):
        return by_name(m["artifact_types"])["TestMatrix"]["body_extraction"][
            "yield_pattern"
        ]["match"]

    now, was = matrix(manifest), matrix(baseline)
    for table in ("test_cases", "functional_coverage"):
        assert now[table]["assert"] == was[table]["assert"], f"{table} asserts changed"
    status = now["test_cases"]["assert"]["column_patterns"]["Status"]
    assert status == r"^(✅|❌|🚧|⛔)(\s+.*)?$"
    assert "⚠️" not in status
    assert (
        manifest["traceability"]["vocabularies"]
        == baseline["traceability"]["vocabularies"]
    )
    assert "⚠️" not in str(manifest["traceability"]["status"])
    review = by_name(manifest["artifact_types"])["SpecReview"]["body_extraction"][
        "yield_pattern"
    ]["match"]
    review_was = by_name(baseline["artifact_types"])["SpecReview"]["body_extraction"][
        "yield_pattern"
    ]["match"]
    assert review["findings"]["assert"] == review_was["findings"]["assert"]


@pytest.mark.trace("TC-129")
def test_every_added_locator_is_optional(manifest, baseline):
    """NFR-001-AC-3. An added `required: true` locator makes every existing
    document of that type fail, everywhere."""
    was = {
        e["name"]: set(
            ((e.get("body_extraction") or {}).get("yield_pattern") or {}).get("match")
            or {}
        )
        for e in baseline["artifact_types"]
    }
    for entry in manifest["artifact_types"]:
        locators = (
            (entry.get("body_extraction") or {}).get("yield_pattern") or {}
        ).get("match") or {}
        for name, locator in locators.items():
            if name in was.get(entry["name"], set()):
                continue
            assert (
                locator.get("required") is False
            ), f"{entry['name']}.{name} was added at 0.2.0 and is not `required: false`"


@pytest.mark.trace("TC-093")
def test_the_module_loads_with_the_same_archetypes_as_the_baseline(
    quire_engine, tmp_path
):
    """A `semantic` key the loader cannot parse empties the whole model silently
    (agent-ix/quire-rs#221), so the archetype set is compared, not merely counted."""
    current = quire_engine.Registry.load_from([str(REPO_ROOT)]).archetype_names()
    staging = tmp_path / "spec_artifacts_process"
    staging.mkdir()
    shutil.copy(
        REPO_ROOT / "tests/fixtures/baseline-0.1.0/manifest.yaml",
        staging / "manifest.yaml",
    )
    shutil.copytree(SCHEMAS_DIR, staging / "schemas")
    before = quire_engine.Registry.load_from([str(tmp_path)]).archetype_names()
    assert sorted(current) == sorted(before)
    assert set(artifact_type_names()) <= set(current)


@pytest.mark.trace("TC-094")
def test_an_unknown_key_and_a_bad_digest_are_both_refused(quire_engine, tmp_path):
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

    def bad_digest(text: str) -> str:
        """One digest replaced by a syntactically valid, wrong one."""
        import re as _re

        return _re.sub(
            r"(    digest: sha256:)[0-9a-f]{64}", r"\g<1>" + "0" * 64, text, count=1
        )

    good = quire_engine.Registry.load_from([str(REPO_ROOT)]).archetype_names()
    assert good, "the committed manifest must load"
    assert load(unknown_key) != good, "an unknown `semantic` key must be refused"
    # The digest half is a MEASUREMENT, not an assertion of the contract we want.
    # quire 0.46.0 never verifies a reference-form `data_schema.digest`: the type
    # loads unchanged with a digest of 64 zeros. Filed as agent-ix/quire-rs#400.
    # Asserting the refusal here would be red for a defect this module cannot
    # fix; asserting the current behaviour pins it, so the day the engine starts
    # checking, this line fails and is deleted deliberately.
    assert load(bad_digest) == good, (
        "quire-rs#400: a mismatched data_schema.digest is expected to be INERT at "
        "load in the measured engine. If this fails, the engine now verifies the "
        "digest — delete this assertion and enable TC-094's refusal check."
    )
    # What does hold: the file the reference names must exist, which is the half
    # of the contract the loader does honour.
    assert load(lambda text: text) == good


@pytest.mark.xfail(
    strict=True,
    reason=(
        "FR-010-AC-9. quire 0.46.0 refuses an unknown `semantic` key and a mismatched "
        "digest SILENTLY: no diagnostic names the key, the path or the digest "
        "(agent-ix/quire-rs#221, agent-ix/quire-rs#394). This row is red by design and "
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


@pytest.mark.trace("TC-095")
def test_the_digest_rewriter_touches_nothing_else():
    import subprocess
    import sys

    before = MANIFEST_PATH.read_text()
    result = subprocess.run(
        [sys.executable, "scripts/manifest_digests.py"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert (
        MANIFEST_PATH.read_text() == before
    ), "the committed tree must already be up to date"
    assert "up to date" in result.stdout


@pytest.mark.trace("TC-096")
def test_the_standard_object_type_keeps_its_inline_schema(manifest, baseline):
    """`Standard` (artifact type) and `standard` (object type) are two
    declarations. A document is dispatched on frontmatter `type:`, so
    `type: Standard` resolves to the artifact type; the object type is reached
    only through `object: standard`."""
    now = by_name(manifest["object_types"])["standard"]
    was = by_name(baseline["object_types"])["standard"]
    assert now == was
    assert "properties" in now["data_schema"], "the object type keeps the INLINE form"
    artifact = by_name(manifest["artifact_types"])["Standard"]
    assert set(artifact["data_schema"]) == {
        "schema",
        "digest",
    }, "the artifact type is the REFERENCE form"


@pytest.mark.trace("TC-136")
def test_the_trace_targets_are_byte_identical(manifest, baseline):
    """Trace targets bind by archetype name, so adding a `data_schema` key
    changes no binding — asserted rather than assumed."""
    for key in (
        "trace_targets",
        "document_references",
        "trace_tags",
        "status",
        "source_exclude",
    ):
        assert manifest["traceability"][key] == baseline["traceability"][key], key


@pytest.mark.trace("TC-127")
def test_the_baseline_covers_every_declaration_class(baseline):
    """A diff that silently stops covering a class is worse than no diff."""
    top_level = set(baseline) - {
        "manifest_version",
        "name",
        "version",
        "description",
        "nav",
    }
    assert top_level <= set(DECLARATION_CLASSES), (
        f"the 0.1.0 manifest declares {top_level - set(DECLARATION_CLASSES)}, "
        "which the baseline diff does not cover"
    )


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
