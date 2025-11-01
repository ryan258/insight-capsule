import whisper
from pathlib import Path
from typing import Optional
from config.settings import WHISPER_MODEL
from core.exceptions import TranscriptionError
from core.logger import setup_logger

logger = setup_logger(__name__)


class Transcriber:
    """Handles audio transcription using OpenAI's Whisper model."""

    def __init__(self, model_name: str = WHISPER_MODEL):
        """
        Initialize the transcriber.

        Args:
            model_name: Whisper model size (tiny, base, small, medium, large)
        """
        self.model_name = model_name
        self._model = None
        logger.info(f"Transcriber initialized with model: {model_name}")

    @property
    def model(self):
        """Lazy load the Whisper model."""
        if self._model is None:
            try:
                logger.info(f"Loading Whisper model: {self.model_name}")
                print(f"Loading Whisper model: {self.model_name}")
                self._model = whisper.load_model(self.model_name)
                logger.info("Whisper model loaded successfully")
            except Exception as e:
                error_msg = f"Failed to load Whisper model '{self.model_name}': {e}"
                logger.error(error_msg, exc_info=True)
                raise TranscriptionError(error_msg) from e
        return self._model

    def transcribe(self, audio_path: Path, language: Optional[str] = None) -> str:
        """
        Transcribe audio file to text.

        Args:
            audio_path: Path to audio file
            language: Optional language code (e.g., 'en')

        Returns:
            Transcribed text

        Raises:
            TranscriptionError: If transcription fails
        """
        if not audio_path.exists():
            error_msg = f"Audio file not found: {audio_path}"
            logger.error(error_msg)
            raise TranscriptionError(error_msg)

        try:
            logger.info(f"Starting transcription: {audio_path}")
            print(f"Transcribing: {audio_path}")

            result = self.model.transcribe(str(audio_path), language=language)
            transcript = result["text"].strip()

            logger.info(
                f"Transcription complete: {len(transcript)} characters, "
                f"{len(transcript.split())} words"
            )

            if not transcript:
                logger.warning("Transcription resulted in empty text")

            return transcript

        except Exception as e:
            error_msg = f"Transcription failed for {audio_path}: {e}"
            logger.error(error_msg, exc_info=True)
            raise TranscriptionError(error_msg) from e