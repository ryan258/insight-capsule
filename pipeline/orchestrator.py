# pipeline/orchestrator.py
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, Callable
import threading
# import json # No longer needed for brief_json here

from core.audio import AudioRecorder
from core.transcription import Transcriber
from core.tts import TextToSpeech
from core.storage import StorageManager
# from agents.clarifier import ClarifierAgent # ClarifierAgent is no longer used
from agents.synthesizer import SynthesizerAgent
from config.settings import AUDIO_DIR, AUDIO_FILENAME
from core.logger import setup_logger

from core.local_generation import HybridGenerator

logger = setup_logger(__name__)


class InsightPipeline:
    """
    Long-running service for capturing and processing voice insights.
    Can be triggered on-demand and run in the background.
    """
    def __init__(self, use_local: bool = True): # use_local can still determine HybridGenerator preference
        self.audio_recorder = AudioRecorder()
        self.transcriber = Transcriber()

        self.generator = HybridGenerator(prefer_local=use_local)

        self.tts = TextToSpeech()
        self.storage = StorageManager()
        # self.clarifier = ClarifierAgent(self.generator) # Removed
        self.synthesizer = SynthesizerAgent(self.generator) # Synthesizer uses the same generator

        # State management for long-running service
        self._is_recording = False
        self._is_processing = False
        self._recording_thread = None
        self._processing_thread = None
        self._state_lock = threading.Lock()

        # Callbacks for state changes
        self.on_recording_start: Optional[Callable[[], None]] = None
        self.on_recording_stop: Optional[Callable[[], None]] = None
        self.on_processing_start: Optional[Callable[[], None]] = None
        self.on_processing_complete: Optional[Callable[[Dict[str, Any]], None]] = None
        self.on_error: Optional[Callable[[str], None]] = None
        
    def _generate_simple_title(self, text: str, max_length: int = 5) -> str:
        """Generates a simple title from the first few words of a text."""
        if not text.strip():
            return "Untitled Insight"
        words = text.split()
        title = " ".join(words[:max_length])
        if len(words) > max_length:
            title += "..."
        return title

    def run(self, audio_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Run the complete insight generation pipeline.
        
        Args:
            audio_path: Optional pre-recorded audio file
            
        Returns:
            Dict with results from each stage
        """
        results = {
            "success": False,
            "audio_path": None,
            "transcript": None,
            # "brief": None, # Brief removed
            "title": "Untitled Insight", # Added title to results
            "capsule": None,
            "log_path": None,
            "error": None
        }
        
        try:
            # Step 1: Audio Recording (if needed)
            if audio_path is None:
                audio_path = AUDIO_DIR / AUDIO_FILENAME
                success_recording = self.audio_recorder.record_to_file(
                    audio_path,
                    on_start=lambda: self.tts.speak("Recording started"),
                    on_stop=lambda: self.tts.speak("Recording complete. Processing audio.")
                )
                if not success_recording: # Check the return value
                    raise Exception("Audio recording failed or was cancelled")
            
            results["audio_path"] = str(audio_path)
            
            # Step 2: Transcription
            self.tts.speak("Transcribing audio")
            transcript = self.transcriber.transcribe(audio_path)
            results["transcript"] = transcript
            
            processed_transcript = transcript # Keep original for results
            if not transcript.strip():
                self.tts.speak("Transcript is empty")
                # Provide a placeholder if you want to continue processing
                # or raise an error to stop.
                processed_transcript = "User provided silent or very short audio." 
            else:
                self.tts.speak("Transcription complete")
            
            # Step 3: Generate Capsule (directly from transcript)
            # Brief generation step is removed
            # self.tts.speak("Generating creative brief locally") # Removed
            # brief = self.clarifier.generate_brief(processed_transcript) # Removed
            # results["brief"] = brief # Removed
            # self.tts.speak("Creative brief generated") # Removed
            
            # Generate a simple title from the transcript for logging purposes
            # This can be refined later.
            log_title = self._generate_simple_title(transcript)
            results["title"] = log_title

            self.tts.speak("Generating insight capsule")
            capsule = self.synthesizer.generate_capsule(processed_transcript) # No brief passed
            results["capsule"] = capsule
            self.tts.speak("Insight capsule generated") # Added feedback
            
            # Step 4: Save Everything
            tags = self.storage.extract_tags_from_text(transcript)
            timestamp = datetime.now()
            
            # Save brief step removed
            # brief_json = json.dumps(brief, indent=2) if isinstance(brief, dict) else str(brief) # Removed
            # self.storage.save_brief(brief, brief.get("title", "Untitled"), timestamp) # Removed
            
            # Save log
            log_path = self.storage.save_log(
                title=log_title, # Use the generated title
                transcript=transcript,
                # brief=None, # Pass None or an empty string for the brief parameter
                capsule=capsule,
                tags=tags,
                timestamp=timestamp
            )
            results["log_path"] = str(log_path)
            
            # Step 5: Speak Result
            self.tts.speak("Here is your insight capsule")
            if capsule and "error" not in capsule.lower() and "skipped" not in capsule.lower():
                 self.tts.speak(capsule)
            elif not capsule:
                 self.tts.speak("The insight capsule is empty.")
            else:
                 self.tts.speak("The insight capsule contains an error or was based on empty input.")

            results["success"] = True
            print("\n🎉 Pipeline completed successfully!")

        except Exception as e:
            results["error"] = str(e)
            print(f"\n🔴 Pipeline error: {e}")
            self.tts.speak("An error occurred during processing")

        return results

    # === New methods for long-running service ===

    @property
    def is_recording(self) -> bool:
        """Check if currently recording."""
        with self._state_lock:
            return self._is_recording

    @property
    def is_processing(self) -> bool:
        """Check if currently processing."""
        with self._state_lock:
            return self._is_processing

    @property
    def is_busy(self) -> bool:
        """Check if recording or processing."""
        with self._state_lock:
            return self._is_recording or self._is_processing

    def start_recording_async(self) -> bool:
        """
        Start recording asynchronously (non-blocking).
        Returns True if recording started, False if already busy.
        """
        with self._state_lock:
            if self._is_recording or self._is_processing:
                logger.warning("Cannot start recording: already busy")
                return False

        # Set up silence detection callback
        self.audio_recorder._on_silence_detected = self._on_silence_auto_stop

        # Start the actual audio recording
        if not self.audio_recorder.start_recording():
            logger.error("Failed to start audio recording")
            return False

        with self._state_lock:
            self._is_recording = True

        logger.info("Starting async recording")
        self.tts.speak("Recording started")

        if self.on_recording_start:
            self.on_recording_start()

        return True

    def _on_silence_auto_stop(self):
        """Callback for when silence is detected and recording should auto-stop."""
        logger.info("Auto-stopping recording due to silence detection")
        # Use a thread to avoid blocking the audio callback
        import threading
        threading.Thread(target=self.stop_recording_async, daemon=True).start()

    def stop_recording_async(self) -> bool:
        """
        Stop recording and trigger processing asynchronously.
        Returns True if recording was stopped, False if not recording.
        """
        with self._state_lock:
            if not self._is_recording:
                logger.warning("Cannot stop recording: not currently recording")
                return False

        # Stop the actual audio recording and save to file
        audio_path = AUDIO_DIR / AUDIO_FILENAME
        if not self.audio_recorder.stop_recording(audio_path):
            logger.error("Failed to stop and save audio recording")
            with self._state_lock:
                self._is_recording = False
            return False

        with self._state_lock:
            self._is_recording = False
            self._is_processing = True

        logger.info("Stopping recording and starting processing")
        self.tts.speak("Recording complete. Processing audio.")

        if self.on_recording_stop:
            self.on_recording_stop()

        # Start processing in a background thread
        self._processing_thread = threading.Thread(
            target=self._process_recording_background,
            daemon=True
        )
        self._processing_thread.start()

        return True

    def _process_recording_background(self):
        """Process the recorded audio in the background."""
        try:
            if self.on_processing_start:
                self.on_processing_start()

            # Use the latest audio file
            audio_path = AUDIO_DIR / AUDIO_FILENAME

            if not audio_path.exists():
                raise FileNotFoundError(f"Audio file not found: {audio_path}")

            results = {
                "success": False,
                "audio_path": str(audio_path),
                "transcript": None,
                "title": "Untitled Insight",
                "capsule": None,
                "log_path": None,
                "error": None
            }

            # Step 1: Transcription
            self.tts.speak("Transcribing audio")
            transcript = self.transcriber.transcribe(audio_path)
            results["transcript"] = transcript

            processed_transcript = transcript
            if not transcript.strip():
                self.tts.speak("Transcript is empty")
                processed_transcript = "User provided silent or very short audio."
            else:
                self.tts.speak("Transcription complete")

            # Step 2: Generate title
            log_title = self._generate_simple_title(transcript)
            results["title"] = log_title

            # Step 3: Generate capsule
            self.tts.speak("Generating insight capsule")
            capsule = self.synthesizer.generate_capsule(processed_transcript)
            results["capsule"] = capsule
            self.tts.speak("Insight capsule generated")

            # Step 4: Save everything
            tags = self.storage.extract_tags_from_text(transcript)
            timestamp = datetime.now()

            log_path = self.storage.save_log(
                title=log_title,
                transcript=transcript,
                capsule=capsule,
                tags=tags,
                timestamp=timestamp
            )
            results["log_path"] = str(log_path)

            # Step 5: Speak result
            self.tts.speak("Here is your insight capsule")
            if capsule and "error" not in capsule.lower() and "skipped" not in capsule.lower():
                self.tts.speak(capsule)
            elif not capsule:
                self.tts.speak("The insight capsule is empty.")
            else:
                self.tts.speak("The insight capsule contains an error or was based on empty input.")

            results["success"] = True
            logger.info("Processing completed successfully")

            if self.on_processing_complete:
                self.on_processing_complete(results)

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Processing error: {error_msg}", exc_info=True)
            self.tts.speak("An error occurred during processing")

            if self.on_error:
                self.on_error(error_msg)

        finally:
            with self._state_lock:
                self._is_processing = False
            logger.info("Processing thread completed")