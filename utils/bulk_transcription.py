import sys

print(sys.executable)
import os
import speech_recognition as sr
from pydub import AudioSegment
from tqdm import tqdm
from datetime import timedelta


def format_timestamp(milliseconds):
    """Convert milliseconds to SRT timestamp format: HH:MM:SS,mmm"""
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def create_subtitle_block(index, start_time, end_time, text):
    """Create a properly formatted SRT subtitle block"""
    return f"{index}\n{start_time} --> {end_time}\n{text}\n\n"


def transcribe_audio_to_srt(file_path, chunk_duration=3000):  # 3 seconds per subtitle
    r = sr.Recognizer()
    audio = AudioSegment.from_file(file_path)

    chunks = []
    for i in range(0, len(audio), chunk_duration):
        chunk = audio[i : i + chunk_duration]
        chunk_path = "temp_chunk.wav"
        chunk.export(chunk_path, format="wav")

        with sr.AudioFile(chunk_path) as source:
            audio_chunk = r.record(source)
            try:
                text = r.recognize_whisper(audio_chunk)
                if text.strip():  # Only add non-empty transcriptions
                    start_time = format_timestamp(i)
                    end_time = format_timestamp(min(i + chunk_duration, len(audio)))
                    chunks.append((start_time, end_time, text))
            except sr.UnknownValueError:
                pass

        os.remove(chunk_path)

    return chunks


def bulk_transcribe_to_srt(directory_path):
    found_files = False

    for file_name in tqdm(os.listdir(directory_path), desc="Transcribing", unit="file"):
        if file_name.endswith((".m4a", ".mp3")):
            found_files = True
            file_path = os.path.join(directory_path, file_name)

            # Create SRT file path
            srt_file_path = os.path.splitext(file_path)[0] + ".srt"

            # Create category folder
            category_folder = os.path.join(
                directory_path, "categorized", file_name.split("_")[0]
            )
            os.makedirs(category_folder, exist_ok=True)

            # Update SRT file path to be in category folder
            srt_file_path = os.path.join(
                category_folder, os.path.basename(srt_file_path)
            )

            # Generate subtitles
            subtitle_chunks = transcribe_audio_to_srt(file_path)

            # Write SRT file
            with open(srt_file_path, "w", encoding="utf-8") as srt_file:
                for i, (start_time, end_time, text) in enumerate(subtitle_chunks, 1):
                    srt_file.write(create_subtitle_block(i, start_time, end_time, text))

    if not found_files:
        raise ValueError(f"No audio files (.m4a, .mp3) found in {directory_path}")
    else:
        print("\n--Finished generating subtitles--\n")


def combine_srt_files(root_dir):
    srt_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".srt"):
                srt_files.append(os.path.join(dirpath, filename))

    srt_files.sort(
        key=lambda x: int("".join(filter(str.isdigit, os.path.splitext(x)[0][-2:])))
    )

    total_subtitle_count = 0
    combined_srt = ""

    for srt_file in srt_files:
        with open(srt_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                title = os.path.splitext(os.path.basename(srt_file))[0]
                combined_srt += f"\n{total_subtitle_count + 1}\n"
                combined_srt += "00:00:00,000 --> 00:00:02,000\n"
                combined_srt += f"-- {title} --\n\n"

                # Update subtitle numbers and add content
                lines = content.split("\n")
                i = 0
                while i < len(lines):
                    if lines[i].strip().isdigit():
                        total_subtitle_count += 1
                        lines[i] = str(total_subtitle_count)
                        combined_srt += "\n".join(lines[i : i + 4])
                    i += 1

    with open(os.path.join(root_dir, "combined.srt"), "w", encoding="utf-8") as f:
        f.write(combined_srt)

    print("\n--SRT files have been combined--\n")


if __name__ == "__main__":
    directory_path = "/Users/liorrozin/"
    bulk_transcribe_to_srt(directory_path)
    combine_srt_files(directory_path)
