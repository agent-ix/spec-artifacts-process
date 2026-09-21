import "@typespec/json-schema";
import "@agent-ix/semantic-core";

using TypeSpec.JsonSchema;
using AgentIx.Semantic.Core;

/**
 * Semantic data models of the spec-artifacts-process module (FR-009, ticket
 * agent-ix/spec-artifacts-process#78).
 *
 * One model per declared process artifact type. Each model is the typed form of
 * the record the archetype's `body_extraction` locators already extract, plus
 * the frontmatter identity, relationships and provenance. The Markdown is the
 * authority and the record is a derived projection (FR-011).
 *
 * Every model describes an **authored definition** or an **authored evidence
 * act** (FR-013). None carries a run identifier, a run timestamp, a duration, a
 * pass/fail count, a log location or a run artefact: those belong to the
 * evidence store, whose schemas are owned by Engineering Assurance and quoin.
 *
 * Every scalar pattern and every enum below is copied from
 * `spec_artifacts_process/manifest.yaml`, which is the single source. A value
 * this file admits that the manifest does not is a defect in this file.
 */
@jsonSchema("https://schemas.agent-ix.org/agent-ix/spec-artifacts-process/0.2.0/")
namespace AgentIx.SpecArtifactsProcess;

// ---------------------------------------------------------------------------
// Scalars
// ---------------------------------------------------------------------------

/** A non-empty string; the base of every prose cell and every name. */
@minLength(1)
scalar NonEmptyText extends string;

/**
 * Document id of the artifact types whose frontmatter schema pins
 * `^[A-Z]{2,4}-[0-9]+$` — ADR, Review, SpecReview, Finding, Feedback,
 * TestMatrix, TestMatrixIndex, SuiteRegistry and Inspections.
 */
@pattern("^[A-Z]{2,4}-[0-9]+$")
scalar UpperDocId extends string;

/**
 * Document id of `Plan` and `Task`, whose frontmatter schemas pin
 * `^[A-Za-z]{2,4}-[0-9]+$` — the minted forms are `Plan-001` and `Task-001`,
 * which are mixed case and would fail the upper-only pattern.
 */
@pattern("^[A-Za-z]{2,4}-[0-9]+$")
scalar MixedDocId extends string;

/** `Standard` document id; its frontmatter schema pins `^[A-Za-z]{2,}-[0-9]+$` (no upper bound on the prefix length). */
@pattern("^[A-Za-z]{2,}-[0-9]+$")
scalar StandardDocId extends string;

/** A findings ROW id inside a SpecReview (`FND-1`). Deliberately not the `Finding` document namespace, which is `FIND-` (FR-008, FR-013). */
@pattern("^FND-[0-9]+$")
scalar FindingRowId extends string;

/** A cross-module integration scenario id in a TestMatrixIndex (`INT-1`). */
@pattern("^INT-[0-9]+$")
scalar IntegrationId extends string;

/** A knowingly-uncovered coverage-gap id in a TestMatrixIndex (`GAP-1`). */
@pattern("^GAP-[0-9]+$")
scalar GapId extends string;

/** A suite id in a SuiteRegistry. Structured, doc-scoped and never renumbered: everything joins on it. */
@pattern("^SUITE-[0-9]+$")
scalar SuiteId extends string;

/** An inspection-act id in an Inspections record. */
@pattern("^INSP-[0-9]+$")
scalar InspectionId extends string;

/**
 * A test-case row id. The segmented forms the ecosystem authors (`TC-060-01`,
 * `TC-SB-001`, `IT-001-HEADER-PARSE`) are legal; the prefix set is `TC` and `IT`
 * because those are the only two artifact types any module mints test ids for
 * (CR-019). Copied verbatim from the manifest's `id_pattern`.
 */
@pattern("^(TC|IT)(-[A-Za-z0-9]+)*-[0-9]+[A-Za-z0-9]*(-[A-Za-z0-9]+)*$")
scalar TestRowId extends string;

/**
 * A status marker: exactly the four the manifest admits.
 *
 * `⚠️` is absent and stays absent. CR-031 retired it because
 * `traceability.status` classed it as nothing, so `class_of` returned `Unknown`
 * and every row carrying it was exempt from the status-lie check by
 * construction (quire-rs CR-083). The `quoin:spec-matrix` skill still documents
 * it as valid; the skill is the defect (agent-ix/quoin#337), not this pattern.
 */
enum StatusMarker {
  complete: "✅",
  failed: "❌",
  inProgress: "🚧",
  retired: "⛔",
}

