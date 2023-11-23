import os
from typing import AnyStr


def add_tag_to_files(directory: AnyStr, tag: AnyStr) -> None:
    """
    Adds a given tag to the YAML front matter at the beginning of all markdown files in the specified directory.
    If the front matter does not exist, it creates one. If the tag is already present, it skips the file.

    :param directory: Path to the directory containing markdown files.
    :param tag: Tag to be added to the files.
    """
    tag_line = f"  - {tag}\n"
    front_matter = f"---\ntags:\n{tag_line}---\n"

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r+", encoding="utf-8") as f:
                    content = f.read()
                    if tag_line in content:
                        print(f"Tag already exists in {file}")
                        continue
                    if content.startswith("---"):
                        insertion_point = content.find("---", 1) + 4
                        updated_content = (
                            content[:insertion_point]
                            + tag_line
                            + content[insertion_point:]
                        )
                    else:
                        updated_content = front_matter + content
                    f.seek(0)
                    f.write(updated_content)
                    f.truncate()


# Example usage
directory_path = (
    "path/to/your/obsidian/folder"  # Replace with the path to your Obsidian folder
)
tag = "yourtag"  # Replace with your desired tag (without the hash symbol)
add_tag_to_files(directory_path, tag)
