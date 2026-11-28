---
type: how-to
description: "Record an observed anomaly, assess its impact, and document its disposition."
tool_versions: "Quoin 0.38.2; Quire 0.53.5; Process module v0.38.0"
---

# How to handle an anomaly

Use an anomaly record to track an observed difference between expected and actual behavior through assessment, repair, and release disposition.

## Steps

1. Run `quoin module ensure-defaults`. Set `PROCESS_MODULE` to the installed Process module directory from `quoin module list`, then copy its `Anomaly` skeleton into the repository's `spec/anomalies/` directory:

```bash
mkdir -p spec/anomalies
cp "$PROCESS_MODULE/skeletons/Anomaly.md" spec/anomalies/AN-001.md
```

`PROCESS_MODULE` is the installed module directory that contains `manifest.yaml`. Give the record a unique ID and describe what happened, where it happened, and what behavior was expected.

For example:

```markdown
| Kind | Target | Impact | Rationale |
|---|---|---|---|
| Requirement | FR-014-AC-2 | Affects | Import returned success before the digest check completed. |
```

Assign severity as a person's assessment. The impact table records the supporting rationale.

3. For a fixed anomaly, set `status: resolved` and `resolution: fixed`. Add a Fix Verification row naming the criterion or test that confirms the repair.

For an anomaly released without a fix, add a Release Rationale row with the author's name and reason. A closed anomaly also names the person who closed it.

4. From the repository root, validate the document with the Process module:

```bash
quire validate spec/anomalies/AN-001.md --module "$PROCESS_MODULE"
```

Quire reports structural errors such as a missing severity or an incomplete assessment table. Check status transitions against Git history with `quoin anomaly check spec/anomalies` before closing the record.

## Result

The anomaly validates with its impact assessment and disposition present. The history check confirms each status transition in Git.
