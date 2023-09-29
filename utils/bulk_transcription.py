import os
import speech_recognition as sr
from pydub import AudioSegment
from tqdm import tqdm


def transcribe_m4a_to_text(file_path):
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = r.record(source)
    return r.recognize_google(audio)


def bulk_transcribe_m4a_to_text(directory_path):
    for file_name in tqdm(os.listdir(directory_path), desc="Transcribing", unit="file"):
        if file_name.endswith(".m4a"):
            file_path = os.path.join(directory_path, file_name)
            wav_file_path = os.path.splitext(file_path)[0] + ".wav"
            AudioSegment.from_file(file_path).export(wav_file_path, format="wav")
            transcription = transcribe_m4a_to_text(wav_file_path)
            txt_file_path = os.path.splitext(file_path)[0] + ".txt"
            with open(txt_file_path, "w") as txt_file:
                txt_file.write(transcription)


# Example usage
directory_path = "/Users/liorrozin/Downloads/ppt/ppt/media/"
bulk_transcribe_m4a_to_text(directory_path)
