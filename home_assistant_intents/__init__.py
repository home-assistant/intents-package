"""API for home_assistant_intents package."""
import importlib.resources
import json
import os
import typing
from pathlib import Path
from typing import IO, Any, Callable, Dict, List, Optional

from .languages import LANGUAGES

_PACKAGE = "home_assistant_intents"
_DIR = Path(typing.cast(os.PathLike, importlib.resources.files(_PACKAGE)))
_DATA_DIR = _DIR / "data"


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
