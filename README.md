# Table of Contents

- [Table of Contents](#table-of-contents)
- [University Utils](#university-utils)
  - [Audio Transcription and Normalization (bulk\_transcription.py)](#audio-transcription-and-normalization-bulk_transcriptionpy)
    - [Requirements](#requirements)
    - [Usage](#usage)
  - [Markdown Tag Manager (bulk\_obsidian\_tagging.py)](#markdown-tag-manager-bulk_obsidian_taggingpy)
    - [Features](#features)
    - [Requirements](#requirements-1)
    - [Usage](#usage-1)
    - [Note](#note)

# University Utils

A bunch of code I wrote to aid me in my university courses

## Audio Transcription and Normalization (bulk_transcription.py)

This Python script provides functionality to transcribe audio files in `.m4a`/`.mp3` format to text using the Google Speech Recognition API in bulk. It also includes a step to normalize the audio files to -1.0dB before converting them to .wav format. All of the transcriptions are stored in a separate folder and combined into a `combined.txt` file containing all of them sorted.

### Requirements

The following is required to run the script:

- Python 3.x
- SpeechRecognition
- pydub
- tqdm
- openai_whisper
- torch

You can install these libraries using pip:

`pip install SpeechRecognition pydub tqdm openai_whisper torch`

### Usage

1. Place your .m4a/.mp3 audio files in the specified directory.
2. Run the script using the command python script.py.
3. The script will transcribe each `.m4a`/`.mp3` file to text using the Whisper API.
4. The transcriptions will be saved as `.txt` files in the same directory.
5. The script will also create a combined text file named `combined.txt` that contains the contents of all the individual .txt files.

## Markdown Tag Manager (bulk_obsidian_tagging.py)

A Python script to manage tags within the YAML front matter of Markdown files, specifically designed for bulk adding or removing tags in markdown files within a directory. This script is particularly useful for managing tags in Markdown files used in applications like Obsidian.

### Features

- **Add Tags**: Automatically adds a specified tag to the YAML front matter of all Markdown files in a given directory. If the file already contains the tag or lacks a front matter, the script intelligently updates or creates the necessary structure.
- **Remove Tags**: Removes a specified tag from the YAML front matter of all Markdown files in a given directory. If the tag isn't present in a file, the script skips it.

### Requirements

- Python 3.x

### Usage

1. Clone or Download the Script

2. Specify the Directory and Tag: In the script, replace `path/to/your/obsidian/folder` with the actual path to your directory containing Markdown files. Similarly, replace `yourtag` with the actual tag you want to add or remove.

   ```
   directory_path = "path/to/your/obsidian/folder" # Replace with your directory path
   tag = "yourtag" # Replace with your desired tag
   ```

3. Run the Script: Choose the operation you want to perform—adding or removing tags—and run the script.

To add a tag to all Markdown files in the specified directory:

`add_tag_to_files(directory_path, tag)`

To remove a tag from all Markdown files in the specified directory:

`remove_tag_from_files(directory_path, tag)`

### Note

This script operates directly on files in the specified directory. It's recommended to back up your Markdown files before running the script to prevent data loss.