/**
 * Test-case type. The same fourteen values as `traceability.vocabularies.test_type`,
 * the TestMatrix `Type` column and the SuiteRegistry `Evidence Kind` column —
 * CR-015's one vocabulary, three uses, restated a fourth time because
 * `from_vocabulary` does not exist yet (quire-rs#146). The manifest test keeps
 * every copy honest.
 */
enum TestType {
  Unit,
  Integration,
  E2E,
  Property,
  Fuzz,
  Benchmark,
  Static,
  Compile,
  Snapshot,
  Manual,
  Eval,
  Inspection,
  Analysis,
  Demonstration,
}

/** Test-case priority; the manifest's `column_choices.Priority`. */
enum Priority {
  P0,
  P1,
  P2,
  P3,
  P4,
}

/** Finding severity: how urgently to look. Orthogonal to `EscapeCause`. */
enum Severity {
  low,
  medium,
  high,
}

/**
 * Which layer let a defect through (FR-008). Orthogonal to `Severity`, and the
 * only axis that answers the question. The fourth value is the one to watch: the
 * only cause that does not indict the specification, and the only one a green
 * Test Matrix would have called healthy.
 */
enum EscapeCause {
  missingRequirement: "missing-requirement",
  wrongRequirement: "wrong-requirement",
  correctRequirementNoEvidence: "correct-requirement-no-evidence",
  implementationBugDespiteEvidence: "implementation-bug-despite-evidence",
}

/** The verdict of one inspection act. */
enum Verdict {
  Pass,
  Fail,
  Waived,
}

/** The analysis a SpecReview carries; the enum its frontmatter schema declares. */
enum AnalysisKind {
  base,
  failureDomain: "failure-domain",
  integrity,
  dependency,
  evidence,
  riskComplexity: "risk-complexity",
  scopeBoundary: "scope-boundary",
  gapAnalysis: "gap-analysis",
  earsConformance: "ears-conformance",
  architectureEvaluation: "architecture-evaluation",
  criterionStrength: "criterion-strength",
  codeReview: "code-review",
  specCorrectness: "spec-correctness",
}

/** How much of the spec a SpecReview covered. */
enum ReviewSet {
  base,
  all,
  subset,
}

/** Feedback thread lifecycle. Anchor resolution is computed at load time and is not part of the record. */
enum FeedbackStatus {
  open,
  addressed,
  resolved,
}

/** A free-form passage comment, or a decision on a review finding. */
enum FeedbackKind {
  comment,
  triage,
}

/** The decision a `triage` feedback records. */
enum FeedbackDecision {
  Fix,
  Dismiss,
  Defer,
}

/** ADR lifecycle, from the `adr` archetype's declared `composition.states`. */
enum AdrState {
  proposed,
  accepted,
  superseded,
  rejected,
}

/** A relationship verb from the module's `allowed_links` registries. */
@pattern("^[a-z][a-z0-9_]*$")
scalar EdgeVerb extends string;

/** A relationship target: an `ix://` identity, as every frontmatter schema requires. */
@pattern("^ix://.+$")
scalar IxTarget extends string;

/** Relationship cardinality as authored (`1:1`, `1:N`, `0..1`); each side is a number, a letter token, or `*`, optionally a `..` range. */
@pattern("^[0-9A-Za-z*]+(\\.\\.[0-9A-Za-z*]+)?(:[0-9A-Za-z*]+(\\.\\.[0-9A-Za-z*]+)?)?$")
scalar Cardinality extends string;

/** SHA-256 over the document bytes, `sha256:<64 hex>`. */
@pattern("^sha256:[0-9a-f]{64}$")
scalar Sha256Digest extends string;

/** A 1-based document line number. */
@minValue(1)
scalar LineNumber extends int32;

/** A relative link target (`./tests.md`, `modules/api/tests.md`); never a scheme, because a matrix link is local navigation. */
@pattern("^(\\./|\\.\\./)*[^:/][^:]*$")
scalar RelativeHref extends string;

/** An object-type name from frontmatter `object:`. */
@pattern("^[a-z][a-z0-9_]*$")
scalar ObjectTypeName extends string;

/** A `Standard` code: the stable slug referenced from spec frontmatter `standards_alignment[]`. */
@pattern("^[a-z0-9][a-z0-9.-]*$")
scalar StandardCode extends string;

/** A commit reference as authored in an inspection record: an abbreviated or full hex sha. */
@pattern("^[0-9a-f]{7,40}$")
scalar CommitRef extends string;

