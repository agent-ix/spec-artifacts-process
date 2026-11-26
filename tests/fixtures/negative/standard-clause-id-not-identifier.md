---
id: Standard-902
title: "negative — a clause id that is not an Identifier"
type: Standard
code: clause-id-not-identifier
expect: mapping.clause-id
because: "clauseId is a semantic-core Identifier — letters, digits and underscores, never a leading digit — because it becomes a name in every lowered target"
---
# Standard-902: negative — a clause id that is not an Identifier

## Invariants

### 1-not-an-identifier

This subsection intentionally has no formal clause.

### ValidClause

```ocl
context Standard
inv ValidClause:
  true
```
