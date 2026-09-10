---
id: SR-024
title: "Rust review — differential verification catalogue contract"
type: SpecReview
analysis: code-review
scope: "Cargo.toml, Cargo.lock, rust-toolchain.toml, rust-tests/catalogue_contract.rs, spec_artifacts_process/manifest.yaml"
review_set: subset
---
# SR-024: Rust review — differential verification catalogue contract

## Summary

Applied `/home/peter/dev/agent-skills/rust-review/SKILL.md` to the implemented
TC-144 portion of issue #86 at reviewed revision `5bc455e`. The review read the
repository conventions, Cargo metadata, the complete Rust acceptance target,
the authoritative manifest change, both manual-dispatch workflows and the full
diff from `origin/main`.

The implementation is a test-only Rust package pinned to Rust 1.98.1. It has one
explicit integration-test target and no empty library or public API. All three
tests carry bare compiler-checked `ix-trace-rs` attributes for TC-144,
FR-007-AC-15 and FR-007-CON-1. The target reads the committed manifest bytes,
checks the exact catalogue census and strict `differential-testing` entry, and
keeps strict decoding scoped to that entry so an accepted extension to an
unrelated method cannot falsify TC-144.

## Verdict

**PASS for the implemented TC-144 checkpoint.** No open Rust finding remains in
that checkpoint. This is not a pass for issue #86 as a whole: TC-145 and TC-146
remain blocked on the accepted typed Rust process-execution result from
`agent-ix/engineering-assurance#34`, and no PR is ready until they execute.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | medium | **Resolved.** The first test-local decoder applied a closed six-field `VerificationMethod` struct to every catalogue entry. Quire's accepted producer type also permits optional `cost`, so adding `cost` to an unrelated method made TC-144 fail before checking `differential-testing`. The decoder now retains unrelated entries as `yaml_serde::Value` and strictly decodes only B's entry. A mutation adding `cost: first-line` to `unit-testing` now proves the differential contract remains unchanged; it failed under the prior decoder. | rust-tests/catalogue_contract.rs:15, rust-tests/catalogue_contract.rs:44, rust-tests/catalogue_contract.rs:100 |
| FND-002 | low | **Resolved.** The package declared an empty library target with no API, caller or behavior. Cargo metadata now exposes only the acceptance test target. | Cargo.toml:1 |
| FND-003 | low | **Resolved.** `rust-version = "1.94"` stated only a minimum and no toolchain file fixed the compiler that produces the evidence. The package and `rust-toolchain.toml` now select 1.98.1; the reproduced gate reports rustc 1.98.1. | Cargo.toml:5, rust-toolchain.toml:1 |
| FND-004 | low | **Resolved.** Six QUOIN review artifacts ended with an extra blank line and made `git diff --check` red. The redundant lines were removed. | spec/reviews/86-differential-testing-catalog/ |

## Rust checks

- Idioms: no production error, wire, async, lock, lifecycle, integer-conversion,
  or resource-bound surface exists in this test-only target.
- Panic surface: `expect` occurs only in the test target while loading
  repository-controlled compile-time bytes; no `unwrap`, `panic!`, unchecked
  indexing, `unsafe`, `allow`, TODO, FIXME or debug macro exists in the Rust diff.
- Test seam: `include_str!` is appropriate because TC-144 verifies declarative
  manifest content. No runtime behavior was replaced with a double.
- Workflows: the change does not modify either workflow; both retain
  `workflow_dispatch` as their only trigger. No hosted workflow was dispatched.
- Dependency policy: this repository has no `deny.toml`, so the skill's
  conditional `cargo deny check` gate is not applicable to this checkpoint.

## Reproduced local gates

```text
cargo fmt --all -- --check
PASS

CARGO_BUILD_JOBS=1 CARGO_TARGET_DIR=/tmp/sap86-target \
  cargo clippy --locked --all-targets --all-features -- -D warnings
PASS (rustc 1.98.1)

CARGO_BUILD_JOBS=1 CARGO_TARGET_DIR=/tmp/sap86-target \
  cargo test --locked --all-targets
PASS: 3 passed; 0 failed; 0 ignored

cargo metadata --locked --no-deps --format-version 1
PASS: one test target; rust_version 1.98.1

git diff --check
PASS
```
