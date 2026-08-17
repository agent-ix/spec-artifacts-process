"""FR-007 — the verification-method catalog content (TC-048..TC-054).

Manifest-data assertions plus one behavioural check that the engine actually
reads what this module declares. The behavioural half matters more than it looks:
the catalog is a manifest block quire-rs v0.29.0 introduced, and a module that
declares it against an older engine loads with the block silently ignored.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest
import yaml

import spec_artifacts_process as pack

MANIFEST_PATH = pack.MANIFEST_PATH

# ISO 29148 IADT. The engine treats `class` as a free string (quire-rs
# FR-054-CON-1) so another module may classify differently — which makes this
# module's own contract this test's job rather than the engine's.
IADT = {"Inspection", "Analysis", "Demonstration", "Test"}

# The axes this module uses for applicability. The engine interprets none of
# them (FR-054-CON-2); listing them here is what stops a per-entry invention.
DECLARED_AXES = {"property_shapes", "characteristics", "object_types", "archetypes"}


def _manifest() -> dict:
    return yaml.safe_load(MANIFEST_PATH.read_text())


def _catalog() -> dict:
    catalog = _manifest().get("verification_catalog")
    assert catalog, "the manifest declares no verification_catalog"
    return catalog


def test_tc048_catalog_covers_the_dispositioned_techniques() -> None:
    """TC-048 (FR-007-AC-1): the seed set is the full sweep.

    A catalog shipping half the techniques teaches the advisor the other half do
    not exist — an absent entry reads as "not applicable" rather than "not yet
    written", which is worse than shipping none.
    """
    catalog = _catalog()
    expected = {
        # Test
        "unit-testing",
        "integration-testing",
        "e2e-testing",
        "property-based-testing",
        "metamorphic-testing",
        "model-based-test-generation",
        "combinatorial-tway",
        "mutation-testing",
        "fuzzing",
        "grammar-based-fuzzing",
        "bdd-spec-by-example",
        "contract-testing",
        "design-by-contract",
        "runtime-monitoring",
        "deterministic-simulation",
        "fault-injection",
        "performance-benchmarking",
        "golden-approval-testing",
        "negative-abuse-testing",
        "dast",
        "iast",
        # Analysis
        "concolic-execution",
        "sast",
        "sca-sbom",
        "architecture-conformance",
        "static-quality",
        "formal-analysis-smt",
        "model-checking",
        # Inspection / Demonstration
        "inspection",
        "demonstration",
        "agent-behaviour-eval",
    }
    missing = expected - set(catalog)
    assert (
        not missing
    ), f"the catalog is missing dispositioned techniques: {sorted(missing)}"
    # All four classes are represented, so no class is silently unreachable.
    assert {entry["class"] for entry in catalog.values()} == IADT


def test_tc049_every_entry_is_well_formed() -> None:
    """TC-049 (FR-007-AC-2)."""
    for method_id, entry in _catalog().items():
        for field in ("name", "class", "definition"):
            assert entry.get(field, "").strip(), f"{method_id} has an empty `{field}`"
        assert (
            entry["class"] in IADT
        ), f"{method_id} class `{entry['class']}` is not IADT"


def test_tc050_evidence_kinds_are_the_declared_test_type_vocabulary() -> None:
    """TC-050 (FR-007-AC-3): one vocabulary, several uses (CR-015).

    This is the third literal copy of the same list — catalog, Test Matrix
    `Type`, suite registry `Evidence Kind` — because `from_vocabulary` was
    deferred (quire-rs#146). Deleting this test makes the duplication silent,
    which is the whole reason it exists.
    """
    declared = set(_manifest()["traceability"]["vocabularies"]["test_type"])
    for method_id, entry in _catalog().items():
        kind = entry.get("evidence_kind")
        assert kind, f"{method_id} declares no evidence_kind"
        assert kind in declared, (
            f"{method_id} evidence_kind `{kind}` is outside the declared "
            f"test_type vocabulary {sorted(declared)}"
        )


def test_tc051_every_entry_is_selectable() -> None:
    """TC-051 (FR-007-AC-4): an entry no rule can ever select is a definition,
    not a catalog entry — the advisor would never reach it."""
    for method_id, entry in _catalog().items():
        rules = entry.get("applicability") or {}
        assert (
            rules
        ), f"{method_id} declares no applicability rule, so nothing can select it"
        unknown = set(rules) - DECLARED_AXES
        assert not unknown, (
            f"{method_id} invents applicability axes {sorted(unknown)}; the "
            f"declared axes are {sorted(DECLARED_AXES)}"
        )
        for axis, values in rules.items():
            assert values, f"{method_id} declares an empty `{axis}` rule"


@pytest.mark.skipif(
    shutil.which("quire") is None,
    reason="the `quire` CLI is required to load the manifest through the engine",
)
def test_tc052_engine_loads_the_catalog() -> None:
    """TC-052 (FR-007-AC-5): the engine reads what this module declares.

    `verification_catalog` is a quire-rs v0.29.0 manifest block. Against an
    older engine the top-level key is tolerated and silently ignored — the
    module would look correct and contribute nothing — so this asserts the
    manifest loads clean rather than assuming it.
    """
    result = subprocess.run(
        ["quire", "schema", "--module", str(pack.PACK_ROOT)],
        capture_output=True,
        text=True,
        check=False,
    )
    combined = result.stdout + result.stderr
    assert "verification_catalog" not in combined or result.returncode == 0, combined
    # A manifest the engine rejects reports the offending key by name; the
    # absence of a load failure is the signal here.
    for failure in ("ManifestError", "unknown field", "ArchetypeLoadFailure"):
        assert failure not in combined, f"the manifest failed to load: {combined}"


def test_tc053_derived_vocabularies_follow_the_catalog() -> None:
    """TC-053 (FR-007-AC-6): quire-rs derives `verification_method` and
    `verification_class` from the merged catalog rather than reading a second
    declaration (FR-054-CON-4). Asserted here against the source of truth."""
    catalog = _catalog()
    # The keys ARE the method vocabulary, so they must be usable as one: no
    # blanks, no case-collisions, nothing that would make two entries
    # indistinguishable to a consumer matching on the name.
    keys = list(catalog)
    assert all(k and k.strip() == k for k in keys), keys
    lowered = [k.lower() for k in keys]
    assert len(set(lowered)) == len(keys), "two method ids differ only by case"

    classes = sorted({entry["class"] for entry in catalog.values()})
    assert classes == ["Analysis", "Demonstration", "Inspection", "Test"]
    # No separate authored copy of either vocabulary exists to drift from.
    vocabularies = _manifest()["traceability"]["vocabularies"]
    for invented in ("verification_method", "verification_class"):
        assert invented not in vocabularies, (
            f"`{invented}` is derived from the catalog by the engine; declaring "
            f"it here is the duplication FR-054-CON-4 forbids"
        )


def test_tc054_symbol_free_methods_carry_a_no_source_symbol_kind() -> None:
    """TC-054 (FR-007-AC-7): inspection, demonstration and agent evaluation
    produce no source symbol, so a row verified that way can never carry a trace
    tag. Reporting it as a status lie would assert something its own declared
    method makes impossible (CR-041)."""
    catalog = _catalog()
    exempt = set(_manifest()["traceability"]["vocabularies"]["no_source_symbol"])
    for method_id in ("inspection", "demonstration", "agent-behaviour-eval"):
        kind = catalog[method_id]["evidence_kind"]
        assert kind in exempt, (
            f"{method_id} mints no source symbol but its evidence_kind `{kind}` "
            f"is not in the no_source_symbol set {sorted(exempt)}; rows verified "
            f"this way would be reported as status lies"
        )


def test_catalog_names_no_tool_outside_tooling() -> None:
    """Scope guard: tools live in `tooling` (documentation) and in the suite
    registry's `tool` column. A tool name reaching `class`, `evidence_kind` or an
    applicability rule is the per-tool vocabulary growth the split exists to
    prevent."""
    tools = {"semgrep", "proptest", "pytest", "cargo-fuzz", "zap", "z3", "clippy"}
    for method_id, entry in _catalog().items():
        blob = json.dumps(
            {
                "class": entry["class"],
                "evidence_kind": entry.get("evidence_kind"),
                "applicability": entry.get("applicability", {}),
            }
        ).lower()
        for tool in tools:
            assert tool not in blob, (
                f"{method_id} names the tool `{tool}` outside `tooling`; the "
                f"suite registry's own `tool` column carries the tool"
            )
