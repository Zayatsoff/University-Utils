import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import platform
from tqdm import tqdm
import tempfile
import shutil
import mlx_whisper


def select_folder():
    """Prompt user to select a folder for processing (works on both macOS and Windows)"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Make sure the dialog appears in front (important for macOS)
    root.attributes("-topmost", True)

    folder_path = filedialog.askdirectory(title="Select folder containing media files")
    root.destroy()
    return folder_path


def check_dependencies():
    """Check for required dependencies"""
    try:
        import mlx_whisper
        from pydub import AudioSegment
    except ImportError as e:
        messagebox.showerror(
            "Missing Dependencies",
            f"Please install required packages: {str(e)}\n\nRun: pip install mlx-whisper pydub tqdm",
        )
        sys.exit(1)

    # Check for FFmpeg (required by both pydub and for video conversion)
    try:
        if platform.system() == "Windows":
            subprocess.run(
                ["where", "ffmpeg"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        else:  # macOS/Linux
            subprocess.run(
                ["which", "ffmpeg"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
    except subprocess.CalledProcessError:
        messagebox.showerror(
            "Missing FFmpeg",
            "FFmpeg is required but not found in PATH.\n"
            "Please install FFmpeg and make sure it's in your system PATH.",
        )
        sys.exit(1)


def convert_video_to_audio(video_path, audio_path):
    """Convert video file (MP4/MOV) to audio file (MP3) using FFmpeg directly"""
    try:
        # Using FFmpeg directly is more reliable across platforms
        command = [
            "ffmpeg",
            "-i",
            video_path,
            "-q:a",
            "0",  # Best quality
            "-map",
            "a",  # Extract audio only
            "-hide_banner",
            "-loglevel",
            "error",
            audio_path,
        ]

        subprocess.run(
            command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return True
    except Exception as e:
        print(f"Error converting {video_path}: {str(e)}")
        return False


def transcribe_with_mlx_whisper(audio_path):
    """Transcribe audio file using mlx-whisper with the large-v3-turbo model"""
    try:
        # Using the whisper-large-v3-turbo model optimized for Apple Silicon
        result = mlx_whisper.transcribe(
            audio_path, path_or_hf_repo="mlx-community/whisper-large-v3-turbo"
        )
        return result["text"]
    except Exception as e:
        print(f"Error transcribing {audio_path}: {str(e)}")
        return ""


def process_files(input_folder):
    """Process all media files in the given folder"""
    # Create output folder for transcripts
    transcript_folder = os.path.join(input_folder, "transcripts")
    os.makedirs(transcript_folder, exist_ok=True)

    # Create temp folder for audio conversions - use system temp for better cross-platform support
    temp_folder = tempfile.mkdtemp(prefix="media_transcribe_")

    try:
        # Get all files in the directory
        files = [
            f
            for f in os.listdir(input_folder)
            if os.path.isfile(os.path.join(input_folder, f)) and not f.startswith(".")
        ]  # Skip hidden files

        # Filter to only media files we can process
        media_files = [
            f
            for f in files
            if os.path.splitext(f)[1].lower() in [".mp4", ".mov", ".mp3", ".wav"]
        ]

        if not media_files:
            print("No media files found to process.")
            return

        print("First run will download the model - this may take a few minutes...")

        # Process files with progress bar
        for file in tqdm(media_files, desc="Processing files"):
            file_path = os.path.join(input_folder, file)
            file_extension = os.path.splitext(file)[1].lower()
            file_name = os.path.splitext(file)[0]

            # Process based on file type
            if file_extension in [".mp4", ".mov"]:
                # Convert video to audio first
                temp_audio_path = os.path.join(temp_folder, f"{file_name}.mp3")

                print(f"Converting {file} to audio...")
                if convert_video_to_audio(file_path, temp_audio_path):
                    # Transcribe the audio
                    print(f"Transcribing {file}...")
                    transcript = transcribe_with_mlx_whisper(temp_audio_path)

                    # Save transcript
                    transcript_path = os.path.join(
                        transcript_folder, f"{file_name}.txt"
                    )
                    with open(transcript_path, "w", encoding="utf-8") as f:
                        f.write(transcript)

                    print(f"Saved transcript for {file}")

            elif file_extension in [".mp3", ".wav"]:
                # Directly transcribe audio file
                print(f"Transcribing {file}...")
                transcript = transcribe_with_mlx_whisper(file_path)

                # Save transcript
                transcript_path = os.path.join(transcript_folder, f"{file_name}.txt")
                with open(transcript_path, "w", encoding="utf-8") as f:
                    f.write(transcript)

                print(f"Saved transcript for {file}")

    finally:
        # Clean up temp files
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder, ignore_errors=True)

    print(f"\nTranscription complete! Transcripts saved to: {transcript_folder}")


if __name__ == "__main__":
    print(f"Media Transcription Tool (Running on {platform.system()})")
    print("------------------------")

    # Check for dependencies first
    check_dependencies()

    # Get folder from user
    folder_path = select_folder()

    if folder_path:
        print(f"Selected folder: {folder_path}")
        process_files(folder_path)
    else:
        print("No folder selected. Exiting.")
