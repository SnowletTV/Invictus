import re
from pathlib import Path

# ---------------- CONFIG ----------------
ROOT_DIR = Path("C:/Users/snowl/Documents/Paradox Interactive/Imperator/mod/invictus")
GLOB = "**/*.txt"

# Define rules for block patterns
# pattern: keys must exist; value=None means any value
REPLACE_RULES = [
    {
        "pattern": {"multiply": "-6", "add": None},
        "max": "-20",
        "min": "-2000",
        "flag": "floor = yes"
    },
    {
        "pattern": {"multiply": "6", "subtract": None},
        "max": "-20",
        "min": "-2000",
        "flag": "floor = yes"
    },
    {
        "pattern": {"multiply": "6", "add": None},
        "max": "1000",
        "min": "10",
        "flag": "ceiling = yes"
    },
    {
        "pattern": {"multiply": "-6", "subtract": None},
        "max": "1000",
        "min": "10",
        "flag": "ceiling = yes"
    },
    {
        "pattern": {"multiply": "-12", "add": None},
        "max": "-20",
        "min": "-4000",
        "flag": "floor = yes"
    },
    {
        "pattern": {"multiply": "12", "subtract": None},
        "max": "-20",
        "min": "-4000",
        "flag": "floor = yes"
    },
    {
        "pattern": {"multiply": "12", "add": None},
        "max": "2000",
        "min": "20",
        "flag": "ceiling = yes"
    },
    {
        "pattern": {"multiply": "-12", "subtract": None},
        "max": "2000",
        "min": "20",
        "flag": "ceiling = yes"
    },
    {
        "pattern": {"multiply": "-18", "add": None},
        "max": "-20",
        "min": "-6000",
        "flag": "floor = yes"
    },
    {
        "pattern": {"multiply": "18", "subtract": None},
        "max": "-20",
        "min": "-6000",
        "flag": "floor = yes"
    },
    {
        "pattern": {"multiply": "18", "add": None},
        "max": "3000",
        "min": "20",
        "flag": "ceiling = yes"
    },
    {
        "pattern": {"multiply": "-18", "subtract": None},
        "max": "3000",
        "min": "20",
        "flag": "ceiling = yes"
    },
]
# ----------------------------------------

kv_pattern = re.compile(r'([a-zA-Z_][a-zA-Z0-9_.]*)\s*=\s*([^\s{}]+)')

