"""The Markdown mapping, the golden records and the skeletons.

Requirements FR-011 and FR-012; rows TC-097..TC-119 and TC-137..TC-142.

The mapping is shipped module DATA. The implementation under test lives in
`tests/support/` and is a test ORACLE: nothing in the published package imports
it (FR-011-CON-3).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from conftest import (
    EXAMPLES_DIR,
    MAPPINGS_SCHEMA_PATH,
    PACKAGE_ROOT,
    SCHEMAS_DIR,
    SKELETONS_DIR,
    artifact_type_names,
    frontmatter,
)
from support.reference_mapping import digest_of

DECLARED_KINDS = (
    "frontmatter",
    "section",
    "table",
    "typed-table",
    "sysml-fence",
    "ocl-clause",
    "list",
    "token",
    "provenance",
)

# The `token` kind is exercised inside a `typed-table` cell rather than as a
# top-level entry: the `Traces To` parse IS the token mapping. `sysml-fence` is
# likewise declared as the `alternate` of a typed table. Both are named here so
# the totality check knows where to look for them.
NESTED_KINDS = {"token": "trace-tokens", "sysml-fence": "alternate"}


def skeleton(name: str) -> str:
    return (SKELETONS_DIR / name).read_text()


def golden(model: str) -> dict[str, Any]:
    return json.loads((EXAMPLES_DIR / f"{model}.record.json").read_text())


def model_schema(model: str) -> dict[str, Any]:
    return json.loads((SCHEMAS_DIR / f"{model}.json").read_text())


def declared_properties(model: str) -> set[str]:
    return set(model_schema(model)["properties"])


def build(mapper, model: str, text: str, path: str = "fixture.md") -> dict[str, Any]:
    record = mapper.build(model, text, path)
    if model == "Standard":
        declarations = mapper.declarations("Standard", text)
        if declarations:
            record["properties"] = declarations
        else:
            record.pop("properties", None)
    return record


@pytest.mark.trace("TC-097")
def test_mappings_validates_against_its_own_schema(mappings):
    from jsonschema import Draft202012Validator

    schema = json.loads(MAPPINGS_SCHEMA_PATH.read_text())
    errors = list(Draft202012Validator(schema).iter_errors(mappings))
    assert errors == [], [f"{list(e.path)}: {e.message}" for e in errors]
    assert mappings["authority"] == "markdown"
    assert mappings["round_trip"] == "derived-projection"
    assert set(mappings["models"]) == set(artifact_type_names())


@pytest.mark.trace("TC-098")
def test_the_mapping_is_total_in_both_directions(mappings):
    """Every model property is named exactly once, and every entry names a
    declared property. A one-directional check passes a mapping that describes a
    property the model does not have."""
    for model, spec in mappings["models"].items():
        declared = declared_properties(model)
        mapped = set(spec["properties"])
        assert mapped == declared, (
            f"{model}: unmapped={sorted(declared - mapped)} "
            f"undeclared={sorted(mapped - declared)}"
        )


@pytest.mark.trace("TC-138")
def test_the_totality_walk_terminates_on_the_cyclic_bundle(mappings):
    """The emitted models `$ref` each other; a naive recursive walk does not
    terminate. This walks the whole reachable graph and asserts it closes."""
    seen: set[str] = set()
    frontier = [f"{m}.json" for m in mappings["models"]]
    while frontier:
        name = frontier.pop()
        if name in seen:
            continue
        seen.add(name)
        path = SCHEMAS_DIR / name
        if not path.is_file():
            continue
        for ref in json.dumps(json.loads(path.read_text())).split('"$ref": "')[1:]:
            target = ref.split('"')[0].rsplit("/", 1)[-1]
            if target not in seen:
                frontier.append(target)
    assert len(seen) >= len(mappings["models"])


@pytest.mark.trace("TC-099")
def test_every_named_section_and_column_is_declared_by_the_manifest(mappings, manifest):
    """FR-011-CON-1: the mapping asserts no contract the manifest does not."""
    locators = {
        at["name"]: ((at.get("body_extraction") or {}).get("yield_pattern") or {}).get(
            "match"
        )
        or {}
        for at in manifest["artifact_types"]
    }
    for model, spec in mappings["models"].items():
        declared = locators[spec["archetype"]]
        headings = {
            loc.get("under_section") or loc.get("after_heading")
            for loc in declared.values()
        }
        for prop, entry in spec["properties"].items():
            heading = entry.get("heading")
            if heading is None or entry.get("whole_body"):
                continue
            assert (
                heading in headings
            ), f"{model}.{prop} names an undeclared section {heading!r}"
            locator = next(
                loc
                for loc in declared.values()
                if heading in (loc.get("under_section"), loc.get("after_heading"))
            )
            asserted = (locator.get("assert") or {}).get("columns")
            if asserted and entry.get("columns"):
                assert (
                    entry["columns"] == asserted
                ), f"{model}.{prop} column list differs"


@pytest.mark.trace("TC-140")
def test_every_declared_mapping_kind_is_used(mappings, semantic_block):
    """A kind declared and used by nothing is a declaration the engine cannot
    honour — the shape this repository has hit before (CR-037, CR-081)."""
    assert semantic_block["mappings"] == list(DECLARED_KINDS)
    used = set()
    for spec in mappings["models"].values():
        for entry in spec["properties"].values():
            used.add(entry["kind"])
            if entry.get("alternate"):
                used.add(entry["alternate"]["kind"])
            for cell in (entry.get("fields") or {}).values():
                if cell["parse"] == "trace-tokens":
                    used.add("token")
    assert used == set(DECLARED_KINDS), f"unused: {sorted(set(DECLARED_KINDS) - used)}"


@pytest.mark.parametrize(
    "path", sorted(SKELETONS_DIR.glob("*.md")), ids=lambda p: p.name
)
@pytest.mark.trace("TC-100")
def test_each_skeleton_maps_to_a_record_that_validates(
    mapper, schema_registry, path: Path
):
    model = frontmatter(path.read_text())["type"]
    record = build(mapper, model, path.read_text(), f"skeletons/{path.name}")
    errors = list(schema_registry(model).iter_errors(record))
    assert errors == [], [f"{list(e.path)}: {e.message}" for e in errors]


@pytest.mark.parametrize("model", sorted(artifact_type_names()))
@pytest.mark.trace("TC-142")
def test_the_golden_record_is_reproduced_exactly(mapper, model: str):
    """The committed record is the contract. There is deliberately no
    regenerate target: a mapping change that alters a record fails here and has
    to be accepted by hand, so a blessed snapshot of a bug cannot slip in."""
    path = SKELETONS_DIR / f"{model}.md"
    record = build(mapper, model, path.read_text(), f"skeletons/{path.name}")
    assert record == golden(model)


@pytest.mark.trace("TC-115")
def test_the_two_standard_forms_declare_the_same_fields(mapper):
    table = build(mapper, "Standard", skeleton("Standard.md"), "skeletons/Standard.md")
    fence = build(
        mapper, "Standard", skeleton("Standard.sysml.md"), "skeletons/Standard.md"
    )
    assert table["properties"] == fence["properties"]
    assert table["invariants"] == fence["invariants"]
    # Provenance differs by construction: the two files are different bytes.
    for record in (table, fence):
        record.pop("provenance")
    assert table == fence


@pytest.mark.trace("TC-141")
def test_exactly_one_skeleton_carries_a_properties_section():
    carriers = [
        p.name
        for p in sorted(SKELETONS_DIR.glob("*.md"))
        if any(line.strip() == "## Properties" for line in p.read_text().split("\n"))
    ]
    assert carriers == ["Standard.md", "Standard.sysml.md"]


@pytest.mark.parametrize(
    "cell,expected",
    [
        ("✅", {"marker": "✅"}),
        (
            "🚧 scale evidence deferred",
            {"marker": "🚧", "note": "scale evidence deferred"},
        ),
        ("⛔ superseded by TC-001", {"marker": "⛔", "note": "superseded by TC-001"}),
    ],
)
@pytest.mark.trace("TC-101")
def test_status_splits_marker_from_note(cell: str, expected: dict):
    from support.reference_mapping import parse_status

    assert parse_status(cell) == expected


@pytest.mark.parametrize("cell", ["⚠️ partial", "Done", "✅ Complete ⚠️", "partial ✅"])
@pytest.mark.trace("TC-101")
def test_status_rejects_anything_but_a_leading_declared_marker(cell: str):
    from support.reference_mapping import parse_status

    if cell == "✅ Complete ⚠️":
        assert parse_status(cell) == {"marker": "✅", "note": "Complete ⚠️"}
        return
    assert parse_status(cell) is None


@pytest.mark.parametrize(
    "cell,expected",
    [
        ("FR-001", {"tokens": ["FR-001"], "noTrace": False}),
        (
            "FR-001-AC-2, -AC-3, -AC-4",
            {"tokens": ["FR-001-AC-2", "FR-001-AC-3", "FR-001-AC-4"], "noTrace": False},
        ),
        (
            "FR-016-AC-1/2/3",
            {"tokens": ["FR-016-AC-1", "FR-016-AC-2", "FR-016-AC-3"], "noTrace": False},
        ),
        ("-", {"tokens": [], "noTrace": True}),
        (
            "FR-001 (partial)",
            {"tokens": ["FR-001"], "noTrace": False, "note": "partial"},
        ),
    ],
)
@pytest.mark.trace("TC-102")
def test_traces_to_expands_both_shorthands(cell: str, expected: dict):
    from support.reference_mapping import parse_traces

    assert parse_traces(cell) == expected


@pytest.mark.parametrize(
    "cell", ["FR-1; FR-2", "", "FR-", "-AC-1", "prose about FR-001"]
)
@pytest.mark.trace("TC-102")
def test_traces_to_rejects_the_forms_the_pattern_rejects(cell: str):
    from support.reference_mapping import parse_traces

    assert parse_traces(cell) is None


@pytest.mark.trace("TC-103")
def test_an_omitted_optional_column_yields_no_key(mapper):
    """CR-018: 49 of 169 ecosystem matrices author no priority anywhere. The
    record must omit the key, never synthesise a value."""
    text = skeleton("TestMatrix.md")
    lines = []
    for line in text.split("\n"):
        if (
            line.startswith("| Test ID |")
            or line.startswith("| TC-")
            or set(line.strip()) <= set("|- ")
        ):
            cells = line.split("|")
            if len(cells) == 8:
                del cells[4]
                line = "|".join(cells)
        lines.append(line)
    record = build(mapper, "TestMatrix", "\n".join(lines))
    assert record["testCases"], "the stripped matrix still declares rows"
    for row in record["testCases"]:
        assert "priority" not in row


@pytest.mark.trace("TC-108")
def test_an_escaped_pipe_is_one_cell():
    from support.reference_mapping import split_row

    assert split_row(r"| INSP-1 | FR-1 | who | a1b2c3d | Pass\|Fail | note |") == [
        "INSP-1",
        "FR-1",
        "who",
        "a1b2c3d",
        "Pass|Fail",
        "note",
    ]


@pytest.mark.parametrize(
    "path", sorted(SKELETONS_DIR.glob("*.md")), ids=lambda p: p.name
)
@pytest.mark.trace("TC-109")
def test_a_crlf_copy_maps_to_the_same_record(mapper, path: Path):
    text = path.read_text()
    model = frontmatter(text)["type"]
    crlf = text.replace("\n", "\r\n")
    assert build(mapper, model, text, "x.md") == build(mapper, model, crlf, "x.md")
    assert digest_of(text) == digest_of(crlf)


@pytest.mark.parametrize(
    "path", sorted(SKELETONS_DIR.glob("*.md")), ids=lambda p: p.name
)
@pytest.mark.trace("TC-110")
def test_every_unnamed_frontmatter_key_is_declared_dropped(
    mapper, mappings, path: Path
):
    text = path.read_text()
    model = frontmatter(text)["type"]
    declared = set(mappings["models"][model]["dropped_frontmatter_keys"])
    for key in mapper.dropped_keys(model, text):
        assert (
            key in declared
        ), f"{path.name} drops {key!r} and the mapping does not declare it"


@pytest.mark.trace("TC-137")
def test_each_model_agrees_with_its_frontmatter_schema(mappings, manifest):
    """The migration must not replace one pair of drifting declarations with
    another: where a model and a frontmatter schema describe the same key, they
    must agree on type and pattern."""
    by_name = {at["name"]: at for at in manifest["artifact_types"]}
    checked = 0
    for model, spec in mappings["models"].items():
        front = json.loads(
            (PACKAGE_ROOT / by_name[model]["frontmatter_schema_ref"]).read_text()
        )
        schema = model_schema(model)
        for prop, entry in spec["properties"].items():
            if entry["kind"] != "frontmatter":
                continue
            key = entry["path"][0]
            if key not in front["properties"]:
                continue
            declared = front["properties"][key]
            emitted = schema["properties"][prop]
            if "$ref" in emitted:
                target = json.loads(
                    (SCHEMAS_DIR / emitted["$ref"].rsplit("/", 1)[-1]).read_text()
                )
            else:
                target = emitted
            if "pattern" in declared:
                assert (
                    target.get("pattern") == declared["pattern"]
                ), f"{model}.{prop} pattern"
                checked += 1
            if "enum" in declared:
                assert sorted(target.get("enum", [])) == sorted(
                    declared["enum"]
                ), f"{model}.{prop} enum"
                checked += 1
            if "const" in declared:
                assert target.get("const") == declared["const"], f"{model}.{prop} const"
                checked += 1
    assert checked > 0, "the agreement check compared nothing"
