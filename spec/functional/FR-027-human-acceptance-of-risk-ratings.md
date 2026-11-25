---
id: FR-027
title: "A named person accepts a feature risk rating by signed commit"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/StR-001"
    type: "satisfies"
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
- The rating's `status`.
- An allowed-signers configuration for engineering-assurance `signature-verify`.
- A versioned `engineering-assurance.signature-verify-request/v1` request.

## Outputs

- An acceptance result of `accepted` or `not_accepted` with a reason.
- External-tool version and configuration-index evidence in the Quoin validation report.

## Behavior

- The acceptance workflow SHALL send the `engineering-assurance.signature-verify-request/v1` request to `engineering-assurance signature-verify`.
- The request SHALL contain exactly the `protocol`, `repository`, `revision`, `kind` and `allowed_signers` members defined by engineering-assurance [FR-036](ix://agent-ix/engineering-assurance/FR-036).
- The request's `protocol` SHALL equal `engineering-assurance.signature-verify-request/v1`.
- The request's `repository` SHALL be an absolute repository directory path.
- The request's `revision` SHALL identify the commit that last changed the rating.
- The request's `kind` SHALL equal `commit`.
- The request's `allowed_signers` SHALL be an absolute path to the required allowed-signers file.
- The workflow SHALL accept only an `engineering-assurance.signature-verify-result/v1` response with `status: signed_valid` and `signer.mapping: mapped`.
- The workflow SHALL validate the response's `protocol`, `status`, `kind`, `signer.mapping`, `signer.principal` and `signed_off_meaning` members before evaluating acceptance.
- The workflow SHALL report a rating as `accepted` only when its status is `accepted`, the verified principal equals `rated_by`, and the commit contains the exact trailer `Signed-off-meaning: feature-risk-rating-accepted`.
- The workflow SHALL report a rating as `not_accepted` when its status is `proposed`.
- The workflow SHALL require `signed_off_meaning.presence: present`.
- The workflow SHALL require `signed_off_meaning.values` to include `feature-risk-rating-accepted`.
- The workflow SHALL report a rating as `not_accepted` when the verifier returns any status other than `signed_valid`.
- The validation workflow SHALL report a rating as `not_accepted` when its commit is unsigned.
- The validation workflow SHALL report a rating as `not_accepted` when its signer is unknown or unmapped.
- The validation workflow SHALL report a rating as `not_accepted` when its verified principal differs from `rated_by`.
- The validation workflow SHALL report a rating as `not_accepted` when the meaning trailer is missing.
- A `not_accepted` result SHALL name the failed condition.
- The workflow SHALL report a rating as `not_accepted` when the verifier process cannot start, exits unexpectedly, times out, or returns malformed output.
- The workflow SHALL report a rating as `not_accepted` when the allowed-signers file is unavailable, unreadable or malformed.
- Engineering-assurance FR-037's `signature_verify_allowed_signers_invalid` machine error and exit status 2 SHALL never produce an `accepted` result.
- The workflow SHALL reject a response whose protocol is not `engineering-assurance.signature-verify-result/v1` or whose required response members are malformed or absent.
- An Engineering Assurance `engineering-assurance.error/v1` response or non-zero verifier process exit SHALL never produce an `accepted` result.
- The rating document SHALL NOT store a commit id or digest as its identity; the repository history is the record of which commit changed it.
- The rule SHALL apply to both supplier ratings and adopter re-ratings.
- The validation workflow SHALL NOT infer a person's acceptance from the rating value or its evidence.
- The `accepted` status SHALL mean the signed acceptance record satisfies the stated verification conditions.
- The workflow SHALL NOT decide whether a person should accept the risk.
- The person responsible for the intended use SHALL decide whether to accept the risk.
- Quoin [FR-217](ix://agent-ix/quoin/FR-217) SHALL produce the validation report containing external tool versions.
- Quoin [FR-220](ix://agent-ix/quoin/FR-220) SHALL define the external-tools configuration index referenced by that report.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-027-AC-1 | A rating last changed by a signed-valid, mapped commit whose principal equals `rated_by` and whose trailer is present is reported as `accepted`. | Test |
| FR-027-AC-2 | An unsigned commit is reported as `not_accepted` with reason `unsigned`. | Test |
| FR-027-AC-3 | A commit signed by a key not in allowed-signers is reported as `not_accepted` with a reason naming the signer mapping failure. | Test |
| FR-027-AC-4 | A signed commit whose verified principal differs from `rated_by` is reported as `not_accepted` with a reason naming the mismatch. | Test |
| FR-027-AC-5 | A signed commit without the exact acceptance trailer is reported as `not_accepted` with reason `meaning_missing`. | Test |
| FR-027-AC-6 | The acceptance result for supplier and adopter ratings depends on the same signature conditions and the rating schema records no commit id or digest. | Test |
| FR-027-AC-7 | The workflow sends exactly the versioned FR-036 request members and accepts only the versioned FR-036 result protocol. | Test |
| FR-027-AC-8 | A verifier process that cannot start produces `not_accepted` with a verifier failure reason. | Test |
| FR-027-AC-9 | A verifier process that times out or exits unexpectedly produces `not_accepted` with a verifier failure reason. | Test |
| FR-027-AC-10 | Verifier output that cannot be parsed produces `not_accepted` with a verifier failure reason. | Test |
| FR-027-AC-11 | Missing, unreadable or malformed allowed-signers input produces `not_accepted`; FR-037's `signature_verify_allowed_signers_invalid` error never produces acceptance. | Test |
| FR-027-AC-12 | A response with a wrong protocol or missing/malformed required result members produces `not_accepted`. | Test |
| FR-027-AC-13 | A rating marked `proposed` is reported `not_accepted`, including when its commit is otherwise signed-valid. | Test |
| FR-027-AC-14 | An accepted rating requires a `rated_by` principal matching the verified signer and the exact acceptance trailer. | Test |
| FR-027-AC-13 | The Quoin validation report identifies the versions of external tools and references their FR-220 configuration-index entries. | Test |

## Dependencies

- Engineering-assurance [FR-036](ix://agent-ix/engineering-assurance/FR-036) verifies the signature and [FR-037](ix://agent-ix/engineering-assurance/FR-037) maps the signer and reads the meaning trailer.
- [FR-025](./FR-025-feature-risk-rating-archetype.md) defines `rated_by` and supplier/adopter rating scope.
- PLAT-1637 implements the human-gated acceptance workflow.
