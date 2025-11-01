import sys
import subprocess
from pathlib import Path
from typing import List
import requests


def ensure_ffmpeg() -> bool:
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


def check_ollama_available() -> bool:
    """Check if Ollama is running and available."""
    try:
        from config.settings import LOCAL_LLM_URL
        response = requests.get(f"{LOCAL_LLM_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def list_audio_devices() -> None:
    """List available audio input devices."""
    import sounddevice as sd
    print("Available audio devices:")
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            print(f"  [{i}] {device['name']} ({device['max_input_channels']} channels)")


def validate_environment() -> List[str]:
    """
    Validate the environment setup.

    Returns:
        List of issues found (empty if everything is OK)
    """
    issues = []

    # Check ffmpeg (required for Whisper)
    if not ensure_ffmpeg():
        issues.append("ffmpeg not installed (required for audio processing)")

    # Check Ollama (strongly recommended for local-first operation)
    if not check_ollama_available():
        from config.settings import USE_LOCAL_LLM
        if USE_LOCAL_LLM:
            issues.append(
                "Ollama not running (required for local LLM). "
                "Start Ollama and run: ollama pull llama3.2"
            )

    # Check OpenAI API key (only warn if set to use external LLM)
    from config.settings import OPENAI_API_KEY, USE_LOCAL_LLM
    if not USE_LOCAL_LLM and not OPENAI_API_KEY:
        issues.append(
            "OPENAI_API_KEY not set in .env file (required when USE_LOCAL_LLM=false)"
        )

    # Check directories
    from config.settings import DATA_DIR
    if not DATA_DIR.exists():
        issues.append(f"Data directory not found: {DATA_DIR}")

    return issues