/**
 * One trace reference token as the `Traces To` cell writes it, after the two
 * authoring shorthands are expanded: `FR-001`, `FR-001-AC-2`, `IT-003-SC-01`.
 * The kind prefix is deliberately not enumerated — the legal set follows from
 * the declared trace targets and existence is checked by reference resolution.
 */
@pattern("^[A-Za-z]+-[0-9]+(-[A-Za-z]+-[0-9]+)?$")
scalar TraceToken extends string;

// ---------------------------------------------------------------------------
// Shared models
// ---------------------------------------------------------------------------

/** One level-2 section as the `section` mapping yields it: byte-exact content and its document lines. */
model Section {
  /** free text: authored prose; sentence grammar is the advisory EARS lens, not a schema. */
  text: string;
  startLine: LineNumber;
  endLine: LineNumber;
}

/** Where the record came from. */
model Provenance {
  /** Repository-relative path of the document. */
  path: NonEmptyText;
  /** `ix://<org>/<repo>/spec` when the caller supplies one; absent otherwise. */
  sourceIdentity?: SemanticId;
  /** SHA-256 over the line-ending-normalised document bytes (FR-011). */
  digest: Sha256Digest;
}

/**
 * One frontmatter `relationships[]` entry, sealed to the three keys every
 * frontmatter schema in this module admits. An annotation key an author adds
 * cannot reach a sealed model; the `frontmatter` mapping drops it and lists it
 * as dropped, so the loss is declared rather than silent.
 */
model Relationship {
  target: IxTarget;
  type: EdgeVerb;
  cardinality?: Cardinality;
}

/**
 * A status cell split by the `typed-table` mapping: the leading marker and the
 * note that says why. `🚧 scale evidence deferred` is `marker: 🚧`,
 * `note: "scale evidence deferred"`; a bare marker carries no `note`.
 */
model CoverageStatus {
  marker: StatusMarker;
  /** free text: the authored reason, verbatim, so no byte of the cell is dropped. */
  note?: string;
}

/**
 * A `Traces To` cell after the mapping expands its two shorthands. `noTrace` is
 * the explicit `-` form a retired row writes: severing the edge is precisely the
 * act of retiring, and an empty list with no flag would be indistinguishable
 * from a cell nobody filled in.
 */
model TraceCell {
  tokens: TraceToken[];
  noTrace: boolean;
  /** free text: a trailing parenthesised remark, verbatim. */
  note?: string;
}

/** One `## Findings` row of a SpecReview (`ID | Severity | Summary | Refs | Escape Cause`). */
model FindingRow {
  id: FindingRowId;
  severity: Severity;
  /** free text: the one-line finding. */
  summary: NonEmptyText;
  /** free text: what the finding points at; the column is prose and the census admits ids, paths and `-`. */
  refs: NonEmptyText;
  /** Absent when the analysis did not classify the escape, which the archetype makes optional. */
  escapeCause?: EscapeCause;
  line: LineNumber;
}

/** One `## Test Case Summary` row (`Test ID | Title | Type | Priority | Traces To | Status`). */
model TestCaseRow {
  id: TestRowId;
  /** free text: the row title. */
  title: NonEmptyText;
  type: TestType;
  /** Absent where the matrix omits the whole column, which the archetype allows (CR-018); never synthesised. */
  priority?: Priority;
  tracesTo: TraceCell;
  status: CoverageStatus;
  line: LineNumber;
}

/** One `### Functional Requirement Coverage` row (`Functional Req | Acceptance Criteria | Test Cases | Status`). */
model FunctionalCoverageRow {
  /** free text: the requirement cell as authored. */
  functionalReq: NonEmptyText;
  /** free text: the criteria cell; ranges and elisions are authored here and are not expanded. */
  acceptanceCriteria: NonEmptyText;
  /** free text: the test-case cell. */
  testCases: NonEmptyText;
  status: CoverageStatus;
  line: LineNumber;
}

/** One `### Stakeholder Requirement Coverage` row. */
model StakeholderCoverageRow {
  /** free text: the stakeholder requirement cell. */
  stakeholderReq: NonEmptyText;
  /** free text: the US/FR trace cell. */
  traceToUsFr: NonEmptyText;
  /** free text: the test or validation cell. */
  testValidation: NonEmptyText;
  status: CoverageStatus;
  line: LineNumber;
}

