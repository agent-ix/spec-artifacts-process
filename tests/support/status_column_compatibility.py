"""The explicitly approved #409 metadata exception, not a baseline rewrite."""

import copy


def without_reference_status_metadata(manifest):
    current = copy.deepcopy(manifest)
    references = current["traceability"]["document_references"]
    overrides = [(entry["name"], entry["status_column"]) for entry in references
                 if "status_column" in entry]
    assert overrides == [("functional-coverage", "Coverage Status")], overrides
    functional = [entry for entry in references if entry["name"] == "functional-coverage"]
    assert len(functional) == 1
    functional[0].pop("status_column")
    return current
