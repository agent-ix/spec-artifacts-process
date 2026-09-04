---
id: Standard-901
title: "negative — a clause subsection with no fence"
type: Standard
code: clause-without-fence
expect: mapping.orphan-fence
because: "a fence with no `### <clauseId>` heading of its own belongs to no clause, and a clause that is silently dropped reads as one that was never written"
---
# Standard-901: negative — a clause subsection with no fence

## Invariants

The fence below sits under the section with no clause heading of its own.

```ocl
context Standard
inv Unowned:
  true
```
