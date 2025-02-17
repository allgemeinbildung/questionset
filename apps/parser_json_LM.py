import os

def clean_content(content):
    """
    Remove a starting '```json' and a trailing '```' from the content, if present.
    """
    start_marker = "```json"
    end_marker = "```"
    
    if content.startswith(start_marker):
        content = content[len(start_marker):].lstrip()
    if content.endswith(end_marker):
        content = content[:-len(end_marker)].rstrip()
    return content

def main():
    folder1 = input("Enter the path to folder1 with subfolders: ").strip()
    folder2 = input("Enter the path to folder2 where new json files should be saved: ").strip()
    
    # Prepare destination subdirectories
    mcqs_folder = os.path.join(folder2, "mcqs")
    summaries_folder = os.path.join(folder2, "summaries")
    os.makedirs(mcqs_folder, exist_ok=True)
    os.makedirs(summaries_folder, exist_ok=True)
    
    # Iterate over subfolders in folder1
    for subfolder in os.listdir(folder1):
        subfolder_path = os.path.join(folder1, subfolder)
        if os.path.isdir(subfolder_path):
            # Look for the mc and summary JSON files
            mc_file = None
            sum_file = None
            for file in os.listdir(subfolder_path):
                if file.endswith("_mc.json"):
                    mc_file = os.path.join(subfolder_path, file)
                elif file.endswith("_sum.json"):
                    sum_file = os.path.join(subfolder_path, file)
            
            # Process the mc file if found
            if mc_file:
                with open(mc_file, "r", encoding="utf-8") as f:
                    content = f.read()
                cleaned = clean_content(content)
                output_file_path = os.path.join(mcqs_folder, f"{subfolder}.json")
                with open(output_file_path, "w", encoding="utf-8") as f:
                    f.write(cleaned)
                print(f"Saved cleaned mc file to {output_file_path}")
            else:
                print(f"No mc file found in {subfolder_path}")
            
            # Process the summary file if found
            if sum_file:
                with open(sum_file, "r", encoding="utf-8") as f:
                    content = f.read()
                cleaned = clean_content(content)
                output_file_path = os.path.join(summaries_folder, f"{subfolder}.json")
                with open(output_file_path, "w", encoding="utf-8") as f:
                    f.write(cleaned)
                print(f"Saved cleaned summary file to {output_file_path}")
            else:
                print(f"No summary file found in {subfolder_path}")

if __name__ == "__main__":
    main()
