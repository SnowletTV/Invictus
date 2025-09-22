import re
from pathlib import Path

# -------- CONFIG ----------
ROOT_DIR = Path("C:/Users/snowl/Documents/Paradox Interactive/Imperator/mod/invictus")  # change this
GLOB = "**/*.txt"

# List of mass replace rules
REPLACE_RULES = [
    {"multiply": "-6", "max": "-25", "min": "-4000", "flag": "floor = yes"},
    {"multiply": "6", "max": "2000", "min": "25", "flag": "ceiling = yes"}
]
# --------------------------

kv_pattern = re.compile(r'([a-zA-Z_][a-zA-Z0-9_.]*)\s*=\s*([^\s{}]+)')

def find_matching_brace(s: str, open_idx: int):
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

def normalize_block(original_block: str):
    idx_open = original_block.find("{")
    idx_close = original_block.rfind("}")
    if idx_open == -1 or idx_close == -1 or idx_close <= idx_open:
        return original_block

    opening_line_text = original_block[: idx_open + 1]
    inner_text = original_block[idx_open + 1: idx_close]

    item_indent = None
    for l in inner_text.splitlines():
        if l.strip():
            m = re.match(r"^(\s*)", l)
            item_indent = m.group(1) if m else ""
            break
    if item_indent is None:
        item_indent = "    "

    m_close = re.search(r"\n([ \t]*)\}", original_block)
    closing_indent = m_close.group(1) if m_close else ""

    # parse inner lines
    output_items = []
    existing = {}
    lines = inner_text.splitlines()

    for line in lines:
        if not line.strip():
            continue
        matches = list(kv_pattern.finditer(line))
        if matches:
            for mm in matches:
                key = mm.group(1)
                val = mm.group(2)
                # store existing max/min for conditional logic
                if key in ("max", "min"):
                    try:
                        existing[key] = int(val)
                    except ValueError:
                        existing[key] = val  # keep as string if not int
                    continue
                elif key in ("floor", "ceiling"):
                    continue
                else:
                    output_items.append((key, val))
        else:
            output_items.append(("raw", line.strip()))

    # apply rules from REPLACE_RULES if multiply exists
    multiply_found = False
    for i, it in enumerate(output_items):
        if it[0] == "multiply":
            multiply_val = it[1]
            for rule in REPLACE_RULES:
                if rule["multiply"] == multiply_val:
                    multiply_found = True
                    # insert multiply line
                    output_items[i] = ("multiply", multiply_val)
                    # insert flag
                    flag_key, flag_val = rule["flag"].split("=")
                    output_items.insert(i + 1, (flag_key.strip(), flag_val.strip()))
                    # determine max value
                    target_max = int(rule["max"])
                    if "max" in existing:
                        existing_max = int(existing["max"])
                        if target_max < 0:
                            max_val = min(existing_max, target_max)   # negative: smallest
                        else:
                            max_val = min(existing_max, target_max)   # positive: smallest
                    else:
                        max_val = target_max

                    # determine min value
                    target_min = int(rule["min"])
                    if "min" in existing:
                        existing_min = int(existing["min"])
                        if target_min < 0:
                            min_val = max(existing_min, target_min)   # negative: largest
                        else:
                            min_val = min(existing_min, target_min)   # positive: smallest
                    else:
                        min_val = target_min
                    # insert max/min after flag
                    output_items.insert(i + 2, ("max", str(max_val)))
                    output_items.insert(i + 3, ("min", str(min_val)))
                    break
            break

    if not multiply_found:
        # if multiply wasn't found, fallback to adding at the end of block
        for rule in REPLACE_RULES:
            output_items.append(("multiply", rule["multiply"]))
            flag_key, flag_val = rule["flag"].split("=")
            output_items.append((flag_key.strip(), flag_val.strip()))
            output_items.append(("max", rule["max"]))
            output_items.append(("min", rule["min"]))

    # rebuild block
    item_lines = []
    for it in output_items:
        if it[0] == "raw":
            item_lines.append(f"{item_indent}{it[1]}")
        else:
            k, v = it
            item_lines.append(f"{item_indent}{k} = {v}")

    new_block = opening_line_text.rstrip() + "\n"
    if item_lines:
        new_block += "\n".join(item_lines) + "\n"
    new_block += f"{closing_indent}}}"
    return new_block

def process_file(path: Path) -> bool:
    """Process a single file. Returns True if file was changed."""
    text = path.read_text(encoding="utf-8")
    # find any multiply value from rules
    multiply_values = [r["multiply"] for r in REPLACE_RULES]
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

    seen = set()
    uniq_blocks = []
    for b in blocks:
        if b[0] in seen:
            continue
        seen.add(b[0])
        uniq_blocks.append(b)
    uniq_blocks.sort(reverse=True, key=lambda x: x[0])

    new_text = text
    for line_start, open_idx, close_idx in uniq_blocks:
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