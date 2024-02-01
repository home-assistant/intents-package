"""API for home_assistant_intents package."""
import importlib.resources
import json
import os
import typing
from enum import Enum
from pathlib import Path
from typing import IO, Any, Callable, Dict, List, Optional

from .languages import LANGUAGES

_PACKAGE = "home_assistant_intents"
_DIR = Path(typing.cast(os.PathLike, importlib.resources.files(_PACKAGE)))
_DATA_DIR = _DIR / "data"


class ErrorKey(str, Enum):
    """Keys for home assistant intent errors."""

    NO_INTENT = "no_intent"
    """Intent was not recognized."""

    HANDLE_ERROR = "handle_error"
    """Unexpected error while handling intent."""

    NO_AREA = "no_area"
    """Area does not exist."""

    NO_DOMAIN = "no_domain"
    """No devices exist for a domain."""

    NO_DOMAIN_EXPOSED = "no_domain_exposed"
    """No devices are exposed for a domain."""

    NO_DOMAIN_IN_AREA = "no_domain_in_area"
    """No devices in an area exist for a domain."""

    NO_DOMAIN_IN_AREA_EXPOSED = "no_domain_in_area_exposed"
    """No devices in an area are exposed for a domain."""

    NO_DEVICE_CLASS = "no_device_class"
    """No devices of a class exist."""

    NO_DEVICE_CLASS_EXPOSED = "no_device_class_exposed"
    """No devices of a class are exposed."""

    NO_DEVICE_CLASS_IN_AREA = "no_device_class_in_area"
    """No devices of a class exist in an area."""

    NO_DEVICE_CLASS_IN_AREA_EXPOSED = "no_device_class_in_area_exposed"
    """No devices of a class are exposed in an area."""

    NO_ENTITY = "no_entity"
    """Entity does not exist."""

    NO_ENTITY_EXPOSED = "no_entity_exposed"
    """Entity is not exposed."""

    NO_ENTITY_IN_AREA = "no_entity_in_area"
    """Entity does not exist in area."""

    NO_ENTITY_IN_AREA_EXPOSED = "no_entity_in_area_exposed"
    """Entity in area is not exposed."""

    DUPLICATE_ENTITIES = "duplicate_entities"
    """More than one entity matched with the same name."""

    DUPLICATE_ENTITIES_IN_AREA = "duplicate_entities_in_area"
    """More than one entity in an area matched with the same name."""


def get_intents(
    language: str,
    json_load: Callable[[IO[str]], Dict[str, Any]] = json.load,
) -> Optional[Dict[str, Any]]:
    """Load intents by language."""
    intents_path = _DATA_DIR / f"{language}.json"
    if intents_path.exists():
        with intents_path.open(encoding="utf-8") as intents_file:
            return json_load(intents_file)

    return None


def get_languages() -> List[str]:
    """Return a list of available languages."""
    return LANGUAGES
