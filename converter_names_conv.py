import os
import sys

def get_root_path():
    """Prompt the user to enter the root folder path and validate it."""
    while True:
        root_path = input("Enter the path to the root folder: ").strip('"').strip("'")
        if os.path.isdir(root_path):
            return root_path
        else:
            print(f"Error: '{root_path}' is not a valid directory. Please try again.\n")

def rename_files(root_path, prefix='converted_'):
    """
    Rename files that start with the given prefix by removing the prefix.

    Args:
        root_path (str): The root directory to start searching from.
        prefix (str): The prefix to identify files to rename.
    """
    files_renamed = 0
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.startswith(prefix):
                old_file_path = os.path.join(dirpath, filename)
                new_filename = filename[len(prefix):]  # Remove the prefix
                new_file_path = os.path.join(dirpath, new_filename)
                
                # Check if the new file name already exists to avoid overwriting
                if os.path.exists(new_file_path):
                    print(f"Warning: '{new_file_path}' already exists. Skipping renaming of '{old_file_path}'.")
                    continue
                
                try:
                    os.rename(old_file_path, new_file_path)
                    print(f"Renamed: '{old_file_path}' -> '{new_file_path}'")
                    files_renamed += 1
                except Exception as e:
                    print(f"Failed to rename '{old_file_path}'. Error: {e}")
    
    print(f"\nTotal files renamed: {files_renamed}")

def main():
    print("=== File Renaming Utility ===\n")
    root_path = get_root_path()
    rename_files(root_path)
    print("\nFile renaming process completed.")

if __name__ == "__main__":
    main()
