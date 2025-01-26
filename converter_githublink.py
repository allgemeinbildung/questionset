import os

def get_root_path():
    """Prompt the user to enter the root folder path and validate it."""
    while True:
        root_path = input("Enter the path to the root folder: ").strip('"').strip("'")
        if os.path.isdir(root_path):
            return root_path
        else:
            print(f"Error: '{root_path}' is not a valid directory. Please try again.\n")

def replace_url_in_file(file_path, old_url, new_url):
    """
    Replace occurrences of old_url with new_url in the specified file.

    Args:
        file_path (str): Path to the file to be modified.
        old_url (str): The URL string to be replaced.
        new_url (str): The new URL string to replace with.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        if old_url not in content:
            print(f"No occurrences found in '{file_path}'. Skipping.")
            return

        new_content = content.replace(old_url, new_url)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

        print(f"Updated '{file_path}'.")
    except Exception as e:
        print(f"Failed to process '{file_path}'. Error: {e}")

def main():
    root_path = get_root_path()
    old_url = "https://aburossi.github.io/html/multiboxMC/mc_template.html?"
    new_url = "https://allgemeinbildung.github.io/questionset/index.html?"

    # Walk through the directory tree
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.startswith('1. '):
                file_path = os.path.join(dirpath, filename)
                replace_url_in_file(file_path, old_url, new_url)

    print("\nURL replacement completed.")

if __name__ == "__main__":
    main()
