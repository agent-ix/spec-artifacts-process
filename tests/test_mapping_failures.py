"""The mapping failure modes and the negative corpus.

Requirements FR-011 and FR-012; rows TC-104..TC-107, TC-117, TC-118, TC-139.

Every fixture under `tests/fixtures/negative/` carries `expect:` naming the
rejection class and `because:` naming the rule. A fixture that fails for a
*different* reason than it claims is worse than no fixture, so the class is
asserted, not merely the failure.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from conftest import NEGATIVE_DIR, SKELETONS_DIR, frontmatter
from support.reference_mapping import MappingFailure

NEGATIVES = sorted(NEGATIVE_DIR.glob("*.md"))

# Every rejection FR-012 requires the corpus to cover, and the fixture that
# covers it. The map is asserted whole (TC-118) so a rejection cannot lose its
# fixture silently.
REQUIRED_REJECTIONS = {
    "missing": "specreview-missing-findings.md",
    "min-rows": "specreview-zero-rows.md",
    "id-pattern": "specreview-bad-row-id.md",
    "column-choices": "specreview-bad-severity.md",
    "status-marker": "testmatrix-warning-status.md",
    "trace-tokens": "testmatrix-bad-traces-to.md",
    "columns": "suiteregistry-dropped-column.md",
    "duplicate-row-id": "testmatrix-duplicate-row-id.md",
    "both-forms": "standard-both-forms.md",
    "orphan-fence": "standard-clause-without-fence.md",
    "clause-id": "standard-clause-id-not-identifier.md",
}


def run(mapper, path: Path):
    text = path.read_text()
    model = frontmatter(text)["type"]
    if model == "Standard":
        mapper.build(model, text, path.name)
        return mapper.declarations(model, text)
    return mapper.build(model, text, path.name)


@pytest.mark.parametrize("path", NEGATIVES, ids=lambda p: p.name)
@pytest.mark.trace("TC-117")
def test_each_negative_fails_exactly_the_check_it_names(mapper, path: Path):
    front = frontmatter(path.read_text())
    assert front["expect"].startswith(
        "mapping."
    ), "every fixture declares what it expects"
    assert front["because"].strip(), "every fixture says which rule it violates"
    expected = front["expect"].split(".", 1)[1]
    with pytest.raises(MappingFailure) as raised:
        run(mapper, path)
    assert (
        expected in raised.value.reasons
    ), f"{path.name} expects {expected!r} and reported {raised.value.reasons}"


@pytest.mark.trace("TC-118")
def test_the_negative_corpus_covers_every_stated_rejection():
    present = {p.name for p in NEGATIVES}
    assert (
        set(REQUIRED_REJECTIONS.values()) <= present
    ), f"missing fixtures: {sorted(set(REQUIRED_REJECTIONS.values()) - present)}"
    reasons = {frontmatter(p.read_text())["expect"].split(".", 1)[1] for p in NEGATIVES}
    assert (
        set(REQUIRED_REJECTIONS) <= reasons
    ), f"uncovered rejections: {sorted(set(REQUIRED_REJECTIONS) - reasons)}"


@pytest.mark.parametrize("path", NEGATIVES, ids=lambda p: p.name)
@pytest.mark.trace("TC-117")
def test_no_negative_fixture_passes(mapper, path: Path):
    with pytest.raises(MappingFailure):
        run(mapper, path)


@pytest.mark.trace("TC-104")
def test_prose_under_the_clause_section_is_an_empty_clause_list(mapper):
    """The section is optional and prose under it is commentary, not a defect."""
    text = (
        '---\nid: Standard-100\ntitle: "prose only"\n'
        "type: Standard\ncode: prose-only\n---\n"
        "# Standard-100: prose only\n\n## Invariants\n\n"
        "This standard states no formal invariant yet.\n"
    )
    record = mapper.build("Standard", text, "prose.md")
    assert "invariants" not in record


@pytest.mark.trace("TC-104")
def test_a_second_fence_in_one_subsection_is_reported(mapper):
    text = (
        '---\nid: Standard-101\ntitle: "two fences"\n'
        "type: Standard\ncode: two-fences\n---\n"
        "# Standard-101: two fences\n\n## Invariants\n\n### OneClause\n\n"
        "```ocl\ncontext X\ninv OneClause: true\n```\n\n"
        "```ocl\ncontext X\ninv Shadow: true\n```\n"
    )
    with pytest.raises(MappingFailure) as raised:
        mapper.build("Standard", text, "two.md")
    assert "second-fence" in raised.value.reasons


@pytest.mark.trace("TC-104")
def test_an_unterminated_fence_is_reported(mapper):
    text = (
        '---\nid: Standard-102\ntitle: "unterminated"\n'
        "type: Standard\ncode: unterminated\n---\n"
        "# Standard-102: unterminated\n\n## Invariants\n\n### Open\n\n"
        "```ocl\ncontext X\ninv Open: true\n"
    )
    with pytest.raises(MappingFailure) as raised:
        mapper.build("Standard", text, "open.md")
    assert "unterminated-fence" in raised.value.reasons


@pytest.mark.trace("TC-104")
def test_a_duplicate_clause_id_is_reported(mapper):
    text = (
        '---\nid: Standard-103\ntitle: "duplicate"\n'
        "type: Standard\ncode: duplicate\n---\n"
        "# Standard-103: duplicate\n\n## Invariants\n\n"
        "### Same\n\n```ocl\ncontext X\ninv Same: true\n```\n\n"
        "### Same\n\n```ocl\ncontext X\ninv Same: false\n```\n"
    )
    with pytest.raises(MappingFailure) as raised:
        mapper.build("Standard", text, "dup.md")
    assert "duplicate-clause-id" in raised.value.reasons


@pytest.mark.trace("TC-106")
def test_three_independent_defects_are_reported_in_one_pass(mapper):
    """A mapper that stops at the first error makes a reviewer run it once per
    defect, which is how a third defect gets found in production."""
    text = (
        '---\nid: SR-910\ntitle: "three defects"\ntype: SpecReview\n'
        "analysis: base\nreview_set: subset\n---\n"
        "# SR-910: three defects\n\n## Summary\n\nThree independent problems below.\n\n"
        "## Findings\n\n"
        "| ID | Severity | Summary | Refs |\n| --- | --- | --- | --- |\n"
        "| FIND-1 | low | wrong id namespace | FR-1 |\n"
        "| FND-2 | critical | severity outside the vocabulary | FR-2 |\n"
        "| FND-3 | low | fine | FR-3 |\n"
        "| FND-3 | low | duplicate id | FR-4 |\n"
    )
    with pytest.raises(MappingFailure) as raised:
        mapper.build("SpecReview", text, "three.md")
    reasons = raised.value.reasons
    assert {"id-pattern", "column-choices", "duplicate-row-id"} <= set(reasons)
    assert all(error.line > 0 for error in raised.value.errors)
    assert all(error.model == "SpecReview" for error in raised.value.errors)


@pytest.mark.trace("TC-107")
def test_duplicate_row_id_names_both_lines(mapper):
    path = NEGATIVE_DIR / "testmatrix-duplicate-row-id.md"
    with pytest.raises(MappingFailure) as raised:
        mapper.build("TestMatrix", path.read_text(), path.name)
    duplicate = next(e for e in raised.value.errors if e.reason == "duplicate-row-id")
    assert "first at line" in duplicate.detail
    assert duplicate.line > 0


@pytest.mark.trace("TC-139")
def test_row_ids_are_unique_per_table_not_per_document(mapper):
    """A TestMatrixIndex carries INT- and GAP- ids in different tables, and a
    document-scoped rule would reject conforming documents."""
    text = (SKELETONS_DIR / "TestMatrixIndex.md").read_text()
    collided = text.replace("| INT-001 |", "| INT-1 |").replace(
        "| GAP-001 |", "| GAP-1 |"
    )
    record = mapper.build("TestMatrixIndex", collided, "index.md")
    assert record["integrationMatrix"][0]["id"] == "INT-1"
    assert record["coverageGaps"][0]["id"] == "GAP-1"


@pytest.mark.trace("TC-105")
def test_both_declaration_forms_in_one_document_build_no_record(mapper):
    path = NEGATIVE_DIR / "standard-both-forms.md"
    with pytest.raises(MappingFailure) as raised:
        mapper.declarations("Standard", path.read_text())
    assert raised.value.reasons == ["both-forms"]
