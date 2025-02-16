import os
import json
import tkinter as tk
from tkinter import filedialog

def select_folder(title):
    """Open a dialog to select a folder and return its path."""
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title=title)
    root.destroy()
    return folder

def extract_json(content, input_path):
    """
    Finds the first '{' in the content and attempts to decode a JSON object from that position.
    """
    start_index = content.find('{')
    if start_index == -1:
        print(f"No JSON object found in file {input_path}. Skipping file.")
        return None
    try:
        decoder = json.JSONDecoder()
        data, _ = decoder.raw_decode(content[start_index:])
        return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file {input_path}: {e}")
        return None

def process_file(input_path, output_dir):
    """
    Reads the file, extracts the JSON starting from the first '{', removes the "Verständnisfragen "
    prefix from the title, and saves the JSON with the cleaned title as filename.
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    data = extract_json(content, input_path)
    if data is None:
        return

    title = data.get("title")
    if not title:
        print(f"No title found in file {input_path}. Skipping file.")
        return

    # Remove the prefix "Verständnisfragen " if present.
    prefix = "Verständnisfragen "
    new_title = title[len(prefix):].strip() if title.startswith(prefix) else title.strip()

    # Construct a safe filename.
    new_filename = new_title + ".json"
    new_filename = "".join(c for c in new_filename if c.isalnum() or c in " ._-").strip()
    output_path = os.path.join(output_dir, new_filename)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Processed:\n  Input: {input_path}\n  Output: {output_path}\n")

def main():
    # Select the folder that contains subfolders with markdown files.
    input_folder = select_folder("Select the folder containing subfolders with md files")
    if not input_folder:
        print("No input folder selected. Exiting.")
        return

    # Select the folder to save the output JSON files.
    output_folder = select_folder("Select the folder to save output JSON files")
    if not output_folder:
        print("No output folder selected. Exiting.")
        return

    # Walk through the input folder and its subdirectories.
    for root_dir, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith("qa.md"):
                file_path = os.path.join(root_dir, file)
                process_file(file_path, output_folder)

if __name__ == "__main__":
    main()
