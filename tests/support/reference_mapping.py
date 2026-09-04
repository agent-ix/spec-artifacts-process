"""Reference implementation of the FR-011 Markdown record mapping.

This is the oracle the suite uses to prove that the shipped `mappings.yaml`, the
emitted JSON Schemas and the authored skeletons agree with each other. It is not
module code and nothing in the published package imports it.

It is **strict** by contract: any reported error means no record is built, and
every error found in one document is reported in one pass. A partial record whose
missing properties are indistinguishable from absent ones is the failure that
rule removes (FR-011).
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MappingError:
    """One defect, naming the model, the property and the 1-based line."""

    model: str
    prop: str
    reason: str
    line: int
    detail: str = ""

    def __str__(self) -> str:  # pragma: no cover - diagnostics only
        head = f"{self.model}.{self.prop}:{self.line}"
        return f"{head}: {self.reason} {self.detail}".rstrip()


class MappingFailure(Exception):
    """Raised when a document cannot be mapped. Carries every error of one pass."""

    def __init__(self, errors: list[MappingError]) -> None:
        self.errors = errors
        super().__init__("; ".join(str(e) for e in errors))

    @property
    def reasons(self) -> list[str]:
        return [e.reason for e in self.errors]


# ---------------------------------------------------------------------------
# Document primitives
# ---------------------------------------------------------------------------

FRONTMATTER = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)
STATUS_MARKERS = ("✅", "❌", "🚧", "⛔")
FENCE = re.compile(r"^```(?P<lang>[A-Za-z0-9_-]*)\s*$")


def normalise(text: str) -> str:
    """CRLF (and lone CR) to LF, before anything is sliced.

    The digest is taken over these bytes, so one document has one digest whatever
    the checkout did to its line endings (FR-011-AC-13).
    """
    return text.replace("\r\n", "\n").replace("\r", "\n")


def digest_of(text: str) -> str:
    return f"sha256:{hashlib.sha256(normalise(text).encode('utf-8')).hexdigest()}"


@dataclass
class Document:
    text: str
    path: str
    source_identity: str | None = None
    frontmatter: dict[str, Any] = field(default_factory=dict)
    lines: list[str] = field(default_factory=list)
    body_start: int = 1

    @classmethod
    def parse(
        cls, text: str, path: str, source_identity: str | None = None
    ) -> "Document":
        text = normalise(text)
        match = FRONTMATTER.match(text)
        front: dict[str, Any] = {}
        if match:
            front = yaml.safe_load(match.group("body")) or {}
        lines = text.split("\n")
        body_start = text[: match.end()].count("\n") + 1 if match else 1
        return cls(text, path, source_identity, front, lines, body_start)

    def heading_span(self, heading: str) -> tuple[int, int] | None:
        """1-based inclusive span of a named section's *content*, fences respected.

        The level is not part of the contract: the manifest locators name the
        heading TEXT, and the matrix coverage tables sit at H3 under
        `## Requirements Traceability` while every other asserted section is H2.
        A section ends at the next heading of the same level or shallower.
        """
        start = None
        level = 0
        in_fence = False
        for index, line in enumerate(self.lines, start=1):
            if FENCE.match(line.strip()):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            stripped = line.strip()
            if start is None:
                for candidate in (2, 3):
                    if stripped == f"{'#' * candidate} {heading}":
                        start, level = index + 1, candidate
                        break
                continue
            hashes = len(line) - len(line.lstrip("#"))
            if (
                line.startswith("#")
                and 0 < hashes <= level
                and line[hashes : hashes + 1] == " "
            ):
                return (start, index - 1)
        if start is None:
            return None
        return (start, len(self.lines))

    def slice(self, span: tuple[int, int]) -> str:
        return "\n".join(self.lines[span[0] - 1 : span[1]]).strip("\n")

    def whole_body(self) -> tuple[str, int, int]:
        start = self.body_start + 1
        return "\n".join(self.lines[start - 1 :]).strip("\n"), start, len(self.lines)


def split_row(line: str) -> list[str]:
    """Split a Markdown table row, treating `\\|` as a literal pipe (FR-011-AC-12)."""
    cells: list[str] = []
    current = ""
    escaped = False
    for char in line.strip():
        if escaped:
            current += char if char == "|" else "\\" + char
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == "|":
            cells.append(current)
            current = ""
            continue
        current += char
    cells.append(current)
    if cells and cells[0].strip() == "":
        cells = cells[1:]
    if cells and cells[-1].strip() == "":
        cells = cells[:-1]
    return [c.strip() for c in cells]


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c) for c in cells)


# ---------------------------------------------------------------------------
# Cell parses
# ---------------------------------------------------------------------------

TRACE_TOKEN = re.compile(
    r"^(?P<prefix>[A-Za-z]+)-(?P<num>\d+)(?:-(?P<sub>[A-Za-z]+)-(?P<subnum>\d+(?:/\d+)*))?$"
)
CONTINUATION = re.compile(r"^-(?P<sub>[A-Za-z]+)-(?P<subnum>\d+(?:/\d+)*)$")
NOTE = re.compile(r"\s*\((?P<note>[^)]*)\)\s*$")


def parse_status(cell: str) -> dict[str, str] | None:
    """Split the leading marker from the note that says why."""
    text = cell.strip()
    for marker in STATUS_MARKERS:
        if text.startswith(marker):
            note = text[len(marker) :].strip()
            return {"marker": marker, "note": note} if note else {"marker": marker}
    return None


def parse_traces(cell: str) -> dict[str, Any] | None:
    """Expand the two authoring shorthands; map a lone `-` to the no-trace form."""
    text = cell.strip()
    if text == "-":
        return {"tokens": [], "noTrace": True}
    note = None
    match = NOTE.search(text)
    if match:
        note = match.group("note").strip()
        text = text[: match.start()].strip()
    tokens: list[str] = []
    parent: str | None = None
    for raw in text.split(","):
        item = raw.strip()
        if not item:
            return None
        cont = CONTINUATION.match(item)
        if cont:
            if parent is None:
                return None
            for part in cont.group("subnum").split("/"):
                tokens.append(f"{parent}-{cont.group('sub')}-{part}")
            continue
        base = TRACE_TOKEN.match(item)
        if not base:
            return None
        parent = f"{base.group('prefix')}-{base.group('num')}"
        if base.group("sub"):
            for part in base.group("subnum").split("/"):
                tokens.append(f"{parent}-{base.group('sub')}-{part}")
        else:
            tokens.append(parent)
    if not tokens:
        return None
    out: dict[str, Any] = {"tokens": tokens, "noTrace": False}
    if note:
        out["note"] = note
    return out


# ---------------------------------------------------------------------------
# The mapper
# ---------------------------------------------------------------------------

SYSML_ATTR = re.compile(
    r"^\s*(?:attribute|ref item|item)\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*:\s*"
    r"(?P<type>[A-Za-z_][A-Za-z0-9_]*)\s*\[(?P<mult>[^\]]*)\]\s*(?:\{(?P<constraints>[^}]*)\})?\s*$"
)
IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class ReferenceMapper:
    """Builds one record from one document, per `mappings.yaml`."""

    def __init__(self, mappings: dict[str, Any], manifest: dict[str, Any]) -> None:
        self.mappings = mappings
        self.manifest = manifest
        self._locators = {
            at["name"]: (
                (at.get("body_extraction") or {}).get("yield_pattern") or {}
            ).get("match")
            or {}
            for at in manifest["artifact_types"]
        }

    # -- locator helpers ---------------------------------------------------

    def _assert_for(self, model: str, heading: str) -> dict[str, Any]:
        """The manifest assert whose section is `heading`, so a parse is checked
        against the contract rather than against this file's own opinion."""
        archetype = self.mappings["models"][model]["archetype"]
        for locator in self._locators.get(archetype, {}).values():
            if (
                locator.get("under_section") == heading
                or locator.get("after_heading") == heading
            ):
                return locator.get("assert") or {}
        return {}

    # -- entry point -------------------------------------------------------

    def build(
        self, model: str, text: str, path: str, source_identity: str | None = None
    ) -> dict[str, Any]:
        spec = self.mappings["models"][model]
        doc = Document.parse(text, path, source_identity)
        errors: list[MappingError] = []
        record: dict[str, Any] = {}
        for prop, entry in spec["properties"].items():
            try:
                value = self._one(model, prop, entry, doc, errors)
            except MappingFailure as failure:
                errors.extend(failure.errors)
                continue
            if value is not None:
                record[prop] = value
            elif entry.get("required"):
                errors.append(MappingError(model, prop, "missing", doc.body_start))
        if errors:
            raise MappingFailure(errors)
        return record

    def dropped_keys(self, model: str, text: str) -> list[str]:
        spec = self.mappings["models"][model]
        named = {
            tuple(e["path"])[0]
            for e in spec["properties"].values()
            if e["kind"] in ("frontmatter", "list") and e.get("path")
        }
        front = Document.parse(text, "<memory>").frontmatter
        return sorted(k for k in front if k not in named)

    # -- per-kind ----------------------------------------------------------

    def _one(self, model, prop, entry, doc, errors):
        kind = entry["kind"]
        if kind == "frontmatter":
            return self._frontmatter(entry, doc)
        if kind == "list":
            return self._list(entry, doc)
        if kind == "provenance":
            return self._provenance(doc)
        if kind == "section":
            return self._section(model, prop, entry, doc, errors)
        if kind in ("table", "typed-table"):
            return self._table(model, prop, entry, doc, errors)
        if kind == "ocl-clause":
            return self._clauses(model, prop, entry, doc, errors)
        raise AssertionError(f"unhandled mapping kind {kind}")  # pragma: no cover

    def _frontmatter(self, entry, doc):
        value: Any = doc.frontmatter
        for key in entry["path"]:
            if not isinstance(value, dict) or key not in value:
                return None
            value = value[key]
        return value

    def _list(self, entry, doc):
        raw = self._frontmatter(entry, doc)
        if raw is None:
            return None
        if isinstance(raw, list):
            return [str(item).strip() for item in raw]
        return [
            part.strip() for part in str(raw).split(entry["separator"]) if part.strip()
        ]

    def _provenance(self, doc):
        out = {"path": doc.path, "digest": digest_of(doc.text)}
        if doc.source_identity:
            out["sourceIdentity"] = doc.source_identity
        return out

    # `model`, `prop` and `errors` are unused here and are part of the uniform
    # per-kind signature `_one` dispatches on: a section either exists or does
    # not, and its absence is reported by the caller against the entry's
    # `required` flag rather than here. Dropping them would make the dispatcher
    # branch on kind twice.
    def _section(self, model, prop, entry, doc, errors):
        if entry.get("whole_body"):
            text, start, end = doc.whole_body()
            return {"text": text, "startLine": start, "endLine": end}
        span = doc.heading_span(entry["heading"])
        if span is None:
            return None
        return {"text": doc.slice(span), "startLine": span[0], "endLine": span[1]}

    # -- tables ------------------------------------------------------------

    def _table(self, model, prop, entry, doc, errors):
        heading = entry["heading"]
        span = doc.heading_span(heading)
        if span is None:
            return None
        header_index = None
        for index in range(span[0], span[1] + 1):
            line = doc.lines[index - 1]
            if line.lstrip().startswith("|"):
                header_index = index
                break
        if header_index is None:
            return None
        header = split_row(doc.lines[header_index - 1])
        declared = list(entry.get("columns") or [])
        if declared:
            optional = set(entry.get("optional_columns") or [])
            expected = [c for c in declared if c in header or c not in optional]
            if header != expected:
                errors.append(
                    MappingError(
                        model, prop, "columns", header_index, f"{header} != {expected}"
                    )
                )
                return None
        rows: list[dict[str, Any]] = []
        seen: dict[str, int] = {}
        for index in range(header_index + 1, span[1] + 1):
            line = doc.lines[index - 1]
            if not line.lstrip().startswith("|"):
                if line.strip() == "":
                    continue
                break
            cells = split_row(line)
            if is_separator(cells):
                continue
            if len(cells) != len(header):
                errors.append(
                    MappingError(
                        model,
                        prop,
                        "row-arity",
                        index,
                        f"{len(cells)} != {len(header)}",
                    )
                )
                continue
            row = self._row(model, prop, entry, header, cells, index, errors)
            if row is None:
                continue
            id_column = entry.get("id_column")
            if id_column:
                key = str(row.get(entry["fields"][id_column]["property"]))
                if key in seen:
                    errors.append(
                        MappingError(
                            model,
                            prop,
                            "duplicate-row-id",
                            index,
                            f"{key} first at line {seen[key]}",
                        )
                    )
                    continue
                seen[key] = index
            rows.append(row)
        if not rows:
            errors.append(
                MappingError(model, prop, "min-rows", header_index, "0 data rows")
            )
            return None
        return rows

    def _row(self, model, prop, entry, header, cells, line, errors):
        asserts = self._assert_for(model, entry["heading"])
        row: dict[str, Any] = {"line": line}
        ok = True
        open_columns = entry.get("open_columns")
        for column, cell in zip(header, cells):
            spec = entry["fields"].get(column)
            if spec is None:
                if open_columns:
                    # The locator asserts no column list, so the header is the
                    # author's. Carrying the cells by header keeps every byte
                    # rather than dropping the columns this module cannot name.
                    row.setdefault(open_columns, {})[column] = cell
                    continue
                errors.append(
                    MappingError(model, prop, "unmapped-column", line, column)
                )
                ok = False
                continue
            name, parse = spec["property"], spec["parse"]
            if cell == "" and column in set(entry.get("optional_columns") or []):
                continue
            if parse == "text":
                if cell == "":
                    continue
                row[name] = cell
            elif parse == "id":
                pattern = asserts.get("id_pattern")
                if pattern and not re.fullmatch(pattern, cell):
                    errors.append(MappingError(model, prop, "id-pattern", line, cell))
                    ok = False
                    continue
                row[name] = cell
            elif parse == "enum":
                choices = (asserts.get("column_choices") or {}).get(column)
                if choices is not None and cell not in choices:
                    errors.append(
                        MappingError(
                            model, prop, "column-choices", line, f"{column}={cell!r}"
                        )
                    )
                    ok = False
                    continue
                row[name] = cell
            elif parse == "status-marker":
                parsed = parse_status(cell)
                if parsed is None:
                    errors.append(
                        MappingError(model, prop, "status-marker", line, cell)
                    )
                    ok = False
                    continue
                row[name] = parsed
            elif parse == "trace-tokens":
                parsed = parse_traces(cell)
                if parsed is None:
                    errors.append(MappingError(model, prop, "trace-tokens", line, cell))
                    ok = False
                    continue
                row[name] = parsed
            else:  # pragma: no cover - the schema closes the vocabulary
                raise AssertionError(parse)
        return row if ok else None

    # -- typed declarations and clauses ------------------------------------

    def declarations(self, model: str, text: str) -> list[dict[str, Any]]:
        """`## Properties` as either the typed table or the `sysml` fence.

        One artifact carries one form; a document with both is `both-forms` and
        no record is built.
        """
        spec = self.mappings["models"][model]["properties"]["properties"]
        doc = Document.parse(text, "<memory>")
        heading = spec["heading"]
        span = doc.heading_span(heading)
        if span is None:
            return []
        body = doc.slice(span)
        has_table = any(line.lstrip().startswith("|") for line in body.split("\n"))
        fence = self._sysml_fence(doc, span)
        if has_table and fence is not None:
            raise MappingFailure(
                [MappingError(model, "properties", "both-forms", span[0])]
            )
        if fence is not None:
            return self._from_sysml(model, fence, span[0])
        errors: list[MappingError] = []
        rows = self._table(model, "properties", spec, doc, errors)
        if errors:
            raise MappingFailure(errors)
        return [self._to_field(model, row, row["line"]) for row in (rows or [])]

    def _sysml_fence(self, doc, span):
        inside = False
        collected: list[str] = []
        for index in range(span[0], span[1] + 1):
            line = doc.lines[index - 1]
            match = FENCE.match(line.strip())
            if match and not inside and match.group("lang") == "sysml":
                inside = True
                continue
            if match and inside:
                return collected
            if inside:
                collected.append(line)
        return None

    def _from_sysml(self, model, lines, line_no):
        out = []
        for raw in lines:
            if not raw.strip():
                continue
            match = SYSML_ATTR.match(raw)
            if not match:
                raise MappingFailure(
                    [
                        MappingError(
                            model,
                            "properties",
                            "sysml-declaration",
                            line_no,
                            raw.strip(),
                        )
                    ]
                )
            out.append(
                self._to_field(
                    model,
                    {
                        "name": match.group("name"),
                        "type": match.group("type"),
                        "multiplicity": match.group("mult").strip(),
                        "constraints": (match.group("constraints") or "").strip(),
                    },
                    line_no,
                )
            )
        return out

    def _to_field(self, model, row, line):
        """One typed declaration as a semantic-core `FieldDecl`."""
        lower, _, upper = row["multiplicity"].partition("..")
        multiplicity: dict[str, Any] = {"lower": int(lower)}
        if upper and upper != "*":
            multiplicity["upper"] = int(upper)
        raw = [
            c.strip() for c in (row.get("constraints") or "").split(",") if c.strip()
        ]
        identity = "identity" in raw
        constraints: list[dict[str, Any]] = []
        for item in raw:
            if item == "identity":
                continue
            keyword, _, value = item.partition(":")
            keyword, value = keyword.strip(), value.strip()
            if keyword == "pattern":
                constraints.append(
                    {"keyword": "pattern", "regex": value, "dialect": "ecma-262"}
                )
            elif keyword in ("minLength", "maxLength", "min", "max"):
                constraints.append({"keyword": keyword, "value": int(value)})
            elif keyword == "format":
                constraints.append({"keyword": "format", "name": f"ix:{value}"})
            elif keyword == "nonEmpty":
                constraints.append({"keyword": "nonEmpty"})
            else:
                raise MappingFailure(
                    [
                        MappingError(
                            model, "properties", "unknown-constraint", line, item
                        )
                    ]
                )
        decl: dict[str, Any] = {
            "name": row["name"],
            "type": {"target": row["type"], "multiplicity": multiplicity},
        }
        if identity:
            decl["identity"] = True
        if constraints:
            decl["constraints"] = constraints
        return decl

    def _clauses(self, model, prop, entry, doc, errors):
        span = doc.heading_span(entry["heading"])
        if span is None:
            return None
        clauses: list[dict[str, str]] = []
        seen: set[str] = set()
        current: str | None = None
        fences_here = 0
        open_fence = False
        for index in range(span[0], span[1] + 1):
            line = doc.lines[index - 1]
            if line.startswith("### "):
                current = line[4:].strip()
                fences_here = 0
                if not IDENTIFIER.match(current):
                    errors.append(
                        MappingError(model, prop, "clause-id", index, current)
                    )
                    current = None
                elif current in seen:
                    errors.append(
                        MappingError(model, prop, "duplicate-clause-id", index, current)
                    )
                    current = None
                continue
            match = FENCE.match(line.strip())
            if not match:
                continue
            if open_fence:
                open_fence = False
                continue
            if match.group("lang") != entry.get("language", "ocl"):
                continue
            open_fence = True
            if current is None:
                errors.append(MappingError(model, prop, "orphan-fence", index))
                continue
            fences_here += 1
            if fences_here > 1:
                errors.append(MappingError(model, prop, "second-fence", index, current))
                continue
            seen.add(current)
            clauses.append({"language": "ocl", "clauseId": current})
        if open_fence:
            errors.append(MappingError(model, prop, "unterminated-fence", span[1]))
        return clauses or None
