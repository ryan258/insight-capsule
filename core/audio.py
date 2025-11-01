import queue
import sounddevice as sd
import soundfile as sf
from pathlib import Path
from typing import Optional, Callable
import threading
import time
import numpy as np
from config.settings import (
    AUDIO_SAMPLE_RATE,
    AUDIO_CHANNELS,
    SILENCE_DETECTION_ENABLED,
    SILENCE_THRESHOLD,
    SILENCE_DURATION
)
from core.exceptions import AudioRecordingError
from core.logger import setup_logger

logger = setup_logger(__name__)


class AudioRecorder:
    def __init__(
        self,
        sample_rate: int = AUDIO_SAMPLE_RATE,
        channels: int = AUDIO_CHANNELS,
        silence_detection: bool = SILENCE_DETECTION_ENABLED,
        silence_threshold: float = SILENCE_THRESHOLD,
        silence_duration: float = SILENCE_DURATION
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.queue = queue.Queue()

        # Silence detection settings
        self.silence_detection = silence_detection
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self._silence_start_time = None
        self._on_silence_detected: Optional[Callable[[], None]] = None

        # State for non-blocking recording
        self._is_recording = False
        self._stream = None
        self._recording_lock = threading.Lock()
        self._silence_monitor_thread = None
        
    def _audio_callback(self, indata, frames, time, status):
        """Callback for audio stream."""
        if status:
            logger.warning(f"Audio stream status: {status}")
        self.queue.put(indata.copy())

        # Check for silence if enabled
        if self.silence_detection and self._is_recording:
            # Calculate RMS (root mean square) amplitude
            rms = np.sqrt(np.mean(indata**2))

            if rms < self.silence_threshold:
                # Silence detected
                if self._silence_start_time is None:
                    self._silence_start_time = time.time()
                elif time.time() - self._silence_start_time >= self.silence_duration:
                    # Silence has persisted for the required duration
                    logger.info(f"Silence detected for {self.silence_duration}s, triggering callback")
                    if self._on_silence_detected:
                        self._on_silence_detected()
                    self._silence_start_time = None  # Reset
            else:
                # Sound detected, reset silence timer
                self._silence_start_time = None
    
    def record_to_file(
        self,
        output_path: Path,
        on_start: Optional[Callable[[], None]] = None,
        on_stop: Optional[Callable[[], None]] = None,
    ) -> bool:
        """
        Record audio until Enter is pressed.

        Args:
            output_path: Path to save the audio file
            on_start: Optional callback when recording starts
            on_stop: Optional callback when recording stops

        Returns:
            bool: True if successful, False otherwise

        Raises:
            AudioRecordingError: If recording fails critically
        """
        try:
            logger.info("Waiting for user to start recording...")
            input("📣 Press [Enter] to start recording...")
            print("🎙️ Recording... Press [Enter] again to stop.")
            logger.info("Recording started")

            if on_start:
                on_start()

            # Ensure parent directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with sf.SoundFile(
                output_path, mode="w", samplerate=self.sample_rate, channels=self.channels
            ) as file:
                with sd.InputStream(
                    samplerate=self.sample_rate,
                    channels=self.channels,
                    callback=self._audio_callback,
                ):
                    input()  # Wait for Enter to stop
                    print("🛑 Stopping recording...")
                    logger.info("Recording stopped")

                    if on_stop:
                        on_stop()

                    # Drain queue
                    frames_written = 0
                    while not self.queue.empty():
                        file.write(self.queue.get())
                        frames_written += 1

                    logger.debug(f"Wrote {frames_written} audio frames")

            print(f"🎤 Audio saved to {output_path}")
            logger.info(f"Audio file saved: {output_path}")
            return True

        except KeyboardInterrupt:
            logger.info("Recording cancelled by user")
            if output_path.exists():
                output_path.unlink()
            return False

        except Exception as e:
            error_msg = f"Failed to record audio: {e}"
            logger.error(error_msg, exc_info=True)
            print(f"🔴 [Audio Error] {error_msg}")
            if output_path.exists():
                output_path.unlink()  # Remove corrupt file
                logger.debug(f"Removed corrupt audio file: {output_path}")
            return False
    
    def clear_queue(self):
        """Clear any remaining audio in the queue."""
        while not self.queue.empty():
            self.queue.get()

    # === New methods for non-blocking recording ===

    def start_recording(self) -> bool:
        """
        Start recording audio (non-blocking).
        Returns True if started successfully, False otherwise.
        """
        with self._recording_lock:
            if self._is_recording:
                logger.warning("Already recording")
                return False

            try:
                logger.info("Starting non-blocking recording")
                self.clear_queue()

                self._stream = sd.InputStream(
                    samplerate=self.sample_rate,
                    channels=self.channels,
                    callback=self._audio_callback
                )
                self._stream.start()
                self._is_recording = True
                logger.info("Recording started successfully")
                return True

            except Exception as e:
                logger.error(f"Failed to start recording: {e}", exc_info=True)
                self._is_recording = False
                return False

    def stop_recording(self, output_path: Path) -> bool:
        """
        Stop recording and save to file.
        Returns True if stopped and saved successfully, False otherwise.
        """
        with self._recording_lock:
            if not self._is_recording:
                logger.warning("Not currently recording")
                return False

            try:
                logger.info("Stopping non-blocking recording")

                # Stop the stream
                if self._stream:
                    self._stream.stop()
                    self._stream.close()
                    self._stream = None

                self._is_recording = False

                # Give a moment for the queue to catch up
                time.sleep(0.1)

                # Ensure parent directory exists
                output_path.parent.mkdir(parents=True, exist_ok=True)

                # Save recorded audio
                frames_written = 0
                with sf.SoundFile(
                    output_path, mode="w",
                    samplerate=self.sample_rate,
                    channels=self.channels
                ) as file:
                    while not self.queue.empty():
                        file.write(self.queue.get())
                        frames_written += 1

                logger.info(f"Wrote {frames_written} audio frames to {output_path}")

                if frames_written == 0:
                    logger.warning("No audio data was recorded")
                    if output_path.exists():
                        output_path.unlink()
                    return False

                return True

            except Exception as e:
                logger.error(f"Failed to stop and save recording: {e}", exc_info=True)
                self._is_recording = False
                if output_path.exists():
                    output_path.unlink()
                return False

    @property
    def is_recording(self) -> bool:
        """Check if currently recording."""
        with self._recording_lock:
            return self._is_recording