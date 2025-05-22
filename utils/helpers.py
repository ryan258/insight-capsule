import sys
import subprocess
from pathlib import Path
from typing import List

def ensure_ffmpeg():
    """Check if ffmpeg is available."""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  ffmpeg not found. Please install it:")
        if sys.platform == "win32":
            print("   choco install ffmpeg -y")
        else:
            print("   sudo apt-get install ffmpeg  # Ubuntu/Debian")
            print("   brew install ffmpeg  # macOS")
        return False

def list_audio_devices():
    """List available audio input devices."""
    import sounddevice as sd
    print("Available audio devices:")
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            print(f"  [{i}] {device['name']} ({device['max_input_channels']} channels)")

def validate_environment() -> List[str]:
    """Validate the environment setup."""
    issues = []
    
    # Check API key
    from config.settings import OPENAI_API_KEY
    if not OPENAI_API_KEY:
        issues.append("OPENAI_API_KEY not set in .env file")
    
    # Check ffmpeg
    if not ensure_ffmpeg():
        issues.append("ffmpeg not installed")
    
    # Check directories
    from config.settings import DATA_DIR
    if not DATA_DIR.exists():
        issues.append(f"Data directory not found: {DATA_DIR}")
    
    return issues