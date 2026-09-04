---
id: Standard-900
title: "negative — a Standard carrying both declaration forms"
type: Standard
code: both-forms
expect: mapping.both-forms
because: "one artifact carries one form; two forms under one heading are two claims about the same declarations and nothing says which wins"
---
# Standard-900: negative — a Standard carrying both declaration forms

## Properties

| Field | Type | Multiplicity | Constraints |
|-------|------|--------------|-------------|
| code | String | 1..1 | identity |

```sysml
attribute code : String[1..1] { identity }
```
