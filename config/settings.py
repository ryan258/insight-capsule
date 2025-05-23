import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
AUDIO_DIR = DATA_DIR / "input_voice"
BRIEFS_DIR = DATA_DIR / "briefs"
LOGS_DIR = DATA_DIR / "logs"

# Ensure directories exist
for dir_path in [AUDIO_DIR, BRIEFS_DIR, LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Audio settings
AUDIO_SAMPLE_RATE = 44100
AUDIO_CHANNELS = 1
AUDIO_FILENAME = "latest.wav"

# API settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model settings
WHISPER_MODEL = "base"  # tiny, base, small, medium, large

# External LLM settings (OpenAI)
GPT_MODELS = {
    "writing": "gpt-4o-mini",
    "fact_check": "gpt-4o-mini", 
    "expander": "gpt-4o-mini"
}

# NEW: Local LLM settings
USE_LOCAL_LLM = os.getenv("USE_LOCAL_LLM", "true").lower() == "true"
LOCAL_LLM_URL = os.getenv("LOCAL_LLM_URL", "http://localhost:11434")
LOCAL_LLM_MODEL = os.getenv("LOCAL_LLM_MODEL", "llama3.2")

# TTS settings
TTS_ENABLED = os.getenv("TTS_ENABLED", "true").lower() == "true"
TTS_RATE = 170
TTS_FALLBACK_BEEP = True

# Pipeline settings
DEFAULT_TEMPERATURE = 0.7
MAX_CAPSULE_WORDS = 400