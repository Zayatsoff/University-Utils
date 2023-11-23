import os
from typing import AnyStr


def add_tag_to_files(directory: AnyStr, tag: AnyStr) -> None:
    """
    Adds a given tag to all markdown files in the specified directory.

    :param directory: Path to the directory containing markdown files.
    :param tag: Tag to be added to the files.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r+", encoding="utf-8") as f:
                    content = f.read()
                    if tag not in content:
                        f.write("\n" + tag)


# Example usage
directory_path = "/Users/liorrozin/Library/Mobile Documents/iCloud~md~obsidian/Documents/CU/CRCJ 1000 B"  # Replace with the path to your Obsidian folder
tag = "#Crime"  # Replace with your desired tag
add_tag_to_files(directory_path, tag)
