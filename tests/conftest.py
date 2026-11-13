"""Shared fixtures for the module's test suite.

Two policies are enforced here and nowhere else:

* **The engine is a hard dependency of the semantic rows.** ``quire`` is a dev
  dependency resolved from ``internal-pypi`` (``poetry install``). When it is
  absent the semantic tests **fail**; they never skip, because a skipped row is
  not coverage.
* **The emitted schemas are read from the committed tree**, and every ``$ref``
  resolves locally — module models from ``spec_artifacts_process/schemas/`` and
  grammar models from the ``@agent-ix/semantic-core`` the pinned toolchain
  installs — so a record test validates against the real bytes.
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
from typing import Any

import pytest
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
PACKAGE_ROOT = REPO_ROOT / "spec_artifacts_process"
MANIFEST_PATH = PACKAGE_ROOT / "manifest.yaml"
SCHEMAS_DIR = PACKAGE_ROOT / "schemas"
SKELETONS_DIR = PACKAGE_ROOT / "skeletons"
EXAMPLES_DIR = PACKAGE_ROOT / "examples"
MAPPINGS_PATH = PACKAGE_ROOT / "mappings.yaml"
MAPPINGS_SCHEMA_PATH = PACKAGE_ROOT / "mappings.schema.json"
SEMANTIC_DIR = PACKAGE_ROOT / "semantic"
NEGATIVE_DIR = REPO_ROOT / "tests" / "fixtures" / "negative"
SEMANTIC_CORE_DIR = (
    SEMANTIC_DIR
    / "node_modules"
    / "@agent-ix"
    / "semantic-core"
    / "generated"
    / "json-schema"
)

QUIRE_MISSING = (
    "the Quire wheel exposing the semantic surface is not installed in this "
    "environment. Run `poetry install` (quire is a dev dependency from "
    "internal-pypi). The semantic tests fail rather than skip, because a "
    "skipped row is not coverage."
)

sys.path.insert(0, str(REPO_ROOT / "tests"))

from support.strict_yaml import load_yaml_strict  # noqa: E402


def pytest_sessionstart(session: pytest.Session) -> None:
    """Expose semantic npm tools, including quire, to CLI integration tests."""
    bin_dir = SEMANTIC_DIR / "node_modules" / ".bin"
    if bin_dir.is_dir():
        os.environ["PATH"] = f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}"


#: The installed filament modules the CLI rows load beside this module: the
#: `FR`/`NFR` archetypes (spec-artifacts-iso) and the realizing verb with the
#: design relations (spec-objects-architecture).
MODULES_ROOT = pathlib.Path(
    os.environ.get("IX_FILAMENT_MODULES_PATH")
    or pathlib.Path.home() / ".ix" / "filament" / "modules"
)


def ix_module(name: str) -> str:
    """Directory of the installed sibling module `name`, or fail the row."""
    path = MODULES_ROOT / name
    assert (path / "manifest.yaml").is_file(), (
        f"{name} is not installed under {MODULES_ROOT} (set "
        "IX_FILAMENT_MODULES_PATH); the rows that load it fail rather than "
        "skip, because a skipped row is not coverage. The sibling modules "
        "spec-artifacts-iso and spec-objects-architecture must be installed; "
        "spec-objects-architecture must be a release that declares "
        "`realizes_requirement` (its FR-010)."
    )
    return str(path)


def run_quire(
    *args: str, siblings: tuple[str, ...] = ()
) -> subprocess.CompletedProcess:
    """Run `quire <args>` with the named sibling modules and this module loaded."""
    assert shutil.which("quire"), (
        "the `quire` CLI is not on PATH; run `make semantic-install` (it installs "
        "the quire-cli the semantic package pins, which loads the manifest "
        "keys). The row fails rather than skips."
    )
    modules: list[str] = []
    for name in siblings:
        modules += ["--module", ix_module(name)]
    modules += ["--module", str(PACKAGE_ROOT)]
    return subprocess.run(
        ["quire", *args, *modules], capture_output=True, text=True, check=False
    )


def load_manifest() -> dict[str, Any]:
    return load_yaml_strict(MANIFEST_PATH.read_text())


MODULE_BASE = "https://schemas.agent-ix.org/agent-ix/spec-artifacts-process/"
SEMANTIC_CORE_VERSION = json.loads((SEMANTIC_DIR / "package.json").read_text())[
    "dependencies"
]["@agent-ix/semantic-core"]
SEMANTIC_CORE_BASE = (
    f"https://schemas.agent-ix.org/semantic-core/{SEMANTIC_CORE_VERSION}/"
)


def artifact_type_names() -> list[str]:
    """The declared types, enumerated from the manifest (FR-009-CON-6).

    A hard-coded list silently stops covering the type added after it was
    written, which is the whole reason this helper exists.
    """
    return [at["name"] for at in load_manifest()["artifact_types"]]


def frontmatter(markdown: str) -> dict[str, Any]:
    match = re.match(r"---\n(.*?)\n---\n", markdown, re.DOTALL)
    assert match, "document has no frontmatter"
    return yaml.safe_load(match.group(1))


def require_quire():
    """Import quire, or fail the test naming the provisioning path."""
    try:
        import quire
    except ImportError as error:  # pragma: no cover - environment guard
        pytest.fail(f"{QUIRE_MISSING} (import error: {error})")
    for surface in ("Registry", "validate_document"):
        if not hasattr(quire, surface):  # pragma: no cover - environment guard
            pytest.fail(
                f"`{surface}` is missing from the installed quire: {QUIRE_MISSING}"
            )
    return quire


@pytest.fixture(scope="session")
def quire_engine():
    return require_quire()


@pytest.fixture(scope="session")
def manifest() -> dict[str, Any]:
    return load_manifest()


@pytest.fixture(scope="session")
def semantic_block(manifest: dict[str, Any]) -> dict[str, Any]:
    return manifest["semantic"]


@pytest.fixture(scope="session")
def mappings() -> dict[str, Any]:
    return yaml.safe_load(MAPPINGS_PATH.read_text())


@pytest.fixture(scope="session")
def mapper(mappings: dict[str, Any], manifest: dict[str, Any]):
    from support.reference_mapping import ReferenceMapper

    return ReferenceMapper(mappings, manifest)


@pytest.fixture(scope="session")
def skeletons() -> list[pathlib.Path]:
    return sorted(SKELETONS_DIR.glob("*.md"))


@pytest.fixture(scope="session")
def schema_registry():
    """A 2020-12 validator factory over the shipped schemas plus semantic-core.

    Every `$ref` resolves locally: module models from the committed `schemas/`
    directory, grammar models from the semantic-core package the pinned toolchain
    installs.
    """
    from referencing import Registry, Resource

    if not SEMANTIC_CORE_DIR.is_dir():  # pragma: no cover - environment guard
        pytest.fail(
            "@agent-ix/semantic-core is not installed, so `$ref`s to the grammar "
            "cannot resolve. Run `make semantic-install` (FR-009-CON-2: `@agent-ix` "
            "resolves from the user-level npm config, never from a repo .npmrc)."
        )
    resources = []
    for path in sorted(SCHEMAS_DIR.glob("*.json")):
        if path.name.endswith("-frontmatter.schema.json"):
            continue
        schema = json.loads(path.read_text())
        resources.append((schema["$id"], Resource.from_contents(schema)))
    for path in sorted(SEMANTIC_CORE_DIR.glob("*.json")):
        schema = json.loads(path.read_text())
        uri = schema.get("$id") or f"{SEMANTIC_CORE_BASE}{path.name}"
        resources.append((uri, Resource.from_contents(schema)))
    registry = Registry().with_resources(resources)

    def validator_for(model: str):
        from jsonschema import Draft202012Validator

        schema = json.loads((SCHEMAS_DIR / f"{model}.json").read_text())
        return Draft202012Validator(schema, registry=registry)

    return validator_for
