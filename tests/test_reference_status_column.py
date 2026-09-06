"""One declared status column; exact parent and frozen historical controls."""

import copy
import hashlib

import pytest
from conftest import MANIFEST_PATH
from support.status_column_compatibility import without_reference_status_metadata


@pytest.mark.trace("TC-144")
def test_exact_override_is_the_only_manifest_delta(manifest):
    """FR-004-AC-16: parent ccc2bea19, not the older 61a20e01 cohort."""
    unchanged = without_reference_status_metadata(manifest)
    assert unchanged["traceability"]["status"]["column"] == "Status"
    text = MANIFEST_PATH.read_text()
    addition = "    status_column: Coverage Status\n"
    assert text.count(addition) == 1
    assert hashlib.sha256(text.replace(addition, "").encode()).hexdigest() == "a969423bd54710ca8acdf212c88652bff8b0b68b7e373de8555683132be4d206"


@pytest.mark.trace("TC-145")
@pytest.mark.parametrize("mutation", ["missing", "wrong", "another", "duplicate"])
def test_compatibility_exception_cannot_hide_another_change(manifest, mutation):
    """NFR-001-AC-1: omission, value, placement and multiplicity are guarded."""
    value = copy.deepcopy(manifest)
    refs = value["traceability"]["document_references"]
    functional = next(entry for entry in refs if entry["name"] == "functional-coverage")
    if mutation == "missing":
        functional.pop("status_column", None)
    elif mutation == "wrong":
        functional["status_column"] = "Status"
    elif mutation == "another":
        next(entry for entry in refs if entry["name"] != "functional-coverage")["status_column"] = "Coverage Status"
    else:
        refs.append(copy.deepcopy(functional))
    with pytest.raises(AssertionError):
        without_reference_status_metadata(value)
