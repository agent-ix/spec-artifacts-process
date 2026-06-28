"""Manifest validity + pack entrypoint tests."""

from __future__ import annotations

import json
import pathlib

import pytest
import yaml

import spec_artifacts_process as pack

MANIFEST_PATH = pack.MANIFEST_PATH


def test_pack_exposes_manifest_path() -> None:
    assert MANIFEST_PATH == pack.PACK_ROOT / "manifest.yaml"
    assert MANIFEST_PATH.is_file()


def test_manifest_loads() -> None:
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    assert manifest["manifest_version"] == "1.0.0"
    assert manifest["name"] == "spec-artifacts-process"
    assert manifest["version"]


def test_spec_review_archetype_registered_with_findings_validation() -> None:
    """SpecReview is the per-analysis review archetype: a Summary section plus a
    Findings table whose Severity column is constrained to low/medium/high
    (quire CR-010 `column_choices`)."""
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())

    names = {a["name"] for a in manifest["archetypes"]}
    assert "SpecReview" in names, "SpecReview archetype must be registered"

    sr = next(t for t in manifest["artifact_types"] if t["name"] == "SpecReview")
    assert sr["frontmatter_schema_ref"] == "schemas/spec-review-frontmatter.schema.json"

    findings = sr["body_extraction"]["yield_pattern"]["match"]["findings"]
    assert findings["from"] == "table_row"
    assert findings["under_section"] == "Findings"
    assert findings["assert"]["columns"] == ["ID", "Severity", "Summary", "Refs"]
    assert findings["assert"]["column_choices"]["Severity"] == [
        "low",
        "medium",
        "high",
    ]
    assert findings["assert"]["id_pattern"] == r"^FND-\d+$"

    schema_path = pack.PACK_ROOT / "schemas" / "spec-review-frontmatter.schema.json"
    assert schema_path.is_file()
    schema = json.loads(schema_path.read_text())
    assert schema["properties"]["type"]["const"] == "SpecReview"

    # An authoring skeleton must exist so `quoin write --types SpecReview`
    # emits the authoritative template (catalog resolves skeletons/<Name>.md).
    skeleton = pack.PACK_ROOT / "skeletons" / "SpecReview.md"
    assert skeleton.is_file()
    body = skeleton.read_text()
    assert "type: SpecReview" in body
    header = next(line for line in body.splitlines() if line.strip().startswith("| ID"))
    assert [c.strip() for c in header.strip().strip("|").split("|")] == [
        "ID",
        "Severity",
        "Summary",
        "Refs",
    ]


def test_track_archetype_registered_as_node_between_plan_and_task() -> None:
    """Track is a first-class node inserted BETWEEN Plan and Task so a four-level
    Spec -> Plan -> Track -> Task hierarchy can map onto external trackers
    (TC-010). Plan expects Track (and, for backward compatibility, still Task);
    Track expects Task. The legacy `track:` field on Task remains valid."""
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())

    # Registered as an archetype with Task as its expected member.
    archetypes = {a["name"]: a for a in manifest["archetypes"]}
    assert "Track" in archetypes, "Track archetype must be registered"
    track = archetypes["Track"]
    assert track["supports_membership"] is True
    assert track["composition"]["expected_artifacts"] == ["Task"]

    # Inserted into the containment chain: Plan now expects Track (Task kept
    # for backward compatibility with legacy Plan -> Task bundles).
    plan = archetypes["Plan"]
    assert plan["composition"]["expected_artifacts"] == ["Track", "Task"]

    # Registered as an artifact type with schema + container links.
    track_type = next(t for t in manifest["artifact_types"] if t["name"] == "Track")
    assert (
        track_type["frontmatter_schema_ref"]
        == "schemas/track-frontmatter.schema.json"
    )
    assert "contains" in track_type["allowed_links"]

    # Schema validates the Track node shape.
    schema_path = pack.PACK_ROOT / "schemas" / "track-frontmatter.schema.json"
    assert schema_path.is_file()
    schema = json.loads(schema_path.read_text())
    assert schema["properties"]["type"]["const"] == "Track"

    # Authoring skeleton exists so `quoin write --types Track` resolves it.
    skeleton = pack.PACK_ROOT / "skeletons" / "Track.md"
    assert skeleton.is_file()
    assert "type: Track" in skeleton.read_text()

    # Backward compatibility: legacy `track:` field still valid on Task.
    task_schema = json.loads(
        (pack.PACK_ROOT / "schemas" / "task-frontmatter.schema.json").read_text()
    )
    assert task_schema["properties"]["track"]["type"] == "string"
    assert "track" not in task_schema.get("required", [])


def test_manifest_validates_against_fr035_schema() -> None:
    """Skip if jsonschema lacks draft 2020-12 (use CI check-jsonschema instead)."""
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        pytest.skip("jsonschema lib missing draft 2020-12 support")
    schema_path = (
        pathlib.Path(__file__).resolve().parent / "module-manifest.schema.json"
    )
    if not schema_path.exists():
        pytest.skip("FR-035 schema not bundled with tests")
    schema = json.loads(schema_path.read_text())
    manifest = yaml.safe_load(MANIFEST_PATH.read_text())
    errors = list(Draft202012Validator(schema).iter_errors(manifest))
    assert not errors, [
        f"{'.'.join(str(p) for p in e.absolute_path)}: {e.message}" for e in errors
    ]
