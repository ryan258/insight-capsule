import pyttsx3
import sys
import platform
from typing import Optional
from config.settings import TTS_ENABLED, TTS_RATE, TTS_FALLBACK_BEEP

class TextToSpeech:
    def __init__(self, enabled: bool = TTS_ENABLED, rate: int = TTS_RATE):
        self.enabled = enabled
        self.rate = rate
        self._engine = None
        self._initialized = False
        
        if self.enabled:
            self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize the TTS engine."""
        try:
            self._engine = pyttsx3.init()
            if self._engine:
                self._engine.setProperty("rate", self.rate)
                self._initialized = True
                print("[TTS] Engine initialized successfully")
        except Exception as e:
            print(f"[TTS Error] Could not initialize: {e}")
            self._initialized = False
            self.enabled = False
    
    def speak(self, text: str, fallback_to_print: bool = True):
        """Speak the given text."""
        if not self.enabled or not self._initialized:
            if fallback_to_print:
                print(f"[TTS Disabled] {text}")
            return
        
        try:
            self._engine.say(text)
            self._engine.runAndWait()
        except Exception as e:
            print(f"[TTS Error] Failed to speak: {e}")
            if fallback_to_print:
                print(f"[TTS Fallback] {text}")
            self.enabled = False
    
    def beep(self, frequency: int = 440, duration_ms: int = 200):
        """Play a beep sound as feedback."""
        if not TTS_FALLBACK_BEEP:
            return
        
        system = platform.system()
        
        try:
            if system == "Windows":
                import winsound
                winsound.Beep(frequency, duration_ms)
            else:
                # Simple terminal bell for other systems
                print('\a', end='', flush=True)
        except Exception:
            pass  # Silent failure for beeps