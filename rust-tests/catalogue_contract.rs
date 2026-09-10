// SPDX-License-Identifier: AGPL-3.0-or-later
// Copyright (C) 2026 Agent-IX

//! Contract tests for the shared verification-method catalogue.

use std::collections::BTreeMap;

use ix_trace_rs::trace;
use serde::Deserialize;

const MANIFEST: &str = include_str!("../spec_artifacts_process/manifest.yaml");
const DIFFERENTIAL_DEFINITION: &str = "Execute the same exact input projection against two or more identified implementations or oracles, compare their structured observations through a declared relation, and limit agreement to that relation without inferring independence, correctness, general equivalence, or qualification.";

#[derive(Clone, Debug, Deserialize, Eq, PartialEq)]
struct Manifest {
    verification_catalog: BTreeMap<String, VerificationMethod>,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq)]
#[serde(deny_unknown_fields)]
struct VerificationMethod {
    name: String,
    class: String,
    definition: String,
    evidence_kind: String,
    applicability: BTreeMap<String, Vec<String>>,
    tooling: Vec<String>,
}

fn expected() -> VerificationMethod {
    VerificationMethod {
        name: "Differential testing".to_owned(),
        class: "Test".to_owned(),
        definition: DIFFERENTIAL_DEFINITION.to_owned(),
        evidence_kind: "Property".to_owned(),
        applicability: BTreeMap::from([(
            "characteristics".to_owned(),
            vec!["reference-equivalence".to_owned()],
        )]),
        tooling: vec!["proptest".to_owned(), "cargo test".to_owned()],
    }
}

#[trace("TC-144", "FR-007-AC-15", "FR-007-CON-1")]
#[test]
fn tc_144_differential_method_has_one_exact_declarative_contract() {
    let manifest: Manifest = yaml_serde::from_str(MANIFEST).expect("manifest must be valid YAML");
    assert_eq!(manifest.verification_catalog.len(), 34);
    assert_eq!(
        manifest.verification_catalog.get("differential-testing"),
        Some(&expected())
    );
}

#[trace("TC-144", "FR-007-AC-15", "FR-007-CON-1")]
#[test]
fn tc_144_each_identity_bearing_field_discriminates() {
    let manifest: Manifest = yaml_serde::from_str(MANIFEST).expect("manifest must be valid YAML");
    let actual = manifest
        .verification_catalog
        .get("differential-testing")
        .expect("differential-testing must be declared");
    let expected = expected();

    let mut changed_name = expected.clone();
    changed_name.name.push_str(" changed");
    let mut changed_class = expected.clone();
    changed_class.class = "Analysis".to_owned();
    let mut changed_definition = expected.clone();
    changed_definition.definition = "Compare one execution with itself.".to_owned();
    let mut changed_evidence_kind = expected.clone();
    changed_evidence_kind.evidence_kind = "Integration".to_owned();
    let mut changed_applicability = expected.clone();
    changed_applicability.applicability.clear();
    let mut changed_tooling = expected.clone();
    changed_tooling.tooling.reverse();

    for (field, changed) in [
        ("name", changed_name),
        ("class", changed_class),
        ("definition", changed_definition),
        ("evidence_kind", changed_evidence_kind),
        ("applicability", changed_applicability),
        ("tooling", changed_tooling),
    ] {
        assert_ne!(changed, expected, "mutation of {field} was not observable");
        assert_ne!(actual, &changed, "manifest accepted the {field} mutation");
    }
}
