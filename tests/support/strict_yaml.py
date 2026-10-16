"""YAML loading helpers that reject duplicate mapping keys."""

from __future__ import annotations

from typing import Any

import yaml


class StrictSafeLoader(yaml.SafeLoader):
    """SafeLoader that fails instead of silently keeping the last duplicate."""


def _construct_mapping(
    loader: StrictSafeLoader,
    node: yaml.MappingNode,
    deep: bool = False,
) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as error:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable key",
                key_node.start_mark,
            ) from error
        if duplicate:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


StrictSafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping,
)


def load_yaml_strict(text: str) -> Any:
    """Parse safe YAML and reject repeated keys at every mapping depth."""
    return yaml.load(text, Loader=StrictSafeLoader)
