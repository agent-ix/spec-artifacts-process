# Explicit functional-coverage status column

Parent: `ccc2bea19de857d9adb765b7c64065ae5efbb387`, the published semantic-module
main, not the older locked `61a20e01` cohort. Scope is exactly one manifest
field: functional-coverage.status_column = Coverage Status. FR-003's normative
headers, all vocabularies, skeletons, emitted schemas and mappings are unchanged.

The coordinator explicitly approved a new NFR-001-AC-1 compatibility amendment
for this metadata. It is not an inferred exception to the earlier semantic
ticket and is not FR-003-CON-1 approval. The frozen baseline fixture is untouched.
The compatibility helper requires exactly one override on the named reference
with the exact value before removing it for the historical comparison. Missing,
wrong, other-reference and duplicate overrides each fail. Independently, removing
the one literal added line must recover the entire parent's raw manifest hash:
`a969423bd54710ca8acdf212c88652bff8b0b68b7e373de8555683132be4d206`.

Spec-first and banked tests preceded implementation. Parent measurement: one
expected missing-override failure, four negative controls pass. Candidate:
all five new controls plus historical declaration and unchanged-vocabulary tests
pass (seven total). Native schema crossover uses the exact ISO parent and the
additive schema candidate; only old ISO plus new process is rejected, naming
status_column. That required ordering is recorded rather than hidden.

Four existing controls additionally pass against the new ISO schema: complete
manifest validation, the TestMatrix body/header contract, its no-widening gate,
and the single-source column vocabulary. The final focused run is 11 passed,
25 deselected. Changed Python files pass Ruff and per-file Black checks. These
are native Python 3.13 controls with exact local package roots in PYTHONPATH;
the repository-wide coverage/report defaults were not run or claimed by this
bounded selection.

These are bounded declaration/schema results, not a new consumer sweep or
aggregate engine qualification. The old validation-stack ISO a6b1c70/process
61a20e01 pins are not moved; the coordinator owns their reviewed replacement
after immutable declaration and engine heads exist. No remote writes occurred.
