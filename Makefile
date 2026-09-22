# =============================================================================
# spec-artifacts-process Makefile
# =============================================================================
# All tasks are defined in pyproject.toml using poethepoet.
# Run `poe --help` to see available tasks, or use Make targets below.
# =============================================================================

POETRY = poetry
POE = $(POETRY) run poe

.PHONY: help
help:
	@echo "Available targets (via poe):"
	@echo "  make install        - Install dependencies"
	@echo "  make test           - Run tests"
	@echo "  make lint           - Run linters (ruff + black + schema drift gate)"
	@echo "  make semantic-install - npm ci the TypeSpec package (spec_artifacts_process/semantic)"
	@echo "  make schemas        - Regenerate the semantic JSON Schemas from TypeSpec (FR-009)"
	@echo "  make schemas-check  - Fail if the committed schemas differ from a fresh projection"
	@echo "  make manifest-digests - Rewrite manifest data_schema digests from the shipped bytes"
	@echo "  make format         - Format code (black + ruff --fix)"
	@echo "  make build          - Build distribution"
	@echo "  make clean          - Clean build artifacts"
	@echo "  make version        - Show computed version"
	@echo "  make info           - Show git and version info"
	@echo "  make shell          - Open poetry shell"
	@echo ""
	@echo "Package management:"
	@echo "  make update-lock            - Update poetry.lock"
	@echo "  make update-packages        - Update deps (keep major)"
	@echo "  make update-packages-latest - Update deps (latest)"
	@echo "  make add-package p=<name>   - Add production dependency"
	@echo "  make add-dev-package p=<name> - Add dev dependency"
	@echo "  make use-local p=<name>     - Switch dep to local registry"
	@echo "  make use-upstream p=<name>  - Switch dep to upstream"

# =============================================================================
# Environment
# =============================================================================

.PHONY: install
install:
	$(POETRY) install

.PHONY: shell
shell:
	$(POETRY) shell

# =============================================================================
# Tasks (delegated to poe)
# =============================================================================

.PHONY: test
test:
	$(POE) test

.PHONY: test-integrations test-it
test-integrations test-it:
	$(POE) test-integrations

.PHONY: lint
lint: schemas-check
	$(POE) lint

# =============================================================================
# Semantic data schemas (FR-009): TypeSpec -> JSON Schema projection
# =============================================================================
# The TypeSpec package lives in spec_artifacts_process/semantic/ (npm, lockfile
# committed). `make schemas` regenerates spec_artifacts_process/schemas/<Model>.json
# and semantic/generated/toolchain.json; `make schemas-check` fails on any byte
# drift.
#
# `schemas-check` is a LOCAL gate, wired into `make lint`. It is deliberately not
# a GitHub-workflow gate: `@agent-ix/semantic-core` resolves only through the
# user-level npm config (agent-ix/filament-core-data#11), so a CI job asserting
# it would fail for a reason that is not a defect in this module.

SEMANTIC_DIR = spec_artifacts_process/semantic

.PHONY: semantic-install
semantic-install:
	cd $(SEMANTIC_DIR) && npm ci

.PHONY: schemas
schemas:
	cd $(SEMANTIC_DIR) && npm run --silent generate

.PHONY: schemas-check
schemas-check:
	cd $(SEMANTIC_DIR) && npm run --silent check

# FR-010: rewrite every `data_schema.digest` in manifest.yaml from the shipped
# bytes of the file its `data_schema.schema` names. Run after `make schemas`.
.PHONY: manifest-digests
manifest-digests:
	$(POETRY) run python scripts/manifest_digests.py

.PHONY: format
format:
	$(POE) format

.PHONY: build
build:
	$(POE) build

.PHONY: build-dist
build-dist: build

.PHONY: clean
clean:
	$(POE) clean

.PHONY: version
version:
	$(POE) version

.PHONY: info
info:
	$(POE) info

# =============================================================================
# Package Management
# =============================================================================

.PHONY: update-lock
update-lock:
	$(POETRY) lock

.PHONY: update-packages
update-packages:
	$(POE) update-deps

.PHONY: update-packages-latest
update-packages-latest:
	$(POE) update-deps-latest

.PHONY: add-package
add-package:
	package=$(p) $(POE) add-dep

.PHONY: add-dev-package
add-dev-package:
	package=$(p) $(POE) add-dev-dep

.PHONY: use-local
use-local:
	package=$(p) $(POE) use-local-dep

.PHONY: use-upstream
use-upstream:
	package=$(p) $(POE) use-upstream-dep

# =============================================================================
# Publishing
# =============================================================================

LOCAL_PYPI_URL ?= http://pypi.ix/root/dev/+simple/

.PHONY: local-publish
local-publish: build
	@echo "📦 Publishing to local PyPI ($(LOCAL_PYPI_URL))..."
	@export PATH="$$HOME/.local/bin:$$PATH"; \
	VERSION=$$($(POE) version); \
	echo "  Full version: $$VERSION"; \
	devpi use $(LOCAL_PYPI_URL); \
	devpi login root --password=''; \
	devpi upload --from-dir dist/; \
	echo "✅ Published $$VERSION"
