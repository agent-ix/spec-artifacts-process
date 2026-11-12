/**
 * Which files under schemas/ the generator owns (FR-009).
 *
 * A file here is hand-authored: it is neither emitted, removed, nor reported
 * stale. Everything else ending in `.json` is a projection.
 */

/** The hand-authored `record_validation` schemas of an extracted record (FR-014). */
export const HAND_AUTHORED = new Set(["AnomalyFields.json"]);

export function isProjection(name) {
  return (
    name.endsWith(".json") &&
    !name.endsWith("-frontmatter.schema.json") &&
    !HAND_AUTHORED.has(name)
  );
}
