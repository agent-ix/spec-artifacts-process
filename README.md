# spec-artifacts-process

> Filament Module: process artifact templates (ADR, Plan, Track, Task, Review, Finding, TestMatrix, Standard) — Jinja .md.j2 templates

Agent-IX Filament module loaded by [`quire-cli`](https://github.com/agent-ix/quire-cli) and [`quoin`](https://github.com/agent-ix/quoin).

## Installing quire-cli

`@agent-ix` packages are published to public npm. Install the CLI globally:

```bash
npm install -g @agent-ix/quire-cli
```

See https://github.com/agent-ix/quire-cli#install for details.

## Install this module via npm

This module is also published as a config-only npm package: `@agent-ix/spec-artifacts-process`.
The package root **is** the Filament module (`manifest.yaml` + schemas/skeletons),
so it works directly as a `--module` target or via quoin's `package:` source.

```bash
npm install @agent-ix/spec-artifacts-process
```

```bash
# quoin — resolve the module from npm by name
quoin plugin install package:@agent-ix/spec-artifacts-process

# or point any tool at the installed package root
quire validate spec/**/*.md --module node_modules/@agent-ix/spec-artifacts-process
```

## Artifact types provided

| Kind | ID pattern | Description |
|------|------------|-------------|
| ADR | `ADR-{next:03d}` | Architecture Decision Record capturing a decision, its context and consequences; moves through `proposed → accepted → superseded → rejected` states and links via `supersedes`/`superseded_by`/`relates_to`/`depends_on`. |
| Plan | `Plan-{next:03d}` | An implementation plan that owns member Tracks and/or Tasks (expected artifacts `Track`, `Task`); links via `contains`/`depends_on`/`references`. |
| Track | `TRK-{next:03d}` | A first-class node between Plan and Task that groups related Tasks into a parallelizable workstream (expected artifact `Task`); enables a Spec → Plan → Track → Task hierarchy. Links via `contains`/`depends_on`/`references`. |
| Task | `Task-{next:03d}` | A single unit of implementation work; links via `depends_on`/`verifies`/`references`. Retains an optional legacy `track:` string field (superseded by the nodal `Track`). |
| Review | `Review-{next:03d}` | A review document that owns a set of member Findings (expected artifact `Finding`); top-level nav item, links via `reviews`/`references`. |
| Finding | `Finding-{next:03d}` | An individual review finding/issue; links via `found_in`/`blocks`/`references`. |
| TestMatrix | `TestMatrix-{next:03d}` | A requirement-to-test coverage matrix; links via `covers`/`references`. |
| Standard | `Standard-{next:03d}` | A normative standard definition with a stable `code` slug, description and application guidance; links via `references`. |

All artifacts share the `process-artifacts` grammar and require `id`, `title`, and `type` frontmatter; Standard additionally requires `code`.

### Object type: `standard`

The module also exposes a `standard` object type. It extracts a stable `code` slug (required), optional `name`/`link` frontmatter, a `description` from the **Description** section body, and a `guide` from the **Application Guidance** section body. These objects are referenced from spec frontmatter `standards_alignment[]`.

## How this module is used

### With quoin (recommended)

```bash
quoin plugin install path:../spec-artifacts-process
quoin catalog list
quoin catalog show ADR
quoin write . --types ADR,Plan
quoin review
```

See https://github.com/agent-ix/quoin.

### With quire-cli directly

```bash
quire schema ADR --module ./spec_artifacts_process
quire validate spec/**/*.md --module ./spec_artifacts_process
quire extract <DOC> --module ./spec_artifacts_process --archetype ADR
```

See https://github.com/agent-ix/quire-cli#usage-instructions.

## Development

- **Library:** `spec_artifacts_process` (flat layout, Python 3.13+, [Poetry](https://python-poetry.org/))
- **Build & CI:** GitHub Actions; dynamic Git-tag-based versioning; published to Google Artifact Registry via `twine upload -r internal-pypi`.

```bash
make install          # install dependencies in Poetry venv
make test             # run pytest
make lint             # ruff + black check
make format           # ruff + black format
make build            # build wheel and sdist under dist/
make update-lock      # update poetry.lock
make use-local p=<name>     # switch dep to local pypi.ix
make use-upstream p=<name>  # switch dep back to upstream
make local-publish    # build and publish to local pypi.ix
```

Required CI secrets/variables: `GCP_SERVICE_ACCOUNT_KEY`, `GCP_REGION`, `GCP_PROJECT_NAME`, `GCP_PYPI`.
