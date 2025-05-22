import whisper
from pathlib import Path
from typing import Optional
from config.settings import WHISPER_MODEL

class Transcriber:
    def __init__(self, model_name: str = WHISPER_MODEL):
        self.model_name = model_name
        self._model = None
    
    @property
    def model(self):
        """Lazy load the model."""
        if self._model is None:
            print(f"Loading Whisper model: {self.model_name}")
            self._model = whisper.load_model(self.model_name)
        return self._model
    
    def transcribe(self, audio_path: Path, language: Optional[str] = None) -> str:
        """
        Transcribe audio file to text.
        
        Args:
            audio_path: Path to audio file
            language: Optional language code (e.g., 'en')
            
        Returns:
            Transcribed text
        """
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        print(f"Transcribing: {audio_path}")
        result = self.model.transcribe(str(audio_path), language=language)
        return result["text"].strip()