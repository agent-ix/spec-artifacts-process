---
id: SR-20261113084030
title: "Base review of FR-016 anomaly release rationale (spec-artifacts-process#147)"
type: SpecReview
analysis: base
review_set: subset
scope: "agent-ix/spec-artifacts-process; PR #147 (git diff origin/main...plat-1528-spec-sap at 2b6d5e3): spec/functional/FR-016-anomaly-release-rationale.md, spec/non-functional/NFR-001-anomaly-diagnostics-in-one-pass.md, spec/spec.md, spec/functional/index.md"
relationships:
  - target: "ix://agent-ix/spec-artifacts-process/FR-016"
    type: references
---

# Base review of FR-016 anomaly release rationale (spec-artifacts-process#147)

## Summary

Ticket: PLAT-1528. Method: spec-review/base, scoped to `git diff origin/main...HEAD` of agent-ix/spec-artifacts-process#147 at 2b6d5e3.
Read against FR-011, FR-014 and FR-015 on main and the consuming side in agent-ix/quoin#857 (FR-162, FR-163, FR-164, NFR-035).

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | The closed-anomaly rule keys on `resolution` is not `wont-fix`, which also holds when a `closed` anomaly has no `resolution` (already an FR-014 finding at the `status` line) or a mistyped one (already a vocabulary finding). Whether such a document also gets a section finding is unstated, and the two natural `AnomalyFields.json` encodings differ: a `properties: {resolution: {not: {const: wont-fix}}}` condition holds vacuously on an absent key, while a `required: [resolution]` guard does not. FR-014 resolves the analogous case explicitly (status rules apply only to a status in the vocabulary). State whether the rule applies only to a `resolution` in the vocabulary, and add the case to AC-2. | spec/functional/FR-016-anomaly-release-rationale.md:51 |
| FND-002 | medium | The shipped-fixture list names valid `assessed` and `resolved` anomalies with the section but no `identified` one, while AC-1 requires an `impacting` anomaly at `identified` carrying the section to validate. Add an `identified` `impacting` fixture with the section to the list (and say which pairs serve AC-10). | spec/functional/FR-016-anomaly-release-rationale.md:69-70 |
| FND-003 | medium | The ownership table assigns the closed-status rule and the Author/Rationale value rules to the manifest, `assert` facet and `AnomalyFields.json` only. FR-014 and FR-015 each also state that the emitted record schema `Anomaly.json` (FR-009) carries the same rules for the mapped record (quoin FR-073), and quoin FR-162/FR-164 read the mapped `releaseRationale`. As written, a mapped record with a placeholder entry, or with a rationale on a `closed` `fixed` anomaly, passes `Anomaly.json`; AC-7 only requires that the schema declare the key. State whether `Anomaly.json` carries these rules, as FR-014/FR-015 do, and cover it in AC-7. | spec/functional/FR-016-anomaly-release-rationale.md:34 |
| FND-004 | medium | quoin FR-163-AC-4 (companion quoin#857) uses this module's shipped `closed` `wont-fix` fixture and needs its `closed_by` to differ from the rationale `Author`, so the test can tell the typed author from `closed_by`. FR-016 only says the fixture carries `closed_by` and the section; a fixture with the same name in both makes the quoin AC unable to fail. Require the fixture's `closed_by` to differ from every row's `Author`. | spec/functional/FR-016-anomaly-release-rationale.md:69-70 |
| FND-005 | low | FR-016 adds the record key `releaseRationale` and new `AnomalyFields.json` rules, but does not extend FR-014's enumerations: FR-014's mapping bullet and AC-7 name the `Anomaly` record keys, and its `AnomalyFields.json` bullet lists the `yield_pattern.match` keys verbatim. PLAT-1527 amended FR-014 for `verification`; here FR-014 stays silent and FR-016 names no `yield_pattern.match` key for the section. Add `releaseRationale` and the section's match key to FR-014's lists, or name the match key in FR-016. | spec/functional/FR-016-anomaly-release-rationale.md:59-61 |
| FND-006 | low | The title ("releasing with an anomaly open") and the first Description sentence ("releasing with this anomaly still open") describe only open anomalies, but the amended FR admits the section on a `closed` `wont-fix` anomaly. Reword to 'carried' or 'not fixed', matching quoin FR-162's term. | spec/functional/FR-016-anomaly-release-rationale.md:3, 19-21 |

## Verdict

Changes requested: four medium findings (the closed-anomaly rule on absent or mistyped `resolution`; a missing `identified` fixture for AC-1; `Anomaly.json` not stated to carry the new rules, unlike FR-014/FR-015; and the `closed` `wont-fix` fixture not constrained to serve quoin FR-163-AC-4), plus two low.

Checked and clean: the closed-anomaly rule itself is consistent across Behavior, the ownership table, AC-2 and the fixture list (admitted at any non-`closed` status and at `closed` `wont-fix`, refused at `closed` `fixed`, `duplicate` and `not-a-defect`, at the section heading line); it matches FR-014's status/resolution vocabularies and its intended `wont-fix` close path; the placeholder list and case-insensitive comparison are exactly FR-014's `closed_by` rule and exactly quoin FR-164's value rule, so `quire validate` and the gate agree; `releaseRationale` follows the camelCase record-key convention (`closedBy`, `safetyImpact`); no default, no computed cell, no skeleton section, no date, commit, signature or acceptance field (consistent with FR-014/FR-015 and FR-163's git attribution); no paywalled standard text is quoted; no compatibility layer, fallback or migration path is introduced; quoin holds no copy of the fixtures.

