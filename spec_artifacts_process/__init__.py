"""spec-artifacts-process — Filament Module pack.

This package ships the pack's ``manifest.yaml``, ``schemas/*.json`` and
``templates/*.md.j2`` as resource data. The filament-core activation
pipeline (via cloudmanager-local-sync ``load_pack_manifest``) imports this
package and reads ``MANIFEST_PATH`` to register the pack's object_types.

The Python module exists primarily so the pack can ship via the IX
package registry; there is no runtime API.
"""

from pathlib import Path

PACK_ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = PACK_ROOT / "manifest.yaml"
SCHEMAS_DIR = PACK_ROOT / "schemas"
TEMPLATES_DIR = PACK_ROOT / "templates"
EXAMPLES_DIR = PACK_ROOT / "examples"

__all__ = [
    "MANIFEST_PATH",
    "SCHEMAS_DIR",
    "TEMPLATES_DIR",
    "EXAMPLES_DIR",
    "PACK_ROOT",
]
