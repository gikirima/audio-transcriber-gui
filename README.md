# Audio Transcriber GUI

## Overview
The Audio Transcriber GUI is a Python application designed to transcribe audio files into text. It supports various audio formats and provides a user-friendly interface for converting audio files to WAV format, selecting the language for transcription, and saving the transcription results.

## Features
- Convert audio files from various formats to WAV.
- Drag and drop functionality for easy file selection.
- Browse functionality to select audio files.
- Language selection for transcription.
- Automatic saving of transcription results.

## Project Structure
```
audio-transcriber-gui
├── src
│   ├── main.py          # Entry point of the application
│   ├── gui.py           # GUI management and functionality
│   ├── audio_utils.py    # Audio file manipulation functions
│   ├── transcriber.py    # Transcription handling
│   └── languages.py      # Supported languages for transcription
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Installation
To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd audio-transcriber-gui
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```
   python src/main.py
   ```

2. Use the browse button to select an audio file.

3. Choose the desired model and language for transcription from the dropdown menu.

4. Click the 'Transcribe' button to start the transcription process.

5. The transcription result will be automatically saved to a text file in the same directory as the audio file.

## Dependencies
The project requires the following Python libraries:
- `openai-whisper`
- `ffmpeg-python`

Make sure to install these libraries using the `requirements.txt` file provided.
