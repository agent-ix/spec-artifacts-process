"""The emitted JSON Schema bundle and its drift gate (requirement FR-009).

TC-080..TC-088 and TC-132..TC-134.

Every assertion that quantifies over "all declared types" enumerates them from
the manifest or from the emitted bundle (FR-009-CON-6). A hard-coded list stops
covering the type added after it was written, which is the failure this rule
exists to prevent.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from conftest import (
    MANIFEST_PATH,
    PACKAGE_ROOT,
    REPO_ROOT,
    SCHEMAS_DIR,
    SEMANTIC_DIR,
    TOOLCHAIN_PATH,
    artifact_type_names,
    load_manifest,
    manifest_version,
    module_base,
)

SEMANTIC_CORE_BASE = "https://schemas.agent-ix.org/semantic-core/0.3.0/"


def toolchain() -> dict:
    return json.loads(TOOLCHAIN_PATH.read_text())


def projections() -> list[Path]:
    return sorted(
        p
        for p in SCHEMAS_DIR.glob("*.json")
        if not p.name.endswith("-frontmatter.schema.json")
    )


def run_generator(
    args: list[str], env_overlay: dict | None = None, cwd: Path | None = None
):
    import os

    env = dict(os.environ)
    env.update(env_overlay or {})
    return subprocess.run(
        [sys.executable and "node", "scripts/generate.mjs", *args],
        cwd=str(cwd or SEMANTIC_DIR),
        capture_output=True,
        text=True,
        env=env,
    )


@pytest.fixture()
def sandbox(tmp_path: Path) -> Path:
    """A throwaway copy of the semantic package and the module, so a test may
    mutate a tree without touching the checkout. `node_modules` is symlinked
    rather than copied: it is 100 MB and read-only for these tests."""
    module = tmp_path / "spec_artifacts_process"
    module.mkdir()
    for name in ("manifest.yaml",):
        shutil.copy(PACKAGE_ROOT / name, module / name)
    shutil.copytree(SCHEMAS_DIR, module / "schemas")
    semantic = module / "semantic"
    semantic.mkdir()
    for name in ("main.tsp", "tspconfig.yaml", "package.json"):
        shutil.copy(SEMANTIC_DIR / name, semantic / name)
    shutil.copytree(SEMANTIC_DIR / "scripts", semantic / "scripts")
    shutil.copytree(SEMANTIC_DIR / "generated", semantic / "generated")
    (semantic / "node_modules").symlink_to(SEMANTIC_DIR / "node_modules")
    return semantic


@pytest.mark.trace("TC-080")
def test_bundle_is_exactly_what_the_toolchain_lists():
    record = toolchain()
    on_disk = sorted(p.name for p in projections())
    assert sorted(record["files"]) == on_disk
    assert record["compiler"] == {"name": "@typespec/compiler", "version": "1.15.0"}
    assert record["emitter"] == {"name": "@typespec/json-schema", "version": "1.15.0"}
    for name in artifact_type_names():
        assert f"{name}.json" in on_disk, f"no emitted model for declared type {name}"


@pytest.mark.trace("TC-081")
def test_every_projection_declares_the_versioned_id():
    base = module_base()
    assert manifest_version() in base
    for path in projections():
        schema = json.loads(path.read_text())
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert schema["$id"] == f"{base}{path.name}"


@pytest.mark.trace("TC-082")
def test_every_ref_resolves_to_a_sibling_or_to_semantic_core():
    base = module_base()
    shipped = {p.name for p in projections()}
    for path in projections():
        for ref in re.findall(r'"\$ref":\s*"([^"]+)"', path.read_text()):
            if ref.startswith(SEMANTIC_CORE_BASE):
                continue
            assert ref.startswith(base), f"{path.name} refs a foreign host: {ref}"
            assert (
                ref[len(base) :] in shipped
            ), f"{path.name} refs a missing sibling: {ref}"


@pytest.mark.trace("TC-083")
def test_check_is_clean_and_fails_on_one_changed_byte(sandbox: Path):
    assert run_generator(["--check"], cwd=sandbox).returncode == 0
    victim = sandbox.parent / "schemas" / "SpecReview.json"
    original = victim.read_text()
    victim.write_text(original.replace("SpecReview", "SpecReviewX", 1))
    result = run_generator(["--check"], cwd=sandbox)
    assert result.returncode == 1
    assert "SpecReview.json" in result.stderr
    assert (
        victim.read_text() != original
    ), "--check must not rewrite the file it reports"


@pytest.mark.trace("TC-084")
def test_a_base_version_that_disagrees_with_the_manifest_fails(sandbox: Path):
    source = sandbox / "main.tsp"
    source.write_text(source.read_text().replace(f"/{manifest_version()}/", "/9.9.9/"))
    result = run_generator([], cwd=sandbox)
    assert result.returncode != 0
    assert "9.9.9" in result.stderr and manifest_version() in result.stderr


@pytest.mark.trace("TC-085")
def test_a_stale_projection_is_named_and_frontmatter_schemas_are_left_alone(
    sandbox: Path,
):
    schemas = sandbox.parent / "schemas"
    stale = schemas / "Stale.json"
    stale.write_text("{}\n")
    frontmatter = sorted(schemas.glob("*-frontmatter.schema.json"))
    assert frontmatter, "the hand-authored frontmatter schemas must be present"
    before = {p.name: p.read_text() for p in frontmatter}
    result = run_generator(["--check"], cwd=sandbox)
    assert result.returncode == 1
    assert "Stale.json" in result.stderr
    for name in before:
        assert "frontmatter" not in result.stderr.replace(name, "")
        assert (schemas / name).read_text() == before[name]


@pytest.mark.trace("TC-086")
def test_the_wheel_and_the_npm_tree_carry_every_projection():
    subprocess.run(
        ["make", "build"], cwd=str(REPO_ROOT), check=True, capture_output=True
    )
    wheels = sorted((REPO_ROOT / "dist").glob("*.whl"))
    assert wheels, "make build produced no wheel"
    import zipfile

    with zipfile.ZipFile(wheels[-1]) as archive:
        names = set(archive.namelist())
    for path in projections():
        assert f"spec_artifacts_process/schemas/{path.name}" in names
    assert "spec_artifacts_process/manifest.yaml" in names
    assert "spec_artifacts_process/mappings.yaml" in names


@pytest.mark.trace("TC-087")
def test_two_runs_are_byte_identical(sandbox: Path):
    first = run_generator([], cwd=sandbox)
    assert first.returncode == 0, first.stderr
    snapshot = {
        p.name: p.read_bytes() for p in (sandbox.parent / "schemas").glob("*.json")
    }
    toolchain_bytes = (sandbox / "generated" / "toolchain.json").read_bytes()
    second = run_generator([], cwd=sandbox)
    assert second.returncode == 0, second.stderr
    assert {
        p.name: p.read_bytes() for p in (sandbox.parent / "schemas").glob("*.json")
    } == snapshot
    assert (sandbox / "generated" / "toolchain.json").read_bytes() == toolchain_bytes


@pytest.mark.trace("TC-088")
def test_toolchain_pins_semantic_core_by_bytes():
    record = toolchain()["semanticCore"]
    assert record["name"] == "@agent-ix/semantic-core"
    assert record["version"] == load_manifest()["semantic"]["semantic_core"]
    assert re.fullmatch(r"sha256:[0-9a-f]{64}", record["toolchainDigest"])
    installed = (
        SEMANTIC_DIR / "node_modules/@agent-ix/semantic-core/generated/toolchain.json"
    )
    import hashlib

    expected = f"sha256:{hashlib.sha256(installed.read_bytes()).hexdigest()}"
    assert record["toolchainDigest"] == expected


@pytest.mark.trace("TC-132")
def test_a_missing_toolchain_names_the_component_and_the_install(tmp_path: Path):
    """No `node_modules` at all: the generator must say which component is
    missing and how to install it, rather than failing inside the compiler."""
    module = tmp_path / "spec_artifacts_process"
    module.mkdir()
    shutil.copy(MANIFEST_PATH, module / "manifest.yaml")
    semantic = module / "semantic"
    semantic.mkdir()
    for name in ("main.tsp", "tspconfig.yaml", "package.json"):
        shutil.copy(SEMANTIC_DIR / name, semantic / name)
    shutil.copytree(SEMANTIC_DIR / "scripts", semantic / "scripts")
    (semantic / "generated").mkdir()
    result = run_generator([], cwd=semantic)
    assert result.returncode != 0
    assert "make semantic-install" in result.stderr
    assert "semantic-core" in result.stderr or "tsp" in result.stderr


@pytest.mark.trace("TC-133")
def test_a_semantic_core_version_disagreement_names_both(sandbox: Path):
    manifest = sandbox.parent / "manifest.yaml"
    manifest.write_text(
        re.sub(
            r"^  semantic_core: .*$",
            "  semantic_core: 9.9.9",
            manifest.read_text(),
            flags=re.M,
        )
    )
    result = run_generator([], cwd=sandbox)
    assert result.returncode != 0
    assert "9.9.9" in result.stderr and "0.3.0" in result.stderr


@pytest.mark.trace("TC-134")
def test_a_stale_version_segment_fails_even_when_internally_consistent(sandbox: Path):
    """Schemas and digests that agree with each other but were generated against
    a different manifest version must not pass by being internally consistent."""
    manifest = sandbox.parent / "manifest.yaml"
    old = manifest_version()
    manifest.write_text(
        manifest.read_text().replace(f"version: {old}", "version: 0.3.0", 1)
    )
    result = run_generator(["--check"], cwd=sandbox)
    assert result.returncode != 0
    assert "0.3.0" in result.stderr