/** One `### User Story Coverage` row. */
model UserStoryCoverageRow {
  /** free text: the user story cell. */
  userStory: NonEmptyText;
  /** free text: the criteria cell. */
  acceptanceCriteria: NonEmptyText;
  /** free text: the test-case cell. */
  testCases: NonEmptyText;
  status: CoverageStatus;
  line: LineNumber;
}

/** One `### Non-Functional Requirement Coverage` row. */
model NonFunctionalCoverageRow {
  /** free text: the non-functional requirement cell. */
  nonFunctionalReq: NonEmptyText;
  /** free text: the verification method in the author's words; the closed catalog lives in `verification_catalog`, and this column is prose. */
  verificationMethod: NonEmptyText;
  /** free text: the evidence or test-case cell. */
  evidence: NonEmptyText;
  status: CoverageStatus;
  line: LineNumber;
}

/** One `## Requirements Traceability` row of a TestMatrixIndex: a subsystem and where its detail lives. */
model SubsystemIndexRow {
  /** free text: the subsystem name. */
  subsystem: NonEmptyText;
  /** free text: the requirement range this subsystem owns. */
  requirements: NonEmptyText;
  /** The relative link that makes the matrix tree navigable; asserting it is what makes a dropped cell visible. */
  localMatrix: RelativeHref;
  status: CoverageStatus;
  line: LineNumber;
}

/** One `## Integration Test Matrix` row of a TestMatrixIndex. */
model IntegrationMatrixRow {
  id: IntegrationId;
  /** free text: what the integration is for. */
  purpose: NonEmptyText;
  /** free text: the external system or component. */
  target: NonEmptyText;
  /** free text: the integration kind (`service`, `browser`, `event`, `database`); the column has no declared vocabulary. */
  type: NonEmptyText;
  /** free text: the test-case cell. */
  testCases: NonEmptyText;
  status: CoverageStatus;
  line: LineNumber;
}

/**
 * One `## Coverage Gaps` row: the register of what is knowingly uncovered.
 *
 * The locator asserts an id column and no column list, so the header belongs to
 * the author. `cells` carries every other authored cell by column name rather
 * than dropping the columns this module has no contract to name.
 */
model CoverageGapRow {
  id: GapId;
  cells: Record<string>;
  line: LineNumber;
}

/** One `## Suites` row of a SuiteRegistry: the atomic unit of evidence. */
model SuiteRow {
  id: SuiteId;
  /** free text: the suite name. */
  name: NonEmptyText;
  /** free text: the command that runs the suite, verbatim. */
  command: NonEmptyText;
  /** free text: the tool; an adapter-fed kind needs no vocabulary entry, because the kind column stays method-class-shaped. */
  tool: NonEmptyText;
  /** The same vocabulary as the TestMatrix `Type` column — one vocabulary, three uses. */
  evidenceKind: TestType;
  line: LineNumber;
}

/**
 * One `## Inspections` row: a human evidence act for a method that produces no
 * source symbol. Who performed it, against which commit, with what verdict — the
 * record *is* the evidence, and it is authored, never transcribed from a run.
 */
model InspectionRow {
  id: InspectionId;
  /** free text: the obligation id or statement the act discharges. */
  obligation: NonEmptyText;
  /** free text: who performed the inspection. */
  who: NonEmptyText;
  commit: CommitRef;
  verdict: Verdict;
  /** Absent when the author omitted the optional column; never synthesised. */
  note?: string;
  line: LineNumber;
}

/** The exact selected text of a feedback anchor, with context for disambiguation (W3C TextQuoteSelector style). */
model TextSelector {
  quote: NonEmptyText;
  /** free text: preceding context. */
  prefix?: string;
  /** free text: following context. */
  suffix?: string;
}

/** A structural feedback locator that survives prose rewrites. */
model BlockSelector {
  /** free text: the owning requirement or criterion id, e.g. `FR-003-AC-2`. */
  requirementId?: string;
  /** Ordered heading trail to the block. */
  headingPath?: string[];
  @minValue(0) blockIndex?: int32;
}

/**
 * Where a feedback thread attaches. Resolution is text-primary, block-fallback:
 * prefer the quote; if it is gone fall back to the block; if that is gone the
 * thread is orphaned and is never silently re-pointed.
 */
model FeedbackAnchor {
  /** free text: a repository-relative path or an `ix://` reference. */
  artifact: NonEmptyText;
  text?: TextSelector;
  block?: BlockSelector;
}

// ---------------------------------------------------------------------------
// Artifact models (exported)
// ---------------------------------------------------------------------------