Examined (role examined): FR-016, FR-016-AC-1, FR-016-AC-2, FR-016-AC-3, FR-016-AC-4, FR-016-AC-5, FR-016-AC-6, FR-016-AC-7, FR-016-AC-8, FR-016-AC-9, FR-016-AC-10.
Context only: FR-014, FR-015, quoin/FR-163-AC-4, quoin/FR-164.

## New findings (disposition pass 1)

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-007 | medium | quoin FR-164-AC-5 (quoin#857) needs an `impacting` anomaly `closed` as `wont-fix` with no rationale (fails unjustified-impacting) and the same with a rationale (passes), and quoin FR-162-AC-12 requires those documents to be this module's. FR-016 ships one `closed` `wont-fix` fixture with the section, does not say it is `impacting`, and gives it no section-less counterpart (AC-10 counterparts cover only identified, assessed and resolved). Require the `closed` `wont-fix` fixture to be `impacting` and to have a counterpart identical but for the section. | spec/functional/FR-016-anomaly-release-rationale.md:77 |
| FND-008 | low | The FR-014 amendment cites FR-015 for all three table keys, `releaseRationale` included, and FR-014's Downstream still names only FR-015. Cite FR-016 for `releaseRationale` and add FR-016 to Downstream. | spec/functional/FR-014-anomaly-archetype-and-state-lifecycle.md:78-81, 133 |
| FND-009 | low | The ownership row still says FR-164 decides whether an 'open' anomaly needs a rationale, but FR-164 and the amended Description use 'carried' (not closed, or closed as `wont-fix`). Say 'carried'. | spec/functional/FR-016-anomaly-release-rationale.md:40 |

## Dispositions

| FND | Outcome | Reason |
| --- | --- | --- |
| FND-001 | fixed | Fixed in f5b30a4; after-text: - The closed-status rule SHALL apply only to a `resolution` present and in the FR-014 vocabulary, so a `closed` anomaly with no `resolution`, or one outside it, yields the finding FR-014 reports and no finding for the section. `AnomalyFields.json` SHALL encode the rule with a condition that requires `resolution` to be present and one of those three values, so that it does not hold vacuously on an absent key. |
| FND-002 | fixed | Fixed in f5b30a4; after-text: - The module SHALL ship, as fixtures for the criteria below, valid `impacting` anomalies at `identified`, `assessed` and `resolved` that carry the section, each with a counterpart identical but for the section (AC-10), and a valid `closed` `wont-fix` anomaly that carries a `closed_by` and the section. |
| FND-003 | fixed | Fixed in f5b30a4; after-text: - The emitted record schema `Anomaly.json` SHALL state the same rules for the mapped record: the `releaseRationale` entry shape, the non-empty and placeholder rules for `author` and `rationale`, and the closed-status rule. |
| FND-004 | fixed | Fixed in f5b30a4; after-text: - The `closed_by` of the shipped `closed` `wont-fix` fixture SHALL differ from the `Author` of every row of its section, so that a reader can tell the typed rationale author from the closer (quoin FR-163-AC-4). |
| FND-005 | fixed | Fixed in f5b30a4; after-text: - The `Anomaly` archetype SHALL declare a `release_rationale` locator (`required: false`) for the section in its `yield_pattern.match`, and `AnomalyFields.json` carries the section rules over that property. / FR-014: and `safetyImpact`, each a `frontmatter` mapping carried verbatim, and the keys `assessment`, `verification` and `releaseRationale` |
| FND-006 | fixed | Fixed in f5b30a4; after-text: title: "Anomaly release rationale: a human-authored, named reason for releasing with an anomaly not fixed" |
| FND-007 | fixed | Fixed in e3e4bb8; after-text: - The module SHALL ship, as fixtures for the criteria below, valid `impacting` anomalies at `identified`, `assessed` and `resolved` that carry the section, each with a counterpart identical but for the section (AC-10), and a valid `impacting` `closed` `wont-fix` anomaly that carries a `closed_by` and the section, with a counterpart identical but for the section (quoin FR-164-AC-5). |
| FND-008 | fixed | Fixed in e3e4bb8; after-text: ([FR-015](./FR-015-anomaly-safety-impact-assessment.md) for the first two, [FR-016](./FR-016-anomaly-release-rationale.md) for `releaseRationale`). The key `statusHistory` is not / - **Downstream**: [FR-015](./FR-015-anomaly-safety-impact-assessment.md), [FR-016](./FR-016-anomaly-release-rationale.md); quoin [FR-136](ix://agent-ix/quoin/FR-136) (history-based transition check and record mapping) |
| FND-009 | fixed | Fixed in e3e4bb8; after-text: \| Whether a carried anomaly needs a rationale, and whether the rationale is the author's own \| Not this module: quoin FR-164 decides the first; the second is a person's attestation recorded by git, not a check \| |
