"""The Quoin install boundary (IT-002).

`quoin module install path:<dir>` is the second consumer of the manifest, and
before #78 nothing in this specification asserted it: a manifest Quire accepts
and Quoin refuses would have shipped (SR-015 FND-001). It shipped anyway in the
sibling module, and this row is what found it.

**[RAN] 2026-09-04 and it is red for a named upstream reason.** Quoin's FR-070
validator resolves `semantic.exports` against `object_types` only, so an
**artifact** module cannot be installed at all — this one is refused with
`semantic.export-without-schema` (the schemas exist, on the `artifact_types`
entries the validator does not look at) and the already-merged
`spec-artifacts-iso` with `semantic.unknown-export`. Filed as
`agent-ix/quoin#347`.

So this is a **strict expected failure**, never a skip. The boundary is
exercised on every run that opts in, and the row turns green the day Quoin
resolves an artifact-type export.

**Opt-in, and it stays opt-in.** The install writes into the operator's global
`~/.ix/filament/modules/` store, and the module it replaces is the one *every
repository in the programme validates against*. A failed restore does not
inconvenience one test run; it repoints the whole development environment at an
uncommitted branch. So it runs only when `QUOIN_INSTALL_ROUNDTRIP=1` says the
operator has agreed to that, and the restore runs whether or not the earlier
steps passed (IT-002-SC-06) — verified: after the 2026-09-04 run the module
store was byte-identical to a copy taken beforehand.
"""

from __future__ import annotations

import os
import shutil
import subprocess

import pytest
from conftest import PACKAGE_ROOT

OPT_IN = os.environ.get("QUOIN_INSTALL_ROUNDTRIP") == "1"
QUOIN = shutil.which("quoin")

needs_opt_in = pytest.mark.skipif(
    not (OPT_IN and QUOIN),
    reason=(
        "IT-002 mutates the operator's global Quoin module store, and the entry "
        "it replaces is the one every repository validates against. Set "
        "QUOIN_INSTALL_ROUNDTRIP=1 with `quoin` on PATH to run it."
    ),
)


def quoin(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([QUOIN, *args], capture_output=True, text=True, check=False)


@pytest.mark.integration
@pytest.mark.xfail(
    strict=True,
    reason=(
        "agent-ix/quoin#347: the semantic-contract validator resolves "
        "`semantic.exports` against `object_types` only, so no artifact module "
        "installs. Red by design; turns green when Quoin resolves an "
        "artifact-type export."
    ),
)
@needs_opt_in
def test_the_module_installs_into_quoin_and_the_prior_state_is_restored():
    before = quoin("module")
    assert before.returncode == 0, before.stderr
    assert "spec-artifacts-process" in before.stdout, "IT-002-SC-01: nothing to restore"

    try:
        install = quoin("module", "install", f"path:{PACKAGE_ROOT}")
        assert install.returncode == 0, install.stdout + install.stderr  # IT-002-SC-02

        listing = quoin("module")  # IT-002-SC-03
        assert listing.returncode == 0
        assert "spec-artifacts-process" in listing.stdout
    finally:
        # IT-002-SC-05 and SC-06. Unconditional: a failed install must never
        # leave the operator's global store half-written.
        quoin("module", "install", "spec-artifacts-process")
        after = quoin("module")
        assert "spec-artifacts-process" in after.stdout
