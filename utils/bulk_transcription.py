import os
import speech_recognition as sr
from pydub import AudioSegment
from tqdm import tqdm


def normalize_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    normalized_audio = audio.normalize(headroom=-1.0)
    return normalized_audio


def transcribe_audio_to_text(file_path):
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = r.record(source)
    return r.recognize_whisper(audio)


def bulk_transcribe_audio_to_text(directory_path):
    found_files = False  # Flag to check if audio files are found
    for file_name in tqdm(os.listdir(directory_path), desc="Transcribing", unit="file"):
        if file_name.endswith(".m4a") or file_name.endswith(".mp3"):
            found_files = True  # Set the flag to True if an audio file is found
            file_path = os.path.join(directory_path, file_name)
            wav_file_path = os.path.splitext(file_path)[0] + ".wav"
            audio = AudioSegment.from_file(file_path)
            audio.export(wav_file_path, format="wav")
            transcription = transcribe_audio_to_text(wav_file_path)
            txt_file_path = os.path.splitext(file_path)[0] + ".txt"
            # Create a folder based on the file category
            category_folder = os.path.join(
                directory_path, "categorized", file_name.split("_")[0]
            )
            os.makedirs(category_folder, exist_ok=True)
            txt_file_path = os.path.join(
                category_folder, os.path.basename(txt_file_path)
            )
            with open(txt_file_path, "w") as txt_file:
                txt_file.write(transcription)
    if not found_files:
        # No audio files were found; raise an error or print a message
        raise ValueError(f"No audio files (.m4a, .mp3) found in {directory_path}")
    else:
        print("\n--Finished transcribing files--\n")


def combine_txt_files(root_dir):
    # Create a list of all .txt files in the directory tree
    txt_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".txt"):
                txt_files.append(os.path.join(dirpath, filename))

    # Sort the list of .txt files by the number at the end of the filename
    txt_files.sort(
        key=lambda x: int("".join(filter(str.isdigit, os.path.splitext(x)[0][-2:])))
    )

    # Combine the contents of all .txt files into one giant .txt file
    combined_txt = ""
    for txt_file in txt_files:
        with open(txt_file, "r") as f:
            title = os.path.splitext(os.path.basename(txt_file))[0]
            combined_txt += f"\n\n --{title}-- \n\n"
            combined_txt += f.read()

    # Write the combined .txt file to disk
    with open(os.path.join(root_dir, "combined.txt"), "w") as f:
        f.write(combined_txt)
    print("\n--Files have been combined--\n")


# Example usage
directory_path = "/Users/username/Downloads"
bulk_transcribe_audio_to_text(directory_path)
combine_txt_files(directory_path)
