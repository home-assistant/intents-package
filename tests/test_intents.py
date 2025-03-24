"""Test loading intents for available languages."""

import pytest

from home_assistant_intents import get_intents, get_languages


@pytest.mark.parametrize("language", get_languages())
def test_load_intents(language: str) -> None:
    """Test that we can load intents for every supported language."""
    lang_intents = get_intents(language)
    assert lang_intents
