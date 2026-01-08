import os

# --- STEPS TO RUN PROGRAM CORRECTLY ---
# This is a program to automagically generate a .txt containing a command to be used in the in-game explorer.
# It will delete every country that doesn't have a mission tree based on the "potential" blocks of every mission file.
# Countries that get a mission tree after getting free are accounted for.
# You need to fill out:
    #output_filename
    #excluded_files
    #ImperatorRomePath
# If for whatever reason you want to keep a country regardless of mission trees, edit the "footer" at the end of the file.
# Do not move this file, it wont work if you run it elsewhere.

# --- CONFIGURATION ---
output_filename = "delete_generic_countries.txt" # What the output file will be named. Can be anything.

excluded_files = [ # Add the exact filenames you want to ignore here (including .txt)
    "00_example.txt",
    "00_generic.txt",
    "00_generic_mission_infra.txt",
    "00_missions.txt",
    "00_tribal_reform.txt",
    "00_generic_mission_subject_independence_inv.txt",
]

ImperatorRomePath = "C:\Program Files (x86)\Steam\steamapps\common\ImperatorRome" # Add the path to your I:R game so the program can find vanilla missions

# --- This is where the magic happens --- #
# Several trees were harmed in the process of generating this code :(

# Get the folder where this script is located
script_location = os.path.dirname(os.path.abspath(__file__))

# Construct path to Mod Missions: Go up two levels (..) from .scripts\metaprogramming
mod_missions_path = os.path.abspath(os.path.join(script_location, "..", "..", "common", "missions"))

# Construct path to Vanilla Missions
vanilla_missions_path = os.path.join(ImperatorRomePath, "game", "common", "missions")

# --- HELPER FUNCTIONS ---
def extract_potential(content):
    """Finds text inside 'potential = { ... }' handling nested braces."""
    marker = "potential = {"
    start_index = content.find(marker)
    
    if start_index == -1:
        return None

    current_index = start_index + len(marker)
    brace_count = 1
    extracted_text = ""
    
    while brace_count > 0 and current_index < len(content):
        char = content[current_index]
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
        
        if brace_count > 0:
            extracted_text += char
        current_index += 1
        
    return extracted_text.strip()

def get_mission_files(directory):
    """Returns a dict of {filename: full_path} for .txt files in a dir."""
    files_dict = {}
    if os.path.exists(directory):
        for f in os.listdir(directory):
            if f.endswith(".txt"):
                files_dict[f] = os.path.join(directory, f)
    else:
        print(f"Warning: Directory not found: {directory}")
    return files_dict

# --- MAIN LOGIC ---

# 1. Collect Files (Handling Overwrites)
# First get vanilla files
final_file_list = get_mission_files(vanilla_missions_path)

# Then get mod files (updating the dict will overwrite vanilla files with same name)
mod_files = get_mission_files(mod_missions_path)
final_file_list.update(mod_files)

# 2. Sort Alphabetically by Filename
sorted_filenames = sorted(final_file_list.keys())

print(f"Found {len(sorted_filenames)} unique mission files. Processing...")

# 3. Write Output
output_path = os.path.join(script_location, output_filename)

with open(output_path, "w", encoding="utf-8") as out:
    
    # --- HEADER ---
    out.write("#Copy and execute this command in the explorer window of a country that will NOT get deleted\n")
    out.write("every_country = {")

    count = 0
    variable_counter = 1
    
    for filename in sorted_filenames:
        
        # --- EXCLUSION CHECK ---
        if filename in excluded_files:
            print(f"Excluding: {filename}")
            continue

        full_path = final_file_list[filename]
        
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
                logic = extract_potential(content)
                
                if logic:
                   # --- FILTERING LOGIC ---
                    lines = logic.splitlines()
                    filtered_lines = []
                    
                    for line in lines:
                        # 1. Remove comments (split at '#' and take the first part)
                        code_part = line.split('#')[0]
                        
                        # 2. Strip whitespace to check the actual code
                        clean_code = code_part.strip()
                        
                        # 3. Skip if it matches the target string
                        if clean_code == "is_subject = no":
                            continue
                        
                        # 4. If it's a valid line (and not just an empty line after removing comments)
                        if line.strip(): 
                            # Re-add indentation for the final file
                            filtered_lines.append("\t\t" + line.strip())
                    
                    # Join them back together
                    indented_logic = "\n".join(filtered_lines)

                    # First block is 'if', all others are 'else_if'
                    block_type = "if" if count == 0 else "else_if"

                    block = f"""
    {block_type} = {{
        limit = {{
            {indented_logic}
        }}
        set_variable = {{ name = debug_mission_{variable_counter} value = yes }}
    }}
"""
                    out.write(block)
                    count += 1
                    variable_counter += 1
                else:
                    # Optional: print if skipping due to no potential block
                    pass
                    
        except Exception as e:
            print(f"Error reading '{filename}': {e}")

    # --- FOOTER ---
    footer = """
    else_if = { #Manual Fixes
        limit = {
            OR = {
                tag = MRY
                tag = ARP
            }
        }
        set_variable = { name = debug_mission_manual value = yes }
    }

    else = {
        every_owned_province = {
            every_pops_in_province = {
                kill_pop = yes
            }
        }
    }
}"""
    out.write(footer)

print(f"Success! Processed {count} files into '{output_filename}'.")