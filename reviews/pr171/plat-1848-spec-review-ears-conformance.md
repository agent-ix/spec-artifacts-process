---
id: SR-2026112016223475846355045
title: "EARS review — rating requirements"
type: SpecReview
analysis: ears-conformance
scope: "agent-ix/spec-artifacts-process; PLAT-1848; spec/functional/FR-025-feature-risk-rating-archetype.md, spec/functional/FR-027-human-acceptance-of-risk-ratings.md"
review_set: subset
---

## Summary

The changed FR-025 and NFR-002 statements and the FR-027 acceptance workflow requirements were reviewed. The changed statements are sufficiently singular and verifiable; the validator warning on an unchanged FR-027 line is pre-existing and outside the changed obligations.

## Verdict

**PASS** — The changed FR-025 and NFR-002 statements and the FR-027 acceptance workflow requirements were reviewed. The changed statements are sufficiently singular and verifiable; the validator warning on an unchanged FR-027 line is pre-existing and outside the changed obligations.

## Scope

| ID | Path | Role | Excerpt |
| --- | --- | --- | --- |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | A tool supplier and an adopter can assess the same feature under different intended uses. The module SHALL declare a `FeatureRiskRating` artifact type that records a proposed or accepted rating and the requirements it covers, while keeping supplier ratings and adopter re-ratings distinct. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - The module SHALL require frontmatter fields `id`, `type`, `scope`, `rating`, `status` and `relationships` for a `FeatureRiskRating` document. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - `status` SHALL be exactly `proposed` or `accepted`. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - A proposed rating SHALL NOT have a `rated_by` field. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - An accepted rating SHALL have a `rated_by` field naming its allowed-signers principal. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - A supplier rating SHALL identify its intended use with the typed `uses_intended_use` relationship. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - An adopter rating SHALL identify its intended use with the `intended_use` field. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - The `id` field SHALL match `FRR-{next:03d}`. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - The `type` field SHALL equal `FeatureRiskRating`. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - `scope` SHALL be exactly `supplier` or `adopter`. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - The `rating` field SHALL equal `high_process_risk` or `not_high_process_risk`. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - The schema SHALL reject every other `rating` value. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - The schema SHALL declare no default `rating` value. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - When present, `rated_by` SHALL name the allowed-signers principal of the person who accepted the rating. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - A supplier rating SHALL have exactly one `uses_intended_use` relationship to an `IntendedUse` record in the same tool repository. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - An adopter rating's `intended_use` field SHALL identify the adopter's own intended-use subject in the engineering-assurance integrator package. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - This module SHALL NOT redefine the adopter's intended-use subject or copy the adopter configuration. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - The module SHALL declare the edge `re_rates` from adopter `FeatureRiskRating` to supplier `FeatureRiskRating`, with inverse `rerated_by`. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - The module SHALL declare the edge `uses_intended_use` from supplier `FeatureRiskRating` to `IntendedUse`, with inverse `used_by_rating`. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - A supplier rating SHALL carry one or more `rates_feature` relationships to functional requirements. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - A supplier rating SHALL NOT carry a `re_rates` relationship. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - An adopter rating SHALL carry one or more `re_rates` relationships to supplier `FeatureRiskRating` records. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - Each adopter `re_rates` target SHALL cover the same functional requirements as the adopter rating. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - An adopter rating SHALL NOT carry a `rates_feature` relationship. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - The schema SHALL reject relationships that do not match the rating's `scope`. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - The `rates_feature` relationship SHALL identify every functional requirement covered by a supplier rating. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - The rating record SHALL NOT carry per-requirement failure-mode or detection details. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - The rating record SHALL NOT contain a `Feature assessments` section or corresponding property. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - The document SHALL contain a `Rationale` section. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - The document SHALL contain an `Assurance activities` section. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - The rationale SHALL explain why the rating fits the intended use. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - Assurance activities SHALL identify each selected test, inspection or analysis. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - Each assurance activity SHALL identify the acceptance criterion it addresses. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - A rating document MAY cover multiple requirements. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - When one rating covers multiple requirements, its rating SHALL apply to each target. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - When one rating covers multiple requirements, its rationale SHALL apply to each target. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - An adopter rating SHALL be a separately authored assessment for the adopter's intended use. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - An adopter rating SHALL NOT replace or edit its supplier rating. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - An adopter rating SHALL NOT imply acceptance of its supplier rating. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - The records SHALL contain no calculated risk score, threshold or probability. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - The records SHALL contain no product-criticality value. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - The records SHALL contain no assigned software-safety-class value. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - The records SHALL contain no computed rating. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - The adopter MAY use the rating and other evidence to make its own TCL, TQL or T-class determination. |
| FR-025 | spec/functional/FR-025-feature-risk-rating-archetype.md | examined | - This module SHALL define no formula or mapping for those determinations. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The acceptance workflow SHALL send the `engineering-assurance.signature-verify-request/v1` request to `engineering-assurance signature-verify`. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The request SHALL contain exactly the `protocol`, `repository`, `revision`, `kind` and `allowed_signers` members defined by engineering-assurance [FR-036](ix://agent-ix/engineering-assurance/FR-036). |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The request's `protocol` SHALL equal `engineering-assurance.signature-verify-request/v1`. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The request's `repository` SHALL be an absolute repository directory path. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The request's `revision` SHALL identify the commit that last changed the rating. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The request's `kind` SHALL equal `commit`. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The request's `allowed_signers` SHALL be an absolute path to the required allowed-signers file. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The workflow SHALL accept only an `engineering-assurance.signature-verify-result/v1` response with `status: signed_valid` and `signer.mapping: mapped`. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The workflow SHALL validate the response's `protocol`, `status`, `kind`, `signer.mapping`, `signer.principal` and `signed_off_meaning` members before evaluating acceptance. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The workflow SHALL report a rating as `accepted` only when its status is `accepted`, the verified principal equals `rated_by`, and the commit contains the exact trailer `Signed-off-meaning: feature-risk-rating-accepted`. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The workflow SHALL report a rating as `not_accepted` when its status is `proposed`. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The workflow SHALL require `signed_off_meaning.presence: present`. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The workflow SHALL require `signed_off_meaning.values` to include `feature-risk-rating-accepted`. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The workflow SHALL report a rating as `not_accepted` when the verifier returns any status other than `signed_valid`. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The validation workflow SHALL report a rating as `not_accepted` when its commit is unsigned. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The validation workflow SHALL report a rating as `not_accepted` when its signer is unknown or unmapped. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The validation workflow SHALL report a rating as `not_accepted` when its verified principal differs from `rated_by`. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The validation workflow SHALL report a rating as `not_accepted` when the meaning trailer is missing. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - A `not_accepted` result SHALL name the failed condition. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The workflow SHALL report a rating as `not_accepted` when the verifier process cannot start, exits unexpectedly, times out, or returns malformed output. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The workflow SHALL report a rating as `not_accepted` when the allowed-signers file is unavailable, unreadable or malformed. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - Engineering-assurance FR-037's `signature_verify_allowed_signers_invalid` machine error and exit status 2 SHALL never produce an `accepted` result. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The workflow SHALL reject a response whose protocol is not `engineering-assurance.signature-verify-result/v1` or whose required response members are malformed or absent. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - An Engineering Assurance `engineering-assurance.error/v1` response or non-zero verifier process exit SHALL never produce an `accepted` result. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The rating document SHALL NOT store a commit id or digest as its identity; the repository history is the record of which commit changed it. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The rule SHALL apply to both supplier ratings and adopter re-ratings. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The validation workflow SHALL NOT infer a person's acceptance from the rating value or its evidence. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The `accepted` status SHALL mean the signed acceptance record satisfies the stated verification conditions. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The workflow SHALL NOT decide whether a person should accept the risk. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - The person responsible for the intended use SHALL decide whether to accept the risk. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - Quoin [FR-217](ix://agent-ix/quoin/FR-217) SHALL produce the validation report containing external tool versions. |
| FR-027 | spec/functional/FR-027-human-acceptance-of-risk-ratings.md | examined | - Quoin [FR-220](ix://agent-ix/quoin/FR-220) SHALL define the external-tools configuration index referenced by that report. |

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | low | No findings (placeholder) | - |
