import queue
import sounddevice as sd
import soundfile as sf
from pathlib import Path
from typing import Optional, Callable, Union
import threading
import time
import numpy as np
from config.settings import (
    AUDIO_SAMPLE_RATE,
    AUDIO_CHANNELS,
    AUDIO_INPUT_DEVICE,
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
        input_device: Optional[str] = AUDIO_INPUT_DEVICE,
        silence_threshold: float = SILENCE_THRESHOLD,
        silence_duration: float = SILENCE_DURATION
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.queue = queue.Queue()
        self._input_device_config = input_device.strip() if input_device else None

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

    def _open_stream(self, device: Optional[Union[int, str]] = None) -> sd.InputStream:
        """Create an InputStream with optional device override."""
        stream_kwargs = {
            "samplerate": self.sample_rate,
            "channels": self.channels,
            "callback": self._audio_callback
        }
        if device is not None:
            stream_kwargs["device"] = device
        return sd.InputStream(**stream_kwargs)

    def _get_configured_device(self) -> Optional[Union[int, str]]:
        """Resolve configured input device name/index if provided."""
        if not self._input_device_config:
            return None

        config_value = self._input_device_config

        # Allow direct index specification
        try:
            return int(config_value)
        except ValueError:
            pass

        # Match by substring against available device names
        try:
            devices = sd.query_devices()
        except Exception as exc:
            logger.warning(
                "Could not query audio devices to match configured input '%s': %s",
                config_value,
                exc,
            )
            return config_value

        for idx, dev in enumerate(devices):
            name = dev.get("name", "")
            if config_value.lower() in name.lower():
                logger.info("Matched configured audio input '%s' to device %s (%s)",
                            config_value, idx, name)
                return idx

        logger.warning(
            "Configured audio input '%s' not found; falling back to default device",
            config_value,
        )
        return None

    def _find_fallback_device(self, exclude: Optional[Union[int, str]] = None) -> Optional[int]:
        """Find the first available input device, excluding the provided one."""
        try:
            devices = sd.query_devices()
        except Exception as exc:
            logger.warning("Could not query audio devices for fallback: %s", exc)
            return None

        for idx, dev in enumerate(devices):
            if dev.get("max_input_channels", 0) > 0 and idx != exclude:
                return idx
        return None

    def _log_input_devices(self) -> None:
        """Log available input devices for troubleshooting."""
        try:
            devices = sd.query_devices()
        except Exception as exc:
            logger.error("Unable to list audio devices: %s", exc)
            return

        input_devices = [
            f"{idx}: {dev.get('name', 'Unknown')} "
            f"(inputs={dev.get('max_input_channels', 0)}, "
            f"default_sr={dev.get('default_samplerate', 'n/a')})"
            for idx, dev in enumerate(devices)
            if dev.get("max_input_channels", 0) > 0
        ]

        if not input_devices:
            logger.error("PortAudio did not report any usable input devices")
            return

        logger.info("Detected audio input devices:")
        for entry in input_devices:
            logger.info("  %s", entry)

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

                device = self._get_configured_device()
                try:
                    self._stream = self._open_stream(device=device)
                    self._stream.start()
                    self._is_recording = True
                    logger.info(
                        "Recording started successfully%s",
                        f" using device {device}" if device is not None else ""
                    )
                    return True

                except sd.PortAudioError as err:
                    logger.error(
                        "Failed to open audio stream%s: %s",
                        f" with device {device}" if device is not None else "",
                        err,
                        exc_info=True,
                    )
                    fallback_device = self._find_fallback_device(exclude=device)
                    if fallback_device is not None:
                        try:
                            logger.info("Retrying audio stream with fallback device %s", fallback_device)
                            self._stream = self._open_stream(device=fallback_device)
                            self._stream.start()
                            self._is_recording = True
                            logger.info("Recording started successfully using fallback device %s", fallback_device)
                            return True
                        except sd.PortAudioError as fallback_err:
                            logger.error(
                                "Fallback audio device %s also failed: %s",
                                fallback_device,
                                fallback_err,
                                exc_info=True,
                            )
                    self._log_input_devices()
                    raise

            except Exception as e:
                logger.error("Failed to start recording: %s", e, exc_info=True)
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
