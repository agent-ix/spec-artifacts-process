---
id: FR-027
title: "A named person accepts a feature risk rating by signed commit"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-025"
    type: "depends_on"
  - target: "ix://agent-ix/engineering-assurance/FR-036"
    type: "references"
  - target: "ix://agent-ix/engineering-assurance/FR-037"
    type: "references"
---
# FR-027: A named person accepts a feature risk rating by signed commit

## Description

A rating is a person's judgement about a stated intended use. The module SHALL define when a supplier rating or adopter re-rating is considered accepted, so an unsigned or mismatched rating cannot be treated as a human decision.

## Inputs

- The commit that last changed the rating document.
- The `rated_by` principal from the rating.
- An allowed-signers configuration for engineering-assurance `signature-verify`.

## Outputs

- An acceptance result of `accepted` or `not_accepted` with a reason.

## Behavior

- The validation workflow SHALL report a rating as `accepted` only when `engineering-assurance signature-verify` reports `signed_valid` and `mapping: mapped`, the verified principal equals `rated_by`, and the commit contains the trailer `Signed-off-meaning: feature-risk-rating-accepted`.
- The validation workflow SHALL report a rating as `not_accepted` when its commit is unsigned, its signer is unknown or unmapped, its verified principal differs from `rated_by`, or the meaning trailer is missing.
- A `not_accepted` result SHALL name the failed condition.
- The rating document SHALL NOT store a commit id or digest as its identity; the repository history is the record of which commit changed it.
- The rule SHALL apply to both supplier ratings and adopter re-ratings.
- The validation workflow SHALL NOT infer a person's acceptance from the rating value or its evidence.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-027-AC-1 | A rating last changed by a signed-valid, mapped commit whose principal equals `rated_by` and whose trailer is present is reported as `accepted`. | Test |
| FR-027-AC-2 | An unsigned commit is reported as `not_accepted` with reason `unsigned`. | Test |
| FR-027-AC-3 | A commit signed by a key not in allowed-signers is reported as `not_accepted` with a reason naming the signer mapping failure. | Test |
| FR-027-AC-4 | A signed commit whose verified principal differs from `rated_by` is reported as `not_accepted` with a reason naming the mismatch. | Test |
| FR-027-AC-5 | A signed commit without the exact acceptance trailer is reported as `not_accepted` with reason `meaning_missing`. | Test |
| FR-027-AC-6 | The acceptance result for supplier and adopter ratings depends on the same signature conditions and records no commit id or digest in the rating file. | Inspection |

## Dependencies

- Engineering-assurance [FR-036](ix://agent-ix/engineering-assurance/FR-036) verifies the signature and [FR-037](ix://agent-ix/engineering-assurance/FR-037) maps the signer and reads the meaning trailer.
- [FR-025](./FR-025-feature-risk-rating-archetype.md) defines `rated_by` and supplier/adopter rating scope.
- PLAT-1637 implements the human-gated acceptance workflow.
