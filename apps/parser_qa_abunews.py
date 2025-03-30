import os
import sys # Import sys for better error output

def clean_content(content):
    """
    Remove a starting '```json' and a trailing '```' from the content, if present.
    """
    start_marker = "```json"
    end_marker = "```"

    # Ensure content is a string before processing
    if not isinstance(content, str):
        print("Warning: Received non-string content, attempting to convert.", file=sys.stderr)
        try:
            content = str(content)
        except Exception as e:
            print(f"Error: Could not convert content to string: {e}", file=sys.stderr)
            return "" # Return empty string or handle as appropriate

    original_content = content # Keep original for comparison if needed

    if content.startswith(start_marker):
        content = content[len(start_marker):]
        # Use lstrip() cautiously, only remove leading whitespace if intended
        content = content.lstrip() # Removes leading whitespace like spaces, tabs, newlines

    if content.endswith(end_marker):
        # Ensure we don't remove the end marker if it was part of the actual content
        # This check is simple; more robust checks might be needed depending on data
        if len(content) >= len(end_marker):
             content = content[:-len(end_marker)]
             # Use rstrip() cautiously
             content = content.rstrip() # Removes trailing whitespace

    # Optional: Add a check if cleaning actually happened or was needed
    # if content != original_content:
    #     print("  Content cleaned.")
    # else:
    #     print("  No cleaning markers found or content unchanged.")

    return content

def main():
    folder1 = input("Enter the path to the source folder with subfolders: ").strip()
    folder2 = input("Enter the path to the destination folder where cleaned json files should be saved: ").strip()

    # Validate input paths
    if not os.path.isdir(folder1):
        print(f"Error: Source folder '{folder1}' not found or is not a directory.", file=sys.stderr)
        return # Exit if source folder is invalid

    # Ensure the destination folder exists
    try:
        os.makedirs(folder2, exist_ok=True)
        print(f"Ensured destination folder exists: {folder2}")
    except OSError as e:
        print(f"Error: Could not create destination folder '{folder2}': {e}", file=sys.stderr)
        return # Exit if destination folder cannot be created

    # Counters for summary
    processed_files_count = 0
    skipped_subfolders_count = 0
    error_count = 0

    print("\nStarting file search and processing...")

    # Iterate over items (subfolders primarily) in folder1
    for item_name in os.listdir(folder1):
        item_path = os.path.join(folder1, item_name)

        # Process only if it's a directory
        if os.path.isdir(item_path):
            subfolder_path = item_path
            subfolder_name = item_name # Keep the name for the output file
            print(f"\nProcessing subfolder: '{subfolder_name}'")

            # Look for the 'q&a.md' file within this subfolder
            found_qa_file = False
            for filename in os.listdir(subfolder_path):
                if filename.lower().endswith("q&a.md"): # Use lower() for case-insensitive matching
                    qa_file_path = os.path.join(subfolder_path, filename)
                    print(f"  Found matching file: {filename}")

                    # --- Process the found file ---
                    try:
                        with open(qa_file_path, "r", encoding="utf-8") as f_read:
                            original_content = f_read.read()

                        cleaned_json_content = clean_content(original_content)

                        # Define output file path using the subfolder name
                        output_filename = f"{subfolder_name}.json"
                        output_file_path = os.path.join(folder2, output_filename)

                        with open(output_file_path, "w", encoding="utf-8") as f_write:
                            f_write.write(cleaned_json_content)

                        print(f"  Successfully cleaned and saved to: {output_file_path}")
                        processed_files_count += 1
                        found_qa_file = True
                        # Assuming only one q&a.md per subfolder, break after finding and processing
                        break

                    except FileNotFoundError:
                        print(f"  Error: File not found during read attempt: {qa_file_path}", file=sys.stderr)
                        error_count += 1
                    except IOError as e:
                        print(f"  Error reading or writing file {filename}: {e}", file=sys.stderr)
                        error_count += 1
                    except Exception as e:
                        print(f"  An unexpected error occurred processing {filename}: {e}", file=sys.stderr)
                        error_count += 1
                    # --- End processing block ---

            # If the inner loop finished without finding the file
            if not found_qa_file:
                print(f"  No file ending with 'q&a.md' found in this subfolder.")
                skipped_subfolders_count += 1
        else:
            print(f"\nSkipping non-directory item: {item_name}")

    # --- Script Finish Summary ---
    print("\n--- Script Finished ---")
    print(f"Successfully processed and saved: {processed_files_count} file(s)")
    print(f"Subfolders skipped (no 'q&a.md' found): {skipped_subfolders_count}")
    print(f"Errors encountered: {error_count}")
    print(f"Cleaned files saved in: {folder2}")

if __name__ == "__main__":
    main()