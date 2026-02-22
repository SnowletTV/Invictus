import os
import re

def count_deities_in_directory(directory_path):
    # This pattern looks for strings starting with "deity_" followed by alphanumeric characters,
    # then an equals sign and an opening brace.
    # It accounts for whitespace and ensures the line isn't commented out (doesn't start with #).
    deity_pattern = re.compile(r'^\s*(?!#)deity_\w+\s*=\s*\{', re.MULTILINE)
    
    total_deities = 0
    files_processed = 0

    print(f"Scanning directory: {directory_path}\n")

    # Check if directory exists
    if not os.path.exists(directory_path):
        print(f"Error: The directory '{directory_path}' was not found.")
        return

    # Loop through all files in the folder
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            files_processed += 1
            
            try:
                # Paradox files usually use UTF-8-SIG (UTF-8 with BOM) or standard UTF-8
                with open(file_path, 'r', encoding='utf-8-sig', errors='ignore') as file:
                    content = file.read()
                    
                    # Find all matches in the file
                    matches = deity_pattern.findall(content)
                    count = len(matches)
                    
                    if count > 0:
                        print(f"Found {count} deities in: {filename}")
                        total_deities += count
                        
            except Exception as e:
                print(f"Could not read file {filename}: {e}")

    print("-" * 30)
    print(f"Scan complete.")
    print(f"Files scanned: {files_processed}")
    print(f"Total deities found: {total_deities}")

if __name__ == "__main__":
    # The path you provided
    target_path = r"C:\Users\bab\Documents\Paradox Interactive\Imperator\mod\invictus\common\deities"
    
    count_deities_in_directory(target_path)