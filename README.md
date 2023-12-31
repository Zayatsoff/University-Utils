# University Utils
 A bunch of code I wrote to aid me in my university courses


## Audio Transcription and Normalization (bulk_transcription.py)
This Python script provides functionality to transcribe audio files in .m4a/.mp3 format to text using the Google Speech Recognition API in bulk. It also includes a step to normalize the audio files to -1.0dB before converting them to .wav format. All of the transcriptions are stored in sperate folder, and combined into a "combined.txt" file conteaining all of them, sorted.

### Requirements
The following libraries are required to run the script:

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
3. The script will transcribe each .m4a/.mp3 file to text using the Whisper API.
4. The transcriptions will be saved as .txt files in the same directory.
5. The script will also create a combined text file named combined.txt that contains the contents of all the individual .txt files.