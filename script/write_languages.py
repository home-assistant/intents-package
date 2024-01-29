"""
Generates a Python file with available domains/languages.

This is automatically run by script/package after the data files are generated.
"""
import argparse
import json
from pathlib import Path


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("data_dir", help="Path to directory with <language>.json files")
    args = parser.parse_args()
    data_dir = Path(args.data_dir)

    languages = [language_file.stem for language_file in data_dir.glob("*.json")]
    print("LANGUAGES =", json.dumps(sorted(languages)))


if __name__ == "__main__":
    main()
