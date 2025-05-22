import queue
import sounddevice as sd
import soundfile as sf
from pathlib import Path
from typing import Optional
from config.settings import AUDIO_SAMPLE_RATE, AUDIO_CHANNELS

class AudioRecorder:
    def __init__(self, sample_rate: int = AUDIO_SAMPLE_RATE, channels: int = AUDIO_CHANNELS):
        self.sample_rate = sample_rate
        self.channels = channels
        self.queue = queue.Queue()
        
    def _audio_callback(self, indata, frames, time, status):
        """Callback for audio stream."""
        if status:
            print(f"[Audio Status] {status}")
        self.queue.put(indata.copy())
    
    def record_to_file(self, output_path: Path, on_start=None, on_stop=None) -> bool:
        """
        Record audio until Enter is pressed.
        
        Args:
            output_path: Path to save the audio file
            on_start: Optional callback when recording starts
            on_stop: Optional callback when recording stops
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            input("📣 Press [Enter] to start recording...")
            print("🎙️ Recording... Press [Enter] again to stop.")
            
            if on_start:
                on_start()
            
            # Ensure parent directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with sf.SoundFile(
                output_path, 
                mode='w', 
                samplerate=self.sample_rate, 
                channels=self.channels
            ) as file:
                with sd.InputStream(
                    samplerate=self.sample_rate,
                    channels=self.channels,
                    callback=self._audio_callback
                ):
                    input()  # Wait for Enter to stop
                    print("🛑 Stopping recording...")
                    
                    if on_stop:
                        on_stop()
                    
                    # Drain queue
                    while not self.queue.empty():
                        file.write(self.queue.get())
            
            print(f"🎤 Audio saved to {output_path}")
            return True
            
        except Exception as e:
            print(f"🔴 [Audio Error] Failed to record: {e}")
            if output_path.exists():
                output_path.unlink()  # Remove corrupt file
            return False
    
    def clear_queue(self):
        """Clear any remaining audio in the queue."""
        while not self.queue.empty():
            self.queue.get()