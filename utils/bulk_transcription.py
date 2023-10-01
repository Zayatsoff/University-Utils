import os
import speech_recognition as sr
from pydub import AudioSegment
from tqdm import tqdm


def normalize_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    normalized_audio = audio.normalize(headroom=-1.0)
    return normalized_audio


def transcribe_m4a_to_text(file_path):
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = r.record(source)
    return r.recognize_whisper(audio)


def bulk_transcribe_m4a_to_text(directory_path):
    for file_name in tqdm(os.listdir(directory_path), desc="Transcribing", unit="file"):
        if file_name.endswith(".m4a"):
            file_path = os.path.join(directory_path, file_name)
            wav_file_path = os.path.splitext(file_path)[0] + ".wav"
            normalized_audio = normalize_audio(file_path)
            normalized_audio.export(wav_file_path, format="wav")
            transcription = transcribe_m4a_to_text(wav_file_path)
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


def combine_txt_files(directory_path):
    combined_file_path = os.path.join(directory_path, "combined.txt")
    with open(combined_file_path, "w") as combined_file:
        for file_name in os.listdir(directory_path):
            if file_name.endswith(".txt"):
                file_path = os.path.join(directory_path, file_name)
                with open(file_path, "r") as txt_file:
                    combined_file.write(txt_file.read())
                combined_file.write("\n")


# Example usage
directory_path = "/Users/liorrozin/Downloads/ppt/ppt/media/"
bulk_transcribe_m4a_to_text(directory_path)
combine_txt_files(directory_path)
