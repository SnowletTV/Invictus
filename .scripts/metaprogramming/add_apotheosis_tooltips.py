import os
import re

# --- Configuration ---

# 1. Get the directory where THIS script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Construct paths relative to the script's location
COMMON_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "common", "deities"))
LOCALIZATION_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "localization", "english", "deities"))

print(f"Script Directory: {SCRIPT_DIR}")
print(f"Target Common Path: {COMMON_PATH}")
print(f"Target Loc Path:    {LOCALIZATION_PATH}")
print("-" * 30)

# Regex to find the START of a deity definition (e.g., deity_ninurta = {)
# We use MULTILINE and ^ to ensure we only catch top-level definitions, not triggers inside other blocks
DEITY_START_PATTERN = re.compile(r'^\s*(deity_(\w+))\s*=\s*\{', re.MULTILINE)

# Regex to find the START of the on_activate block
ON_ACTIVATE_START_PATTERN = re.compile(r'on_activate\s*=\s*\{')

# Regex to find effects like 'military_apotheosis_effect = yes'
# Matches any word followed immediately by '= yes'
EFFECT_PATTERN = re.compile(r'(\w+)\s*=\s*yes')

# Localization matcher
LOC_LINE_PATTERN = re.compile(r'^\s*(omen_(\w+)_desc)(:\d*)?\s*"(.*)"\s*$', re.MULTILINE)

def extract_block_body(text, open_brace_index):
    """
    Given the full text and the index of an opening '{', 
    this scans forward counting braces to return the content INSIDE the block.
    """
    count = 1
    i = open_brace_index + 1
    length = len(text)
    
    while i < length and count > 0:
        char = text[i]
        if char == '{':
            count += 1
        elif char == '}':
            count -= 1
        i += 1
    
    # Return content excluding the outer braces
    return text[open_brace_index + 1 : i - 1]

def get_deity_data():
    """
    Robustly scans common/deities using bracket counting.
    """
    deity_map = {}
    total_deities_scanned = 0
    
    if not os.path.exists(COMMON_PATH):
        print(f"Error: Could not find path: {COMMON_PATH}")
        return {}

    for filename in os.listdir(COMMON_PATH):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(COMMON_PATH, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                content = f.read()

            # Find all start locations of "deity_xyz = {"
            for match in DEITY_START_PATTERN.finditer(content):
                total_deities_scanned += 1
                short_name = match.group(2) # e.g., 'ninurta'
                
                # The brace is the last character of the match
                start_brace_index = match.end() - 1
                
                # 1. Extract the whole deity block
                deity_body = extract_block_body(content, start_brace_index)
                
                # 2. Find 'on_activate = {' inside this deity block
                oa_match = ON_ACTIVATE_START_PATTERN.search(deity_body)
                
                if oa_match:
                    oa_brace_index = oa_match.end() - 1
                    # 3. Extract the 'on_activate' block content
                    oa_body = extract_block_body(deity_body, oa_brace_index)
                    
                    # 4. Find all 'effect = yes' lines inside on_activate
                    effect_matches = EFFECT_PATTERN.findall(oa_body)
                    
                    target_effect = None
                    
                    if effect_matches:
                        # Logic: Prefer effects with "apotheosis" in the name. 
                        # If none, take the first one found.
                        apotheosis_effects = [e for e in effect_matches if "apotheosis" in e]
                        
                        if apotheosis_effects:
                            target_effect = apotheosis_effects[0]
                        else:
                            target_effect = effect_matches[0]

                    if target_effect:
                        deity_map[short_name] = target_effect

        except Exception as e:
            print(f"Error processing common file {filename}: {e}")

    print(f"Scanned {total_deities_scanned} total deity definitions.")
    return deity_map

def update_localization(deity_map):
    found_keys = set()
    updated_keys = set()
    files_modified = 0
    
    if not os.path.exists(LOCALIZATION_PATH):
        print(f"Error: Could not find path: {LOCALIZATION_PATH}")
        return found_keys, updated_keys

    for filename in os.listdir(LOCALIZATION_PATH):
        if not filename.endswith(".yml"): 
            continue

        filepath = os.path.join(LOCALIZATION_PATH, filename)
        new_lines = []
        file_changed = False

        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                lines = f.readlines()

            for line in lines:
                match = LOC_LINE_PATTERN.match(line)
                
                if match:
                    full_key = match.group(1)
                    short_name = match.group(2)
                    version_num = match.group(3) if match.group(3) else ""
                    current_text = match.group(4)
                    
                    if short_name in deity_map:
                        found_keys.add(short_name)
                        effect = deity_map[short_name]
                        string_to_add = f"\\n\\n${effect}_tt_description$"
                        
                        if string_to_add not in current_text:
                            cleaned_text = current_text.rstrip()
                            indentation = line[:line.find(full_key)]
                            new_line = f'{indentation}{full_key}{version_num} "{cleaned_text}{string_to_add}"\n'
                            new_lines.append(new_line)
                            file_changed = True
                            updated_keys.add(short_name)
                            continue

                new_lines.append(line)

            if file_changed:
                with open(filepath, 'w', encoding='utf-8-sig') as f:
                    f.writelines(new_lines)
                files_modified += 1

        except Exception as e:
            print(f"Error processing loc file {filename}: {e}")
            
    if files_modified > 0:
        print(f"Written changes to {files_modified} localization files.")
    
    return found_keys, updated_keys

if __name__ == "__main__":
    # 1. Get Data
    mapped_data = get_deity_data()
    unique_effects = set(mapped_data.values())

    if mapped_data:
        print(f"Found {len(mapped_data)} deities with apotheosis effects.")
        
        # 2. Update Files
        found_keys, updated_keys = update_localization(mapped_data)
        
        # 3. Calculate Lists
        missing_keys = set(mapped_data.keys()) - found_keys
        skipped_keys = found_keys - updated_keys
        
        # 4. Report Results
        print("\n" + "="*50)
        print("REPORT")
        print("="*50)

        # A. UPDATED
        if updated_keys:
            print(f"\n[UPDATED] ({len(updated_keys)}) - Added tooltips to:")
            for key in sorted(updated_keys):
                print(f"  + {key}")
        
        # B. SKIPPED
        if skipped_keys:
            print(f"\n[SKIPPED] ({len(skipped_keys)}) - Already up to date:")
            for key in sorted(skipped_keys):
                print(f"  = {key}")

        # C. MISSING
        if missing_keys:
            print(f"\n[MISSING] ({len(missing_keys)}) - Deity found in common, but loc key NOT found:")
            for key in sorted(missing_keys):
                print(f"  ! {key}")

        # 5. Print TBD lines
        print("\n" + "-" * 50)
        print("COPY PASTE BELOW FOR NEW LOCALIZATION KEYS")
        print("-" * 50)
        for effect in sorted(unique_effects):
            print(f' {effect}_tt_description:0 "TBD"')
        print("-" * 50)

    else:
        print("No deities with apotheosis effects found.")