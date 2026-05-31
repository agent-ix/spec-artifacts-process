from spec_artifacts_process import (
    EXAMPLES_DIR,
    MANIFEST_PATH,
    PACK_ROOT,
    SCHEMAS_DIR,
    TEMPLATES_DIR,
)


def test_pack_exposes_resource_paths():
    assert MANIFEST_PATH == PACK_ROOT / "manifest.yaml"
    assert MANIFEST_PATH.is_file()
    assert SCHEMAS_DIR == PACK_ROOT / "schemas"
    assert TEMPLATES_DIR == PACK_ROOT / "templates"
    assert EXAMPLES_DIR == PACK_ROOT / "examples"
