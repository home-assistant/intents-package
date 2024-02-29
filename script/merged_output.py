"""Command to generate merged output."""

import argparse
import collections
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
INTENTS_DIR = ROOT / "intents"


def merge_dict(base_dict, new_dict):
    """Merges new_dict into base_dict."""
    for key, value in new_dict.items():
        if key in base_dict:
            old_value = base_dict[key]
            if isinstance(old_value, collections.abc.MutableMapping):
                # Combine dictionary
                assert isinstance(
                    value, collections.abc.Mapping
                ), f"Not a dict: {value}"
                merge_dict(old_value, value)
            elif isinstance(old_value, collections.abc.MutableSequence):
                # Combine list
                assert isinstance(
                    value, collections.abc.Sequence
                ), f"Not a list: {value}"
                old_value.extend(value)
            else:
                # Overwrite
                base_dict[key] = value
        else:
            base_dict[key] = value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument(
        "--intents-dir", default=INTENTS_DIR, help="Intents repo directory"
    )
    args = parser.parse_args()

    intents_dir = Path(args.intents_dir)
    sentence_dir = intents_dir / "sentences"
    response_dir = intents_dir / "responses"
    intents_file = intents_dir / "intents.yaml"
    languages = sorted(p.name for p in sentence_dir.iterdir() if p.is_dir())

    target = Path(args.target)
    target.mkdir(parents=True, exist_ok=True)

    intent_info = yaml.safe_load(intents_file.read_text())

    # Skip intents that are not supported in Home Assistant
    supported_intents = set(
        intent for intent, info in intent_info.items() if info.get("supported")
    )

    # Create one JSON file per language
    for language in languages:
        # Merge language's sentence template YAML files
        merged_sentences: dict = {}
        for sentence_file in (sentence_dir / language).iterdir():
            merge_dict(merged_sentences, yaml.safe_load(sentence_file.read_text()))

        # Merge language's response YAML files
        merged_responses: dict = {}
        for response_file in (response_dir / language).iterdir():
            merge_dict(merged_responses, yaml.safe_load(response_file.read_text()))

        lang_intents: dict = {}
        for intent, info in merged_sentences["intents"].items():
            if intent not in supported_intents:
                continue

            data = []
            for data_set in info["data"]:
                if len(data_set["sentences"]) > 0:
                    data.append(data_set)

            if not data:
                # No sentence templates
                continue

            lang_intents[intent] = {
                **info,
                "data": data,
            }

        lang_responses = {
            intent: info
            for intent, info in merged_responses["responses"]["intents"].items()
            if intent in supported_intents
        }

        if not lang_intents and not lang_responses:
            # Nothing to export
            continue

        output: dict = {
            "language": language,
            **merged_sentences,
            "intents": lang_intents,
        }

        if lang_responses:
            # Do this separately because merged_sentences contains error responses
            output.setdefault("responses", {})["intents"] = lang_responses

        # Write as JSON
        target_path = target / f"{language}.json"
        with target_path.open("w", encoding="utf-8") as target_file:
            json.dump(output, target_file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
