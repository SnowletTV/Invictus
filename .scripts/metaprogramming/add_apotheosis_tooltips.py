import os
import re

# --- Configuration ---

# 1. Get the directory where THIS script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Construct paths relative to the script's location
COMMON_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "common", "deities"))
LOCALIZATION_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "localization", "english", "deities"))
SETUP_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "setup", "main", "deities"))

print(f"Script Directory: {SCRIPT_DIR}")
print(f"Common Path:      {COMMON_PATH}")
print(f"Setup Path:       {SETUP_PATH}")
print(f"Loc Path:         {LOCALIZATION_PATH}")
print("-" * 30)

# --- Regex Patterns ---

# Common/Deities patterns
DEITY_START_PATTERN = re.compile(r'^\s*(deity_(\w+))\s*=\s*\{', re.MULTILINE)
ON_ACTIVATE_START_PATTERN = re.compile(r'on_activate\s*=\s*\{')
EFFECT_PATTERN = re.compile(r'(\w+)\s*=\s*yes')

# Localization patterns
LOC_LINE_PATTERN = re.compile(r'^\s*(omen_(\w+)_desc)(:\d*)?\s*"(.*)"\s*$', re.MULTILINE)

# Setup/Deities patterns
DEITIES_DB_PATTERN = re.compile(r'deities_database\s*=\s*\{')
SETUP_BLOCK_PATTERN = re.compile(r'^\s*(\d+)\s*=\s*\{', re.MULTILINE) # Matches "1700 = {"
SETUP_DEITY_NAME_PATTERN = re.compile(r'deity\s*=\s*deity_(\w+)')
SETUP_DEIFY_RULER_PATTERN = re.compile(r'^\s*deify_ruler\s*=', re.MULTILINE)

# --- Helper Functions ---

def extract_block_body(text, open_brace_index):
    """
    Given text and the index of an opening '{', scans forward counting braces 
    to return the content INSIDE that specific block.
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
    
    return text[open_brace_index + 1 : i - 1]

# --- Main Logic Steps ---

def get_excluded_deities():
    """
    Scans setup/main/deities.
    Returns a set of deity short names (e.g., 'makkhali_gosala') that have 'deify_ruler'.
    """
    excluded = set()
    
    if not os.path.exists(SETUP_PATH):
        print(f"Error: Could not find path: {SETUP_PATH}")
        return excluded

    print("Scanning setup files for deified rulers...")

    for filename in os.listdir(SETUP_PATH):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(SETUP_PATH, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                content = f.read()

            # 1. Find the main "deities_database = {" block
            db_match = DEITIES_DB_PATTERN.search(content)
            if not db_match:
                continue # Skip files that don't have a database
            
            # Extract the database body
            db_body = extract_block_body(content, db_match.end() - 1)
            
            # 2. Iterate through numbered blocks (1700 = {, 1701 = {, etc.) inside the database
            for match in SETUP_BLOCK_PATTERN.finditer(db_body):
                start_brace = match.end() - 1
                entry_body = extract_block_body(db_body, start_brace)
                
                # 3. Check if this entry has 'deify_ruler'
                if SETUP_DEIFY_RULER_PATTERN.search(entry_body):
                    # 4. Extract the deity name
                    name_match = SETUP_DEITY_NAME_PATTERN.search(entry_body)
                    if name_match:
                        deity_name = name_match.group(1)
                        excluded.add(deity_name)

        except Exception as e:
            print(f"Error processing setup file {filename}: {e}")

    print(f"Found {len(excluded)} deities to exclude (Deified Rulers).")
    return excluded

def get_deity_data():
    """
    Scans common/deities and returns map: {'ninurta': 'apotheosis_effect'}
    """
    deity_map = {}
    total_scanned = 0
    
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

            for match in DEITY_START_PATTERN.finditer(content):
                total_scanned += 1
                short_name = match.group(2)
                start_brace = match.end() - 1
                deity_body = extract_block_body(content, start_brace)
                
                oa_match = ON_ACTIVATE_START_PATTERN.search(deity_body)
                if oa_match:
                    oa_body = extract_block_body(deity_body, oa_match.end() - 1)
                    effect_matches = EFFECT_PATTERN.findall(oa_body)
                    
                    target_effect = None
                    if effect_matches:
                        apotheosis_effects = [e for e in effect_matches if "apotheosis" in e]
                        target_effect = apotheosis_effects[0] if apotheosis_effects else effect_matches[0]

                    if target_effect:
                        deity_map[short_name] = target_effect

        except Exception as e:
            print(f"Error processing common file {filename}: {e}")

    print(f"Scanned {total_scanned} definitions in common/deities.")
    return deity_map

def update_localization(deity_map, excluded_deities):
    """
    Updates localization files, respecting the excluded_deities list.
    """
    found_keys = set()
    updated_keys = set()
    excluded_keys_hit = set()
    files_modified = 0
    
    if not os.path.exists(LOCALIZATION_PATH):
        print(f"Error: Could not find path: {LOCALIZATION_PATH}")
        return found_keys, updated_keys, excluded_keys_hit

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
                        
                        # EXCLUSION CHECK
                        if short_name in excluded_deities:
                            excluded_keys_hit.add(short_name)
                            new_lines.append(line) # Add line as-is, do not modify
                            continue

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
    
    return found_keys, updated_keys, excluded_keys_hit

if __name__ == "__main__":
    # 1. Get Exclusions (Setup)
    exclusions = get_excluded_deities()

    # 2. Get Data (Common)
    mapped_data = get_deity_data()
    unique_effects = set(mapped_data.values())

    if mapped_data:
        print(f"Found {len(mapped_data)} deities with apotheosis effects in common.")
        
        # 3. Update Files (Localization)
        found_keys, updated_keys, excluded_hits = update_localization(mapped_data, exclusions)
        
        # 4. Calculate Lists
        # Missing = In common map, NOT found in loc file at all
        missing_keys = set(mapped_data.keys()) - found_keys
        
        # Skipped = Found in loc, matched common, but text was already there (not updated)
        # Note: We must remove excluded hits from skipped calculation to be accurate
        skipped_keys = (found_keys - updated_keys) - excluded_hits
        
        # 5. Report Results
        print("\n" + "="*50)
        print("REPORT")
        print("="*50)

        if updated_keys:
            print(f"\n[UPDATED] ({len(updated_keys)}) - Added tooltips to:")
            for key in sorted(updated_keys):
                print(f"  + {key}")
        
        if excluded_hits:
            print(f"\n[EXCLUDED] ({len(excluded_hits)}) - Found but ignored (Deified Rulers):")
            for key in sorted(excluded_hits):
                print(f"  X {key}")

        if skipped_keys:
            print(f"\n[SKIPPED] ({len(skipped_keys)}) - Already up to date:")
            for key in sorted(skipped_keys):
                print(f"  = {key}")

        if missing_keys:
            print(f"\n[MISSING] ({len(missing_keys)}) - Deity found in common, but loc key NOT found:")
            for key in sorted(missing_keys):
                print(f"  ! {key}")

        print("\n" + "-" * 50)
        print("COPY PASTE BELOW FOR NEW LOCALIZATION KEYS")
        print("-" * 50)
        for effect in sorted(unique_effects):
            print(f' {effect}_tt_description:0 "TBD"')
        print("-" * 50)

    else:
        print("No deities with apotheosis effects found.")