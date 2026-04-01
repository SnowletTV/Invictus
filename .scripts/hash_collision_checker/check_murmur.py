"""Utility to scan localization files and detect MurmurHash collisions.

This script will traverse one or more directories containing YML localization files,
extract all keys under the various `l_<lang>` tables and then compute a MurmurHash
for each key.  An optional vanilla list of keys can be supplied via a file with
one key per line (the workflow will provide the additional test keys here).

If two different keys end up with the same hash value a collision is reported
and the script exits with a non-zero status to make the CI job fail.

It uses the same simple cleaning logic as the existing translation tooling to
allow for the optional digit between the colon and the text value (e.g. "key:0\n").

Usage::

    python .scripts/check_murmur.py <dir1> [<dir2> ...] --vanilla <path/to/file>

See .github/workflows/check_murmur.yml for an example of how this is integrated into the CI process.

"""

import argparse
import os
import re
import sys
from typing import Dict, List, Tuple

try:
    import yaml
except ImportError:
    print("Missing dependency 'PyYAML'. Please install with pip install pyyaml")
    sys.exit(1)

try:
    import mmh3
except ImportError:
    print("Missing dependency 'mmh3'. Please install with pip install mmh3")
    sys.exit(1)


# mostly copied from .scripts/translator/file_handling.py

def clean_yaml(text: str) -> str:
    # strip BOM if present; some files begin with a UTF-8 byte order mark
    # which interferes with our simple pattern matching.
    text = text.lstrip('\ufeff')

    # remove any digit immediately following the colon ("key:0 \"value\"")
    for i in range(0, 10):
        text = text.replace(f":{i}", ":")

    lines: List[str] = []
    in_table = False

    for raw in text.splitlines():
        if not raw.strip():
            # preserve blank lines verbatim
            lines.append(raw)
            continue

        stripped = raw.lstrip()
        # detect the top‑level language header
        stripped_no_bom = stripped.lstrip('\ufeff')
        if re.match(r'l_[^:]+:', stripped_no_bom):
            lines.append(stripped_no_bom)
            in_table = True
            continue

        if stripped.startswith('#'):
            # comments can be kept unchanged
            lines.append(raw)
            continue

        # it's a localisation entry – keep only the key and give it an empty
        # value so that the YAML loader can parse it without being tripped up by
        # the original content (which often contains unescaped quotes,
        # embedded colons, etc).
        key = stripped.split(':', 1)[0]
        indent = '  ' if in_table else ''
        lines.append(f'{indent}{key}: ""')

    return "\n".join(lines)


def load_yaml(file_name: str) -> dict:
    with open(file_name, encoding='utf_8_sig') as f:
        text = f.read()
    clean_text = clean_yaml(text)
    return yaml.safe_load(clean_text) or {}


def collect_keys_from_file(path: str) -> List[str]:
    """Return all localisation keys defined in a YML file.

    If the YAML parser fails due to malformed content we fall back to a
    simple line-based regex scan which is looser but avoids aborting the
    whole run.  We still print a warning so that problematic files can be
    inspected manually later.
    """
    try:
        data = load_yaml(path)
    except Exception as e:
        print(f"Warning: failed to parse {path} with yaml ({e}), using regex fallback")
        return collect_keys_from_file_fallback(path)

    keys: List[str] = []
    if isinstance(data, dict):
        for top, val in data.items():
            if isinstance(val, dict):
                keys.extend(val.keys())
            # some files are already flattened (rare); ignore otherwise
    return keys


def collect_keys_from_file_fallback(path: str) -> List[str]:
    """Extract keys by scanning for leading "key:" patterns.

    This does not attempt to fully parse YAML and will happily grab bogus
    lines, but it works on the poorly formatted files that trip the real
    loader.  We feed it the cleaned text so that the ":0" suffixes are
    removed like in the normal path.
    """
    keys: List[str] = []
    with open(path, encoding='utf_8_sig') as f:
        text = clean_yaml(f.read())
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        m = re.match(r"([^:\s]+):", stripped)
        if m:
            keys.append(m.group(1))
    return keys


def collect_keys_from_dir(directories: List[str]) -> List[Tuple[str, str]]:
    """Walk a list of directories and collect (key, source_file) tuples."""
    collected: List[Tuple[str, str]] = []
    for d in directories:
        if not os.path.isdir(d):
            continue
        for root, _, files in os.walk(d):
            for fn in files:
                if fn.lower().endswith(".yml"):
                    full = os.path.join(root, fn)
                    try:
                        keys = collect_keys_from_file(full)
                    except Exception as e:
                        print(f"Failed to parse {full}: {e}")
                        continue
                    for k in keys:
                        collected.append((k, full))
    return collected


def read_vanilla_keys(path: str) -> List[str]:
    if not os.path.isfile(path):
        return []
    keys: List[str] = []
    with open(path, encoding='utf_8_sig') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            keys.append(line)
    return keys


def murmur_hash(key: str) -> int:
    # use the 32-bit MurmurHash3 value; the original hash algorithm used in
    # Imperator/Paradox games is the 32‑bit variant.  mmh3.hash returns a signed
    # int by default, but we request an unsigned result for consistency.
    return mmh3.hash(key, signed=False)


def main():
    parser = argparse.ArgumentParser(description="Detect MurmurHash collisions in localization keys")
    parser.add_argument(
        "dirs",
        nargs="+",
        help="Directories to scan for localization YML files (english and replace)",
    )
    parser.add_argument(
        "--vanilla",
        help="Path to file containing localization keys from base (vanilla) game (one per line)",
        default=None,
    )

    args = parser.parse_args()

    kvs = collect_keys_from_dir(args.dirs)
    vanilla = []
    if args.vanilla:
        vanilla = read_vanilla_keys(args.vanilla)

    print(f"Loaded {len(kvs)} keys from {len(args.dirs)} directories")
    if vanilla:
        print(f"Loaded {len(vanilla)} vanilla keys")

    hash_map: Dict[int, List[Tuple[str, str]]] = {}

    for key, origin in kvs:
        h = murmur_hash(key)
        hash_map.setdefault(h, []).append((key, origin))

    # add vanilla keys
    for key in vanilla:
        h = murmur_hash(key)
        hash_map.setdefault(h, []).append((key, "<vanilla>"))

    collisions = {h: entries for h, entries in hash_map.items() if len({k for k, _ in entries}) > 1}

    if collisions:
        print("Collisions detected!\n")
        for h, entries in collisions.items():
            print(f"hash {h} ->")
            for k, origin in entries:
                print(f"    {k} (from {origin})")
            print()
        sys.exit(1)
    else:
        print("No collisions detected.")
        sys.exit(0)


if __name__ == "__main__":
    main()
