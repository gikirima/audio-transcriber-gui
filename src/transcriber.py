import os
import sys

def resource_path(relative_path):
    # Untuk akses file di bundle PyInstaller
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

class Transcriber:
    def __init__(self, model_name="turbo"):
        import whisper
        # Cek apakah file model lokal ada di folder models
        local_model_path = os.path.join("models", f"{model_name}.pt")
        if os.path.exists(local_model_path):
            self.model = whisper.load_model(local_model_path)
        else:
            self.model = whisper.load_model(model_name)

    def transcribe(self, audio_path, language="id"):
        result = self.model.transcribe(
            audio_path,
            language=language,
            verbose=False,
            task="transcribe"
        )
        return result["text"]