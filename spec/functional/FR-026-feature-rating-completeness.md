---
id: FR-026
title: "Feature risk rating completeness and duplicate detection"
type: FR
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/StR-001"
    type: "satisfies"
  - target: "ix://agent-ix/spec-artifacts-process/FR-004"
    type: "depends_on"
  - target: "ix://agent-ix/spec-artifacts-process/FR-025"
    type: "depends_on"
---
# FR-026: Feature risk rating completeness and duplicate detection

## Description

A tool supplier needs an observable report showing which functional requirements
have no supplier rating and which have duplicate supplier ratings. The Quoin
ratings command reports this state without changing the repository and does not
count adopter re-ratings as supplier ratings.

## Inputs

- A repository directory containing `spec/functional/` and `FeatureRiskRating` documents.
- The optional `--json` output selection.

## Outputs

- One status row for each functional requirement.
- Unreadable input diagnostics, when any Markdown document cannot be read or parsed.
- An exit status indicating whether the result is complete and duplicate-free.

## Behavior

- Quoin SHALL expose the command `quoin validation ratings --repo DIR [--json]`.
- The command SHALL read requirements and rating records under `DIR/spec/`.
- The command SHALL return a command error and a non-zero exit when `DIR/spec/` is absent or is not a directory.
- The command SHALL include every functional requirement in the ratings result.
- The command SHALL exclude adopter ratings from supplier rating counts.
- Each functional requirement result SHALL contain `feature_id`, `status` and `rating_ids`.
- A functional requirement with no supplier rating SHALL have status `unrated`.
- An `unrated` functional requirement SHALL have an empty `rating_ids` array.
- A functional requirement with one supplier rating SHALL have status `rated`.
- A `rated` functional requirement SHALL have exactly that supplier rating id in `rating_ids`.
- A functional requirement with multiple supplier ratings SHALL have status `rated_more_than_once`.
- A `rated_more_than_once` functional requirement SHALL have every conflicting supplier rating id in `rating_ids`.
- The command SHALL order functional requirement results by `feature_id`.
- The command SHALL order each `rating_ids` array lexically by rating id.
- Without `--json`, the command SHALL emit one line per functional requirement in the form `FR-ID: STATUS (rating IDs: ID[, ID…])`.
- Without `--json`, the command SHALL print `none` for an empty id list.
- Without `--json`, an empty functional-requirement set SHALL emit `supplier feature ratings: no functional requirements found`.
- With `--json`, stdout SHALL contain one JSON object with exactly the top-level members `features` and `unreadable`.
- Each object in `features` SHALL contain exactly `feature_id` (string), `status` (one of `unrated`, `rated`, `rated_more_than_once`) and `rating_ids` (array of strings).
- Each object in `unreadable` SHALL contain exactly `path` (repository-relative path using `/`) and `reason` (diagnostic text).
- The command SHALL report every unreadable functional-requirement or rating input in `unreadable` in JSON mode.
- Without `--json`, the command SHALL emit each unreadable input as `unreadable: PATH: REASON`.
- An unreadable input SHALL make the result partial.
- A partial result due to unreadable input SHALL exit with status 1.
- A `rated_more_than_once` status SHALL make the result partial.
- A partial result due to duplicate supplier ratings SHALL exit with status 1.
- A result with no unreadable inputs and no `rated_more_than_once` status SHALL exit zero.
- The command SHALL NOT create repository files.
- The command SHALL NOT edit repository files.
- The command SHALL NOT delete repository files.
- The command SHALL NOT normalize repository files.
- The manifest's required-relation rule SHALL have default severity `off`.
- When explicitly enabled at error severity, the required-relation rule SHALL report one `feature-without-risk-rating` finding for each FR with no supplier rating.
- The required-relation rule SHALL count only incoming `rates_feature` edges from supplier ratings.
- Adopter `re_rates` edges SHALL neither satisfy nor duplicate a supplier rating.
- The check SHALL remain opt-in for repositories that do not use tool validation.

## Acceptance Criteria

| ID | Criteria | Verification |
|----|----------|--------------|
| FR-026-AC-1 | Given three FRs and supplier ratings for two, validation at severity `error` reports exactly one `feature-without-risk-rating` finding naming the third FR. | Test |
| FR-026-AC-2 | The same fixture reports no `feature-without-risk-rating` finding at the default severity. | Test |
| FR-026-AC-3 | An edge from `FeatureRiskRating` to a non-FR target reports `target-kind-mismatch`. | Test |
| FR-026-AC-4 | When two supplier ratings target the same FR, the duplicate diagnostic names that FR and both rating ids. | Test |
| FR-026-AC-5 | An adopter rating for an otherwise unrated FR does not satisfy the supplier completeness rule. | Test |
| FR-026-AC-6 | An adopter rating for an FR with one supplier rating is not counted as a duplicate supplier rating. | Test |
| FR-026-AC-7 | The command accepts `quoin validation ratings --repo DIR` and reads the repository's `spec/` bundle. | Test |
| FR-026-AC-8 | Human output emits each FR status and its rating ids in the specified line format, and emits the specified empty-set message when no FR exists. | Test |
| FR-026-AC-9 | JSON stdout is one object with exactly the top-level members `features` and `unreadable`. | Test |
| FR-026-AC-10 | Each JSON feature row has exactly `feature_id`, `status` and `rating_ids`, with the declared status vocabulary and id-list cardinality. | Test |
| FR-026-AC-11 | An unreadable FR or rating file appears in human and JSON diagnostics with its path and reason. | Test |
| FR-026-AC-12 | An unreadable FR or rating input makes the result partial and exits with status 1. | Test |
| FR-026-AC-13 | A duplicate supplier rating identifies the FR and every conflicting rating id and exits with status 1. | Test |
| FR-026-AC-14 | Given a readable duplicate fixture, a command run leaves every repository path and file byte unchanged. | Test |
| FR-026-AC-15 | A missing or non-directory `DIR/spec/` returns a command error and non-zero exit without a partial status report. | Test |
| FR-026-AC-16 | JSON feature rows and rating ids are sorted lexically by their ids. | Test |
| FR-026-AC-17 | The declared rule is incoming over `rates_feature`; adopter `re_rates` do not count. | Test |
| FR-026-AC-18 | The local mapping and Quire manifest cannot currently enforce equality and uniqueness between `rates_feature` targets and the extracted assessment table; the remaining engine capability is tracked on SWM-248 and no unsupported check is claimed here. | Inspection |

## Dependencies

- [FR-025](./FR-025-feature-risk-rating-archetype.md) defines rating scope and `rates_feature`.
- [FR-027](./FR-027-human-acceptance-of-risk-ratings.md) defines human acceptance of a rating.
- Quoin PR #1053 implements the supplier-rating command; its tests bind the command-level output contract.
- Quire-rs [SWM-248](https://linear.app/agent-ix/issue/SWM-248) owns cross-table equality and per-table uniqueness assertions.