def find_matching_brace(s: str, open_idx: int):
    """Return index of matching '}' for the '{' at open_idx."""
    depth = 0
    for i in range(open_idx, len(s)):
        ch = s[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
    return None

def match_rule(block_kv: dict):
    """Return first rule that matches the block keys/values."""
    for rule in REPLACE_RULES:
        matched = True
        for key, val in rule["pattern"].items():
            if key not in block_kv:
                matched = False
                break
            if val is not None and str(block_kv[key]) != str(val):
                matched = False
                break
        if matched:
            return rule
    return None

def normalize_block(original_block: str):
    """Normalize a block according to REPLACE_RULES with conditional max/min logic."""
    idx_open = original_block.find("{")
    idx_close = original_block.rfind("}")
    if idx_open == -1 or idx_close == -1 or idx_close <= idx_open:
        return original_block

    opening_line_text = original_block[: idx_open + 1]
    inner_text = original_block[idx_open + 1: idx_close]

    # detect item indent
    item_indent = None
    for l in inner_text.splitlines():
        if l.strip():
            m = re.match(r"^(\s*)", l)
            item_indent = m.group(1) if m else ""
            break
    if item_indent is None:
        item_indent = "    "

    # detect closing brace indent
    m_close = re.search(r"\n([ \t]*)\}", original_block)
    closing_indent = m_close.group(1) if m_close else ""

    # parse block key/value pairs
    lines = inner_text.splitlines()
    output_items = []
    block_kv = {}  # existing key/values
    for line in lines:
        if not line.strip():
            continue
        matches = list(kv_pattern.finditer(line))
        if matches:
            for mm in matches:
                key, val = mm.group(1), mm.group(2)
                block_kv[key] = val
        else:
            # preserve raw lines
            output_items.append(("raw", line.strip()))

    # check which rule applies
    rule = match_rule(block_kv)
    if not rule:
        # No matching pattern, return original block
        return original_block

    # rebuild block lines
    rebuilt = []
    multiply_inserted = False
    for line in lines:
        if not line.strip():
            continue
        matches = list(kv_pattern.finditer(line))
        if matches:
            for mm in matches:
                key, val = mm.group(1), mm.group(2)
                if key in ("floor", "ceiling", "max", "min"):
                    continue  # remove old
                if key == "multiply" and val == rule["pattern"]["multiply"] and not multiply_inserted:
                    rebuilt.append((key, val))
                    # insert flag
                    flag_key, flag_val = rule["flag"].split("=", 1)
                    rebuilt.append((flag_key.strip(), flag_val.strip()))
                    # compute max/min with conditional logic
                    # MAX
                    target_max = int(rule["max"])
                    existing_max = int(block_kv.get("max", target_max))
                    if flag_key.strip() == "floor":
                        # floor → max: pick highest unless existing is already more extreme
                        if abs(existing_max) > abs(target_max):
                            max_val = existing_max
                        else:
                            max_val = max(existing_max, target_max)
                    else:  # ceiling
                        max_val = min(existing_max, target_max)

                    # MIN
                    target_min = int(rule["min"])
                    existing_min = int(block_kv.get("min", target_min))
                    if flag_key.strip() == "ceiling":
                        # ceiling → min: pick lowest unless existing is already more extreme
                        if abs(existing_min) > abs(target_min):
                            min_val = existing_min
                        else:
                            min_val = min(existing_min, target_min)
                    else:  # floor
                        min_val = max(existing_min, target_min)
                    # insert max/min
                    rebuilt.append(("max", str(max_val)))
                    rebuilt.append(("min", str(min_val)))
                    multiply_inserted = True
                else:
                    rebuilt.append((key, val))
        else:
            rebuilt.append(("raw", line.strip()))

    # fallback if multiply wasn't found (unlikely)
    if not multiply_inserted:
        rebuilt.append(("multiply", rule["pattern"]["multiply"]))
        flag_key, flag_val = rule["flag"].split("=", 1)
        rebuilt.append((flag_key.strip(), flag_val.strip()))
        rebuilt.append(("max", rule["max"]))
        rebuilt.append(("min", rule["min"]))

    # assemble final block
    final_lines = []
    for it in rebuilt:
        if it[0] == "raw":
            final_lines.append(f"{item_indent}{it[1]}")
        else:
            k, v = it
            final_lines.append(f"{item_indent}{k} = {v}")

    new_block = opening_line_text.rstrip() + "\n"
    if final_lines:
        new_block += "\n".join(final_lines) + "\n"
    new_block += f"{closing_indent}}}"
    return new_block

def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    # search all multiply values from rules
    multiply_values = [r["pattern"]["multiply"] for r in REPLACE_RULES]
    pattern = re.compile(r"^\s*multiply\s*=\s*(" + "|".join(re.escape(v) for v in multiply_values) + r")\s*$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    if not matches:
        return False

    blocks = []
    for m in matches:
        open_brace_idx = text.rfind("{", 0, m.start())
        if open_brace_idx == -1:
            continue
        close_idx = find_matching_brace(text, open_brace_idx)
        if close_idx is None:
            continue
        if not (open_brace_idx < m.start() < close_idx):
            continue
        line_start = text.rfind("\n", 0, open_brace_idx)
        line_start = 0 if line_start == -1 else line_start + 1
        blocks.append((line_start, open_brace_idx, close_idx))

    if not blocks:
        return False

    # process from bottom to top to avoid shifting indices
    blocks = sorted(set(blocks), key=lambda x: x[0], reverse=True)

    new_text = text
    for line_start, open_idx, close_idx in blocks:
        orig_block = text[line_start: close_idx + 1]
        fixed_block = normalize_block(orig_block)
        new_text = new_text[:line_start] + fixed_block + new_text[close_idx + 1:]

    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False

def main():
    changed = 0
    for p in ROOT_DIR.glob(GLOB):
        if p.is_file():
            if process_file(p):
                print(f"Fixed: {p}")
                changed += 1
    print(f"Done. Files changed: {changed}")

if __name__ == "__main__":
    main()
