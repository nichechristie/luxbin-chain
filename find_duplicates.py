import hashlib
import os
import sys
from collections import defaultdict

def find_duplicates(directory):
    hashes = defaultdict(list)
    file_count = 0
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.startswith("luxbin_") and filename.endswith(".md"):
                file_count += 1
                path = os.path.join(dirpath, filename)
                try:
                    with open(path, 'rb') as f:
                        filehash = hashlib.md5(f.read()).hexdigest()
                    print(f"File: {path}, Hash: {filehash}") # Added for debugging
                    hashes[filehash].append(path)
                except IOError as e:
                    print(f"Could not read file {path}: {e}", file=sys.stderr)
    
    print(f"Found {file_count} files matching the pattern.")
    
    duplicates = []
    for file_list in hashes.values():
        if len(file_list) > 1:
            duplicates.append(file_list)
            
    return duplicates

if __name__ == "__main__":
    duplicates = find_duplicates(".")
    if duplicates:
        print("Duplicate files found:")
        for group in duplicates:
            print("---")
            # Sort the files in each group for consistent output
            for file in sorted(group):
                print(file)