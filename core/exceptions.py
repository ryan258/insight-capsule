"""Custom exceptions for the Insight Capsule application."""

class InsightCapsuleError(Exception):
    """Base exception for all Insight Capsule errors."""
    pass

class AudioRecordingError(InsightCapsuleError):
    """Error during audio recording."""
    pass

class TranscriptionError(InsightCapsuleError):
    """Error during audio transcription."""
    pass

class GPTGenerationError(InsightCapsuleError):
    """Error during GPT text generation."""
    pass

class StorageError(InsightCapsuleError):
    """Error during file storage operations."""
    pass

class TTSError(InsightCapsuleError):
    """Error during text-to-speech operations."""
    pass