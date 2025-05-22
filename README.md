# 🧠 Insight Capsule

**A local-first AI-powered voice-to-insight tool.**  
Speak an idea → transcribe → generate creative brief → synthesize capsule → speak it back to you.

---

## ⚙️ Features

- 🎙️ Voice-recorded idea capture with real-time feedback
- ✨ Whisper for accurate speech-to-text (configurable models)
- 📘 Auto-generated creative briefs with structured output
- 🧠 GPT-based "insight capsule" summarization
- 🔊 Text-to-speech playback with intelligent fallbacks
- 📂 All logs saved to `/data/logs/` and automatically indexed
- 🤖 Modular agent architecture for extensibility
- 🛠️ CLI interface with advanced options
- 🔧 Environment validation and error handling

---

## 📦 Requirements

- Python 3.10+
- Windows 11 (primary target, but cross-platform compatible)
- Microphone (internal or USB)
- OpenAI API key

---

## 🛠️ Installation

```bash
# Clone and navigate to the project
git clone https://github.com/your-name/insight-capsule.git
cd insight-capsule

# Setup virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Install ffmpeg (needed for whisper)
choco install ffmpeg -y  # Windows
# sudo apt-get install ffmpeg  # Ubuntu/Debian
# brew install ffmpeg  # macOS

# Setup environment
copy .env.example .env  # Create from template
# Edit .env and add your OPENAI_API_KEY
```

---

## 🚀 Usage

### Simple Usage (Default Pipeline)
```bash
python main.py
```

### Advanced CLI Usage
```bash
# Full pipeline with options
python cli.py

# Use pre-recorded audio file
python cli.py --audio path/to/audio.wav

# Disable text-to-speech
python cli.py --no-tts

# Use different Whisper model
python cli.py --whisper-model small

# Legacy interface (original implementation)
python record_and_run.py
```

### Pipeline Flow

1. **Press Enter** to start recording
2. **Speak your idea** clearly
3. **Press Enter** again to stop recording
4. **Wait for processing**: The AI will automatically:
   - Transcribe your audio using Whisper
   - Generate a structured creative brief
   - Synthesize an insight capsule
   - Speak the result back to you
   - Save everything to organized logs

---

## 📁 Project Structure

```
insight-capsule/
├── core/                    # Core functionality modules
│   ├── audio.py            # Audio recording with sounddevice
│   ├── transcription.py    # Whisper integration
│   ├── generation.py       # OpenAI GPT interface
│   ├── tts.py             # Text-to-speech with fallbacks
│   ├── storage.py         # File management and indexing
│   └── exceptions.py      # Custom error handling
├── agents/                  # AI agent modules
│   ├── clarifier.py       # Creative brief generation
│   └── synthesizer.py     # Insight capsule synthesis
├── pipeline/               # Pipeline orchestration
│   └── orchestrator.py    # Main pipeline logic
├── config/                 # Configuration management
│   └── settings.py        # Environment and model settings
├── utils/                  # Utility modules
│   ├── helpers.py         # Environment validation
│   ├── gpt_interface.py   # Legacy GPT interface
│   └── whisper_wrapper.py # Legacy Whisper wrapper
├── data/                   # Data storage
│   ├── input_voice/       # Recorded audio files
│   ├── briefs/           # Generated creative briefs
│   └── logs/             # Session logs and index
├── main.py                # Simple entry point
├── cli.py                 # Advanced CLI interface
├── record_and_run.py      # Legacy implementation
└── .env                   # Environment configuration
```

---

## ⚙️ Configuration

The application uses environment variables for configuration. Copy `.env.example` to `.env` and customize:

```env
# Required
OPENAI_API_KEY=your_api_key_here

# Optional
TTS_ENABLED=true
WHISPER_MODEL=base
TTS_RATE=170
```

### Available Whisper Models
- `tiny` - Fastest, least accurate
- `base` - Good balance (default)
- `small` - Better accuracy
- `medium` - High accuracy
- `large` - Best accuracy, slowest

---

## 🧠 Agent Architecture

The system uses a modular agent approach:

- **ClarifierAgent**: Structures raw speech into organized creative briefs
- **SynthesizerAgent**: Transforms ideas into concise insight capsules
- **StorageManager**: Handles file organization and indexing
- **AudioRecorder**: Manages voice recording with real-time feedback
- **GPTGenerator**: Handles all AI text generation with role-based models

---

## 🔧 Troubleshooting

### Audio Issues
```bash
# Test your audio setup
python -c "from utils.helpers import list_audio_devices; list_audio_devices()"

# Validate environment
python cli.py  # Will show warnings for missing dependencies
```

### TTS Issues
- The system includes intelligent fallbacks for text-to-speech
- If TTS fails, it will gracefully fall back to text output
- Test TTS separately with `python test_tts_minimal.py`

### API Issues
- Ensure your OpenAI API key is valid and has sufficient credits
- Check your `.env` file configuration
- The system will provide clear error messages for API failures

---

## 🧭 Roadmap

See [`ROADMAP.md`](./ROADMAP.md) for detailed development plans, including:

- Enhanced agent capabilities
- GUI interface options
- Export to external platforms
- Improved accessibility features

---

## 🤝 Acknowledgements

Built with:

- [OpenAI Whisper](https://github.com/openai/whisper) - Speech recognition
- [OpenAI GPT-4 API](https://platform.openai.com) - Text generation
- [Pyttsx3](https://pyttsx3.readthedocs.io/en/latest/) - Text-to-speech
- [SoundDevice](https://python-sounddevice.readthedocs.io/) - Audio recording
- [SoundFile](https://pysoundfile.readthedocs.io/) - Audio file handling

---

## 🧍 Accessibility & Purpose

This tool was designed with **adaptive accessibility** in mind — to assist creators working under physical limitations. Its goal is to make thinking out loud a seamless path to thoughtful, saved, and structured output.

**Key Accessibility Features:**
- Voice-first interaction requiring minimal typing
- Intelligent error handling that doesn't interrupt workflow
- Multiple interface options (simple, advanced CLI, legacy)
- Graceful fallbacks when components fail
- Clear audio feedback throughout the process

If you're working with constraints, this project is for you.

---

## 💬 License

MIT — use, remix, adapt, evolve.

---

**You shouldn't have to fight for every inch just to build something creative.**