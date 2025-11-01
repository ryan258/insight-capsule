import queue
import sounddevice as sd
import soundfile as sf
from pathlib import Path
from typing import Optional, Callable
from config.settings import AUDIO_SAMPLE_RATE, AUDIO_CHANNELS
from core.exceptions import AudioRecordingError
from core.logger import setup_logger

logger = setup_logger(__name__)


class AudioRecorder:
    def __init__(self, sample_rate: int = AUDIO_SAMPLE_RATE, channels: int = AUDIO_CHANNELS):
        self.sample_rate = sample_rate
        self.channels = channels
        self.queue = queue.Queue()
        
    def _audio_callback(self, indata, frames, time, status):
        """Callback for audio stream."""
        if status:
            logger.warning(f"Audio stream status: {status}")
        self.queue.put(indata.copy())
    
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