/** Architecture decision record (archetype `ADR`). A definition: it records a decision, never a run. */
model ADR {
  id: UpperDocId;
  title: NonEmptyText;
  type: "ADR";
  object?: ObjectTypeName;
  state?: AdrState;
  /** Absent when the author declared none; the frontmatter schemas do not require the key, and the model must not require what the schema does not (FR-011-AC-15). */
  relationships?: Relationship[];
  provenance: Provenance;
  /** free text: the whole authored body; the archetype declares no `body_extraction`, so no section is asserted. */
  body: Section;
}

/**
 * Plan record (archetype `Plan`). The authored plan: its scope, its tracks and
 * its gates. It carries nothing about an execution of that plan — no start, no
 * finish, no outcome (FR-013).
 */
model Plan {
  id: MixedDocId;
  title: NonEmptyText;
  type: "Plan";
  object?: ObjectTypeName;
  /** free text: the authored lifecycle word (`active`, `done`); the archetype declares no vocabulary for it. */
  status?: NonEmptyText;
  /** Absent when the author declared none; the frontmatter schemas do not require the key, and the model must not require what the schema does not (FR-011-AC-15). */
  relationships?: Relationship[];
  provenance: Provenance;
  /** free text: the whole authored body; the archetype declares no `body_extraction`. */
  body: Section;
}

/**
 * Task record (archetype `Task`). The authored unit of work: its track, its
 * dependencies and the tests it verifies. Not a record of the task being done.
 */
model Task {
  id: MixedDocId;
  title: NonEmptyText;
  type: "Task";
  object?: ObjectTypeName;
  /** free text: the authored lifecycle word (`todo`, `done`); the archetype declares no vocabulary for it. */
  status?: NonEmptyText;
  /** The parallel-execution track label (FR-005). A property of a Task; a consumer needing a tree node synthesises one. */
  track?: NonEmptyText;
  /** Absent when the author declared none; the frontmatter schemas do not require the key, and the model must not require what the schema does not (FR-011-AC-15). */
  relationships?: Relationship[];
  provenance: Provenance;
  /** free text: the whole authored body; the archetype declares no `body_extraction`. */
  body: Section;
}

/** Freeform review record (archetype `Review`), the parent of `Finding` documents. */
model Review {
  id: UpperDocId;
  title: NonEmptyText;
  type: "Review";
  object?: ObjectTypeName;
  /** Absent when the author declared none; the frontmatter schemas do not require the key, and the model must not require what the schema does not (FR-011-AC-15). */
  relationships?: Relationship[];
  provenance: Provenance;
  /** free text: the whole authored body; the archetype declares no `body_extraction`. */
  body: Section;
}

/**
 * Validated per-analysis review record (archetype `SpecReview`). One document
 * per analysis skill. The findings stay queryable from the review that raised
 * them and grounded in the artifacts they name (FR-013).
 */
model SpecReview {
  id: UpperDocId;
  title: NonEmptyText;
  type: "SpecReview";
  analysis?: AnalysisKind;
  /** The spec paths or ids reviewed, one entry per authored path. */
  scope?: NonEmptyText[];
  reviewSet?: ReviewSet;
  object?: ObjectTypeName;
  /** Absent when the author declared none; the frontmatter schemas do not require the key, and the model must not require what the schema does not (FR-011-AC-15). */
  relationships?: Relationship[];
  provenance: Provenance;
  summary: Section;
  @minItems(1) findings: FindingRow[];
}

/**
 * Finding document (archetype `Finding`), a child of `Review`. Deliberately a
 * different id namespace from the `FND-` rows inside a SpecReview: the document
 * and the row are different things, and one prefix would read as unification.
 */
model Finding {
  id: UpperDocId;
  title: NonEmptyText;
  type: "Finding";
  object?: ObjectTypeName;
  /** Absent when the author declared none; the frontmatter schemas do not require the key, and the model must not require what the schema does not (FR-011-AC-15). */
  relationships?: Relationship[];
  provenance: Provenance;
  /** free text: the whole authored body; the archetype declares no `body_extraction`, because nothing authors one today. */
  body: Section;
}

/** Review-thread feedback record (archetype `Feedback`). */
model Feedback {
  id: UpperDocId;
  title: NonEmptyText;
  type: "Feedback";
  status: FeedbackStatus;
  kind: FeedbackKind;
  /** Meaningful only when `kind` is `triage`. */
  decision?: FeedbackDecision;
  anchor: FeedbackAnchor;
  object?: ObjectTypeName;
  /** Absent when the author declared none; the frontmatter schemas do not require the key, and the model must not require what the schema does not (FR-011-AC-15). */
  relationships?: Relationship[];
  provenance: Provenance;
  comment: Section;
}

