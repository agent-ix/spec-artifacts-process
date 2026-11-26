"""The emitted JSON Schema bundle and its drift gate (requirement FR-009).

TC-081..TC-087 and TC-132..TC-133.

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
    MODULE_BASE,
    PACKAGE_ROOT,
    REPO_ROOT,
    SCHEMAS_DIR,
    SEMANTIC_CORE_BASE,
    SEMANTIC_DIR,
)


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
    (semantic / "node_modules").symlink_to(SEMANTIC_DIR / "node_modules")
    return semantic


@pytest.mark.trace("TC-081", "FR-009-AC-2")
def test_every_projection_declares_the_id():
    base = MODULE_BASE
    for path in projections():
        schema = json.loads(path.read_text())
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert schema["$id"] == f"{base}{path.name}"


@pytest.mark.trace("TC-082", "FR-009-AC-3")
def test_every_ref_resolves_to_a_sibling_or_to_semantic_core():
    base = MODULE_BASE
    shipped = {p.name for p in projections()}
    for path in projections():
        for ref in re.findall(r'"\$ref":\s*"([^"]+)"', path.read_text()):
            if ref.startswith(SEMANTIC_CORE_BASE):
                continue
            assert ref.startswith(base), f"{path.name} refs a foreign host: {ref}"
            assert (
                ref[len(base) :] in shipped
            ), f"{path.name} refs a missing sibling: {ref}"


@pytest.mark.trace("TC-083", "FR-009-AC-4", "FR-018-AC-12", "TC-241")
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


@pytest.mark.trace("TC-085", "FR-009-AC-6")
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


@pytest.mark.trace("TC-086", "FR-009-AC-7")
def test_the_wheel_and_the_npm_tree_carry_every_projection(tmp_path: Path):
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

    # Exercise the actual prepack staging script in a throwaway package root.
    # The script copies the authoritative inner module beside package.json so
    # the tarball's manifest-relative schema paths resolve.
    staged_root = tmp_path / "npm-stage"
    staged_root.mkdir(parents=True)
    shutil.copy2(REPO_ROOT / "package.json", staged_root / "package.json")
    shutil.copytree(REPO_ROOT / "scripts", staged_root / "scripts")
    shutil.copytree(PACKAGE_ROOT, staged_root / "spec_artifacts_process")
    result = subprocess.run(
        ["node", "scripts/stage-npm.mjs"],
        cwd=str(staged_root),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert (staged_root / "manifest.yaml").read_bytes() == (
        staged_root / "spec_artifacts_process" / "manifest.yaml"
    ).read_bytes()
    staged_schemas = staged_root / "schemas"
    shipped_schemas = sorted(SCHEMAS_DIR.glob("*.json"))
    assert {p.name for p in staged_schemas.glob("*.json")} == {
        p.name for p in shipped_schemas
    }
    for path in shipped_schemas:
        assert (staged_schemas / path.name).read_bytes() == path.read_bytes()


@pytest.mark.trace("TC-087", "FR-009-AC-8", "FR-009-CON-3")
def test_two_runs_are_byte_identical(sandbox: Path):
    first = run_generator([], cwd=sandbox)
    assert first.returncode == 0, first.stderr
    snapshot = {
        p.name: p.read_bytes() for p in (sandbox.parent / "schemas").glob("*.json")
    }
    second = run_generator([], cwd=sandbox)
    assert second.returncode == 0, second.stderr
    assert {
        p.name: p.read_bytes() for p in (sandbox.parent / "schemas").glob("*.json")
    } == snapshot


@pytest.mark.trace("TC-132", "FR-009-AC-10")
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
    result = run_generator([], cwd=semantic)
    assert result.returncode != 0
    assert "make semantic-install" in result.stderr
    assert "semantic-core" in result.stderr or "tsp" in result.stderr


@pytest.mark.trace("TC-196", "FR-003-AC-17", "FR-013-AC-9")
def test_testcase_status_is_optional_in_the_emitted_record_schema():
    """FR-003-AC-17/FR-013-AC-9: status-free rows remain representable in the
    record contract, while an authored status still has its typed schema."""
    schema = json.loads((SCHEMAS_DIR / "TestCaseRow.json").read_text())
    assert "status" not in schema["required"]
    assert schema["properties"]["status"]["$ref"].endswith("/CoverageStatus.json")
