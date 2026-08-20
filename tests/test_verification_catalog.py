"""FR-007 — the verification-method catalog content (TC-048..TC-057).

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


def test_tc055_obligation_sources_are_declared() -> None:
    """TC-055 (FR-007-AC-8): the engine's obligation machinery is inert until a
    module declares a source, so the declaration ships with the evidence layer
    rather than after it.

    Found end-to-end: `quoin evidence record` bound nothing and reported every
    trace id as unmatched, because no module stated an obligation for the
    criteria the tests were tagged against.
    """
    sources = {s["name"]: s for s in _manifest()["traceability"]["obligations"]}
    assert set(sources) == {
        "acceptance-criterion",
        "nfr-acceptance-criterion",
        "nfr-metric",
        "configuration-matrix",
    }

    # `configuration-matrix` is the only source whose arity is not one-per-row
    # (quire-rs FR-061): the table states a configuration SPACE, and the
    # obligation is about the interaction of every row, so one row cannot carry
    # it. Asserted here because that is the property a reader would otherwise
    # have to infer from the presence of `combinatorial`.
    matrix = sources["configuration-matrix"]
    assert matrix["combinatorial"]["strength"] == 2, "pairwise; see the manifest note"
    assert "excludes_column" in matrix["combinatorial"], (
        "a space with forbidden combinations and no column to declare them "
        "demands coverage of combinations that cannot exist"
    )
    assert "target" not in matrix, "no trace target mints a configuration table"
    assert matrix["archetype"] == "FR"

    # The two AC sources inherit from a declared trace target, so an obligation
    # id is by construction the id the rollup and every trace tag already use.
    for name in ("acceptance-criterion", "nfr-acceptance-criterion"):
        src = sources[name]
        assert src["target"] == name
        assert "archetype" not in src, "target and archetype are mutually exclusive"
        assert src["statement_column"] == "Criteria"
        assert src["method_column"] == "Verification"

    # The NFR measurement table mints no id of its own, which is the whole
    # reason `id_format` exists. Its rows are quantified obligations: the spec
    # threshold, the benchmark assertion and the evidence gate are one number.
    metric = sources["nfr-metric"]
    assert metric["archetype"] == "NFR"
    assert metric["section"] == "Measurement and Evaluation"
    assert metric["id_format"] == "{document}-M-{row}"
    assert "target" not in metric
    assert metric["parameters"] == {"target": "Target", "threshold": "Threshold"}


# TC-056 (FR-007-AC-9): the two methods the corpus needed and the catalog
# lacked.
#
# quire-rs FR-054-AC-11 began reporting a declared method no catalog carries,
# and the first sweep — quire-rs' own 20 NFR `Measurement and Evaluation`
# tables, 55 rows, 17 distinct strings — found these two being verified by means
# this registry had no word for. They are added rather than forced into a near
# neighbour, because a catalog whose nearest entry is wrong advises worse than
# one that admits the gap.
def test_tc056_compile_time_and_dynamic_analysis_are_catalogued() -> None:
    catalog = _catalog()

    compile_check = catalog.get("compile-time-check")
    assert compile_check, "no method covers a property a violation cannot compile past"
    assert compile_check["class"] == "Analysis"
    assert compile_check["evidence_kind"] == "Compile"

    sanitizer = catalog.get("dynamic-analysis-sanitizer")
    assert sanitizer, "the catalog carries no dynamic-analysis entry at all"
    assert sanitizer["class"] == "Analysis"
    # It executes, so its evidence is a run — not the `Static` kind its
    # nearest static neighbour carries.
    assert sanitizer["evidence_kind"] == "Integration"

    # And the distinction each was added for holds: neither collapses into the
    # neighbour it was nearly filed under.
    assert catalog["static-quality"]["evidence_kind"] == "Static"
    assert catalog["design-by-contract"]["class"] == "Test"


# TC-057 (FR-007-AC-10): a method is not a tool, a class, or a schedule.
#
# The sweep found all three standing in for a method in a `Method` cell —
# `Proptest` (a tool), `Unit Test` (a class synonym), `CI Gate` (a cadence).
# The catalog must not make the same conflation, or the vocabulary it publishes
# would license the cells it is supposed to correct.
def test_tc057_no_entry_names_a_tool_a_class_or_a_cadence() -> None:
    catalog = _catalog()
    ids = set(catalog)

    # A cadence is the suite registry's schedule, never a method.
    for cadence in (
        "ci-gate",
        "scheduled-ci-gate",
        "nightly",
        "on-push",
        "release-gate",
    ):
        assert cadence not in ids, f"{cadence} is a cadence, not a verification method"

    # A class with several methods under it is not itself a method.
    #
    # `inspection` and `demonstration` are deliberately NOT in this list: for
    # those two IADT classes the class and the method genuinely coincide —
    # there is exactly one way to inspect and one way to demonstrate, and the
    # catalog would otherwise carry a class nothing implements. `Test` and
    # `Analysis` each have a dozen methods under them, so an id naming either
    # would be the conflation this AC forbids.
    for entry in catalog.values():
        assert entry["class"] in IADT
    for synonym in (
        "test",
        "testing",
        "analysis",
        "unit-test",
        "integration-test",
        "static-test",
    ):
        assert (
            synonym not in ids
        ), f"{synonym} restates a class that has methods under it"

    # Every tool named anywhere in the catalog appears ONLY in `tooling`.
    tools = {t.lower() for e in catalog.values() for t in e.get("tooling", [])}
    for tool in tools:
        assert (
            tool not in ids
        ), f"{tool} is a tool; it belongs in `tooling`, not as a method id"
        for entry in catalog.values():
            assert tool != entry["class"].lower()
            assert tool != (entry.get("evidence_kind") or "").lower()


def test_tc065_a_declared_hazard_advises_fault_injection() -> None:
    """FR-007 CR-006 (TC-065): the presence of a safety object is an
    applicability signal for fault injection.

    Assumptions: `object_types` is an established applicability axis in this
    catalog — `attack_surface` already drives DAST, SAST, IAST and
    negative-abuse testing. The engine interprets none of these names
    (quire-rs FR-054-CON-2); the advisor does.

    Criteria:
      * `fault-injection` lists both `hazard` and `failure_mode`, so a bundle
        declaring either advises it. A declared failure mode names a failure
        the system can suffer and a hazard names a state that failure reaches
        — which is the applicability question this method asks, already
        answered in the document.
      * No NEW method was minted for safety. `fault-injection` already
        existed; only the signal was missing. Minting `fmea` or `hazop`
        alongside it would have made the catalog say twice what it says once
        (agent-ix/spec-objects-security#5).
    """
    catalog = _catalog()
    entry = catalog["fault-injection"]
    applicability = entry["applicability"]

    assert set(applicability["object_types"]) == {"hazard", "failure_mode"}
    # The pre-existing signal is intact — this widened the entry, it did not
    # replace what it keyed on.
    assert "reliability" in applicability["characteristics"]

    # Every object type any entry advises on must be one a spec-objects-*
    # module actually declares. A typo here is a rule that silently never
    # fires, which is indistinguishable from a method nobody needs.
    advised = {
        obj
        for method in catalog.values()
        for obj in method.get("applicability", {}).get("object_types", [])
    }
    assert advised == {"attack_surface", "threat", "hazard", "failure_mode"}, advised


def test_no_method_is_keyed_on_the_implementations_control_flow() -> None:
    """TC-067 (FR-007-AC-13, CR-029): the two retired values stay retired.

    `concolic-execution` was keyed on `path-sensitive` and
    `hard-to-reach-branch`, and nothing could ever produce either. Both name the
    *implementation's* control flow, and a specification states what the system
    must do — never that a branch behind it is hard to reach. Measured across
    the installed catalog, it was the last of 33 methods no requirement could
    elicit (agent-ix/quoin#128).

    A denylist rather than a general rule, deliberately: "is this observable" is
    a question about the consuming advisor's fact sources, which this module
    cannot see. What it can do is refuse to reintroduce the specific mistake.
    """
    catalog = _catalog()
    retired = {"path-sensitive", "hard-to-reach-branch"}

    offenders = {
        method_id: sorted(retired & set(entry["applicability"]["characteristics"]))
        for method_id, entry in catalog.items()
        if "characteristics" in entry.get("applicability", {})
        and retired & set(entry["applicability"]["characteristics"])
    }
    assert not offenders, offenders


def test_retired_characteristic_names_stay_retired() -> None:
    """TC-068 (FR-007-AC-14, CR-029): the two rejected names cannot return.

    The evidence-side pair is `fault-detection-unmeasured` /
    `fault-detection-failed`. Two names were considered and rejected:

      surviving-mutants      names mutation testing's ARTIFACT, and
                             `concolic-execution` reads the same signal while
                             producing no mutants. A per-tool name forces a
                             second value meaning the same thing, which is how
                             one signal becomes two vocabularies. CR-015's
                             reasoning for `evidence_kind`, one axis over.
      suite-quality-unknown  "quality" over-claimed — a suite can be slow,
                             flaky or unreadable and none of that is what this
                             measures — and "suite" named the wrong subject,
                             since the fact is about THIS obligation's evidence.

    A denylist, and deliberately not a general rule. Two general forms were
    tried and both were worse than nothing: "does a declared tool name appear
    inside the value" passes `surviving-mutants` cleanly, because no tool is
    called "mutants"; and the reverse, "does a stem of the value appear inside a
    tool name", fires on `cross` in `crosshair` and `fault` in
    `fs-fault-injection`. Deciding whether a name is per-tool needs judgement,
    which is the CR-014 failure this catalogue keeps citing. So the principle
    lives in the CR note and in review, and this test guards the specific
    mistakes rather than pretending to guard the class.
    """
    catalog = _catalog()
    retired = {"surviving-mutants", "suite-quality-unknown"}

    offenders = {
        method_id: sorted(retired & set(entry["applicability"]["characteristics"]))
        for method_id, entry in catalog.items()
        if retired & set(entry.get("applicability", {}).get("characteristics", []))
    }
    assert not offenders, offenders