/**
 * Root matrix record (archetype `TestMatrixIndex`, CR-039). A repository past a
 * certain size does not have one matrix; it has a tree, and this is the root.
 * It mints no test-case id, because `trace_targets.test-case` binds `TestMatrix`
 * and this is not one.
 */
model TestMatrixIndex {
  id: UpperDocId;
  title: NonEmptyText;
  type: "TestMatrixIndex";
  object?: ObjectTypeName;
  /** Absent when the author declared none; the frontmatter schemas do not require the key, and the model must not require what the schema does not (FR-011-AC-15). */
  relationships?: Relationship[];
  provenance: Provenance;
  @minItems(1) subsystemIndex: SubsystemIndexRow[];
  /** Optional: a repository whose subsystems do not integrate has none, and requiring the table would force an empty one. */
  @minItems(1) integrationMatrix?: IntegrationMatrixRow[];
  /** Optional: an absent register and an empty one are different claims, and only the second is authored. */
  @minItems(1) coverageGaps?: CoverageGapRow[];
}

/**
 * Leaf matrix record (archetype `TestMatrix`). Every `Status` marker is the
 * **authored coverage claim**, never an execution result; whether the claim is
 * true is decided by the coverage rollup against the evidence store, outside
 * this module (FR-013).
 */
model TestMatrix {
  id: UpperDocId;
  title: NonEmptyText;
  type: "TestMatrix";
  object?: ObjectTypeName;
  /** Absent when the author declared none; the frontmatter schemas do not require the key, and the model must not require what the schema does not (FR-011-AC-15). */
  relationships?: Relationship[];
  provenance: Provenance;
  @minItems(1) functionalCoverage: FunctionalCoverageRow[];
  @minItems(1) testCases: TestCaseRow[];
  /** Optional: a bundle with no StR artifacts cannot truthfully populate it. */
  stakeholderCoverage?: StakeholderCoverageRow[];
  /** Optional, for the same reason. */
  userStoryCoverage?: UserStoryCoverageRow[];
  /** Optional, for the same reason. */
  nonFunctionalCoverage?: NonFunctionalCoverageRow[];
}

/**
 * Standard record (archetype `Standard`): the stable definition a spec's
 * `standards_alignment[]` points at.
 *
 * The one type in this module that carries a typed declaration, because a
 * standard declares the properties a conforming artifact carries and the
 * invariants conformance requires. Both sections are optional, so every
 * Standard document that validates today keeps validating (FR-012).
 */
model Standard {
  id: StandardDocId;
  title: NonEmptyText;
  type: "Standard";
  code: StandardCode;
  /** free text: the frontmatter summary of what the standard defines. */
  description?: string;
  /** free text: frontmatter application guidance. */
  guide?: string;
  /** free text: the canonical URL; the frontmatter schema declares `format: uri` and no pattern. */
  link?: string;
  object?: ObjectTypeName;
  /** Absent when the author declared none; the frontmatter schemas do not require the key, and the model must not require what the schema does not (FR-011-AC-15). */
  relationships?: Relationship[];
  provenance: Provenance;
  /** The typed `## Properties` declarations, authored as the table or as the `sysml` fence — one artifact carries one form. */
  @minItems(1) properties?: FieldDecl[];
  /** Formal clauses from an optional `## Invariants` section; clause text is carried beside the record, never parsed. */
  @minItems(1) invariants?: ClauseRef[];
}

/**
 * Suite registry record (archetype `SuiteRegistry`). An **evidence act**, not a
 * definition and not a run: it declares which suites exist, what runs them and
 * what kind of evidence they produce, and declares nothing about any particular
 * execution (FR-013).
 */
model SuiteRegistry {
  id: UpperDocId;
  title: NonEmptyText;
  type: "SuiteRegistry";
  provenance: Provenance;
  @minItems(1) suites: SuiteRow[];
}

/**
 * Inspection record (archetype `Inspections`). An **evidence act**: the
 * authored record of inspection and analysis, the methods that produce no
 * source symbol and so can never be discharged by a test run. A human performed
 * the act, and the record of who, when and against which commit *is* the
 * evidence (FR-013).
 */
model Inspections {
  id: UpperDocId;
  title: NonEmptyText;
  type: "Inspections";
  provenance: Provenance;
  @minItems(1) inspections: InspectionRow[];
}
