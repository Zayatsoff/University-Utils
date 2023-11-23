import os
from typing import AnyStr


def add_tag_to_files(directory: AnyStr, tag: AnyStr) -> None:
    """
    Adds a given tag to the YAML front matter at the beginning of all markdown files in the specified directory.
    If the tag is already present, it skips the file. If the front matter does not exist, it creates one.

    :param directory: Path to the directory containing markdown files.
    :param tag: Tag to be added to the files.
    """
    tag_line = f"  - {tag}\n"
    front_matter_start = "---\n"
    front_matter_end = "---\n"
    front_matter = f"{front_matter_start}tags:\n{tag_line}{front_matter_end}"

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r+", encoding="utf-8") as f:
                    content = f.read()
                    if tag_line in content:
                        print(f"Tag '{tag}' already exists in {file}")
                        continue

                    if front_matter_start in content:
                        start_index = content.find(front_matter_start)
                        end_index = content.find(
                            front_matter_end, start_index + len(front_matter_start)
                        ) + len(front_matter_end)
                        front_matter_content = content[start_index:end_index]

                        if "tags:" in front_matter_content:
                            tags_index = front_matter_content.find("tags:") + len(
                                "tags:\n"
                            )
                            updated_front_matter = (
                                front_matter_content[:tags_index]
                                + tag_line
                                + front_matter_content[tags_index:]
                            )
                        else:
                            updated_front_matter = (
                                front_matter_content.rstrip("\n")
                                + "tags:\n"
                                + tag_line
                                + front_matter_end
                            )

                        updated_content = (
                            content[:start_index]
                            + updated_front_matter
                            + content[end_index:]
                        )
                    else:
                        updated_content = front_matter + content

                    f.seek(0)
                    f.write(updated_content)
                    f.truncate()


def remove_tag_from_files(directory: AnyStr, tag: AnyStr) -> None:
    """
    Removes a given tag from the YAML front matter at the beginning of all markdown files in the specified directory.
    If the tag is not present, it skips the file.

    :param directory: Path to the directory containing markdown files.
    :param tag: Tag to be removed from the files.
    """
    tag_line = f"  - {tag}\n"
    front_matter_start = "---\n"
    front_matter_end = "---\n"

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r+", encoding="utf-8") as f:
                    content = f.read()
                    if tag_line not in content:
                        print(f"Tag '{tag}' does not exist in {file}")
                        continue

                    start_index = content.find(front_matter_start)
                    if start_index != -1:
                        end_index = content.find(
                            front_matter_end, start_index + 1
                        ) + len(front_matter_end)
                        front_matter_content = content[start_index:end_index]

                        updated_front_matter = front_matter_content.replace(
                            tag_line, ""
                        )
                        updated_content = updated_front_matter + content[end_index:]

                        f.seek(0)
                        f.write(updated_content)
                        f.truncate()


# Example usage
directory_path = (
    "path/to/your/obsidian/folder"  # Replace with the path to your Obsidian folder
)
tag = "yourtag"  # Replace with your desired tag (without the hash symbol)

# To add the tag
add_tag_to_files(directory_path, tag)

# To remove the tag
# remove_tag_from_files(directory_path, tag)
