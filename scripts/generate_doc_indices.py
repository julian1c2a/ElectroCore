import os
import json

def create_doc_indices(root_path):
    """
    Walks through the directory tree from root_path.
    For each directory, it creates:
    1. A JSON file next to it (in the parent dir) named after the directory.
    2. An 'index.json' file inside it, listing all .md files.
    """
    for dirpath, dirnames, filenames in os.walk(root_path):
        print(f"Processing directory: {dirpath}")

        # Create index.json inside the current directory
        md_files = sorted([f for f in filenames if f.endswith('.md')])
        content_data = {"files": md_files if md_files else []}
        content_json_path = os.path.join(dirpath, 'index.json')

        try:
            with open(content_json_path, 'w', encoding='utf-8') as f:
                json.dump(content_data, f, indent=4, ensure_ascii=False)
            print(f"  -> Created: {content_json_path}")
        except IOError as e:
            print(f"  -> Error writing to {content_json_path}: {e}")

        # For each subdirectory found, create a corresponding .json file alongside it.
        for dirname in dirnames:
            dir_metadata = {
                "name": dirname,
                "type": "directory"
            }
            dir_json_path = os.path.join(dirpath, f"{dirname}.json")
            try:
                with open(dir_json_path, 'w', encoding='utf-8') as f:
                    json.dump(dir_metadata, f, indent=4, ensure_ascii=False)
                print(f"  -> Created: {dir_json_path}")
            except IOError as e:
                print(f"  -> Error writing to {dir_json_path}: {e}")

if __name__ == '__main__':
    target_directory = os.path.join('docs', 'temario')
    if os.path.isdir(target_directory):
        create_doc_indices(target_directory)
        print("\nScript finished.")
    else:
        print(f"Error: Target directory '{target_directory}' not found.")
