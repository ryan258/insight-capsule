# **🧠 Insight Capsule**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![UV](https://img.shields.io/badge/uv-package%20manager-green.svg)](https://astral.sh/uv)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)
[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](ROADMAP.md)

**A local-first, privacy-focused "thought partner" designed for accessibility.** Turn your rambling, spoken ideas into clear, synthesized insights—and then into first drafts for your content. All on your own computer.

## **🎯 Why This Exists**

If you have limited mobility, chronic pain, or just prefer voice-first workflows, Insight Capsule is being built to help you:

* **Capture ideas hands-free** \- A global hotkey or tray icon means you never leave your flow.  
* **Get organized summaries** \- Turn rambling thoughts into clear, high-insight capsules.  
* **Go from thought to draft** \- Use your insights to generate blog post outlines and first drafts, battling the "blank page."  
* **Keep everything private** \- No data ever leaves your computer. Your thoughts stay yours.  
* **Work offline** \- No internet required after setup. No API keys, no cloud services, no ongoing costs.

This project is built from the ground up to be an **accessibility-first** tool for creators.

## **✨ The Vision (How It's Designed to Work)**

This project is moving from a command-line tool to a zero-friction, ambient application.

1. **🎙️ Speak (Anytime)** \- While writing an email or browsing the web, you have a thought. You press a global hotkey (e.g., Ctrl+Shift+Space).  
2. **🗣️ Feedback** \- You hear a "Recording started" confirmation$$cite: \`core/tts.py\`$$  
   . You speak your idea naturally. You press the hotkey again.  
3. **🧠 Process (In Background)** \- In the background, your voice is transcribed$$cite: \`core/transcription.py\`$$  
   , and a local LLM synthesizes a concise "insight capsule"$$cite: \`agents/synthesizer.py\`$$  
   .  
4. **🔊 Hear** \- A few seconds later, the TTS reads your new insight back to you.  
5. **✍️ Act (Optional)** \- A menu in your system tray asks, "What's next?" You select "Draft Blog Outline," and a new draft is added to your log, ready for your evergreen content.  
6. **💾 Save** \- The transcript, insight, and new draft are all saved locally in an organized Markdown file$$cite: \`core/storage.py\`$$  
   .

## **🚀 Project Status & Roadmap**

**Current Version: 0.3.0 - Tray Application** ✅

This project now features a **persistent system tray application** with global hotkey support and content drafting capabilities.

### **✅ COMPLETED: System Tray Application (v0.3.0)**

* **System Tray App** - Persistent tray icon with dynamic color-coded states (blue/red/orange/green)
* **Global Hotkey** - Press Ctrl+Shift+Space from anywhere to toggle recording
* **Content Drafting** - Generate blog outlines, first drafts, and key takeaways from insights
* **Launch on Startup** - Cross-platform auto-start support (macOS, Windows, Linux)
* **Silence Detection** - Optional auto-stop after configurable silence duration
* **Non-blocking Recording** - Thread-safe background recording and processing
* **Actions Menu** - Post-capture actions: Draft Blog Outline, Generate First Draft, Extract Takeaways

### **✅ COMPLETED: Hardened Foundation (v0.2.0)**

* **Core Pipeline** - Audio recording → Whisper transcription → Local LLM synthesis → Storage
* **Local-First Architecture** - Full Ollama integration with OpenAI fallback
* **Professional Logging** - Centralized logging system with file and console output
* **Error Handling** - Robust exception handling with graceful failures and cleanup
* **Modern Project Management** - UV-based dependency management with `pyproject.toml`
* **Type Safety** - Type hints throughout core modules
* **Testing Infrastructure** - Automated tests with coverage reporting (8/8 passing)
* **Documentation** - Comprehensive inline docs and configuration examples

See [BASE_HARDENING_SUMMARY.md](BASE_HARDENING_SUMMARY.md) for complete technical details.

### **🚀 NEXT: The "Happy Path" Plan**

See our full [**ROADMAP.md**](ROADMAP.md) for detailed implementation plans:

* **✅ Phase 1: Tray App** - COMPLETED - System tray application with persistent menu controls
* **✅ Phase 2: Global Hotkey** - COMPLETED - Ctrl+Shift+Space for ambient capture
* **✅ Phase 3: Content Drafting** - COMPLETED - Turn ideas into blog post outlines and drafts
* **🔄 Phase 4: Personal Search** - IN PROGRESS - Natural language search across past insights
* **Phase 5: One-Click Install** - A distributable app for non-technical users

## **🛠️ Quick Start**

### **Prerequisites**

* **Python 3.10+** - [Download](https://www.python.org/downloads/)
* **Microphone** - Any working audio input device
* **[uv](https://astral.sh/uv)** - Modern Python package manager
* **[Ollama](https://ollama.ai)** - Local LLM runtime
* **ffmpeg** - Audio processing library
  * macOS: `brew install ffmpeg`
  * Windows: `choco install ffmpeg`
  * Linux: `sudo apt-get install ffmpeg`

### **Installation**

```bash
# 1. Clone the repository
git clone https://github.com/ryan258/insight-capsule.git
cd insight-capsule

# 2. Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Install dependencies (UV handles venv creation automatically)
uv pip install -r requirements.txt

# 4. Set up Ollama and pull a model
# Start Ollama app, then:
ollama pull llama3.2
# OR use deepseek-r1, mistral, etc.

# 5. Create .env file from example
cp .example.env .env
# Edit .env if needed (optional - defaults work out of the box)

# 6. Verify everything works
uv run python -c "from utils.helpers import validate_environment; print(validate_environment())"
# Should output: []  (empty list = all good!)
```

### **Running the Application**

#### **System Tray Application (Recommended)**

```bash
# Start the persistent tray application
uv run python tray_app.py

# The app will:
# - Add an icon to your system tray/menu bar
# - Listen for Ctrl+Shift+Space hotkey
# - Stay running in the background
# - Automatically process recordings when you stop
```

**Tray Icon Colors:**
- 🔵 **Blue** - Ready (idle)
- 🔴 **Red** - Recording
- 🟠 **Orange** - Processing
- 🟢 **Green** - Complete (briefly)

**Menu Options:**
- **Start Recording** - Begin capturing audio
- **Stop Recording** - Stop and process current recording
- **Actions** → Generate blog outline, first draft, or key takeaways
- **Open Logs Folder** - View your saved insights
- **Launch on Startup** - Toggle auto-start
- **Quit** - Exit the application

**Global Hotkey:** Press **Ctrl+Shift+Space** from any application to toggle recording on/off.

#### **Command Line Interface (Alternative)**

```bash
# Basic usage - voice to insight pipeline
uv run python main.py

# Advanced CLI with options
uv run python cli.py --help

# Example: Use a different Whisper model
uv run python cli.py --whisper-model small

# Example: Disable text-to-speech
uv run python cli.py --no-tts
```

### **Configuration**

All settings are in `.env` (copy from `.example.env` to get started):

```bash
# Local LLM (default and recommended)
USE_LOCAL_LLM=true
LOCAL_LLM_URL=http://localhost:11434
LOCAL_LLM_MODEL=llama3.2  # or deepseek-r1, mistral, etc.

# Whisper settings
WHISPER_MODEL=base  # tiny, base, small, medium, large

# Text-to-speech
TTS_ENABLED=true
TTS_RATE=170

# External LLM (optional fallback)
OPENAI_API_KEY=  # Only needed if USE_LOCAL_LLM=false
```

See `.example.env` for complete configuration options with detailed comments.

## **📁 What Gets Saved**

Everything is stored locally in the `data/` folder - **your** private database.

```
data/
├── input_voice/          # Your raw audio recordings (.wav)
└── logs/
    ├── index.md          # Searchable index of all your insights
    ├── system/           # Application logs (debugging)
    │   └── insight_capsule_20251101.log
    └── 2025-11-01-123000-my-new-idea.md  # Your insight logs
```

### **Example Insight Log Entry**

```markdown
# Insight Capsule Log — 2025-11-01 12:30:00
**Title:** My New Idea
**Tags:** #website #ms

**Transcript:** ```text
I was thinking about maybe building a small tool for...
```

**Insight Capsule:**
This idea centers on creating a focused development tool that addresses...
```

Future phases will add draft outlines and blog posts to these logs.

---

## **🧪 Testing & Development**

The project includes a testing infrastructure and development tools.

### **Running Tests**

```bash
# Run all automated tests
uv run python -m pytest tests/ -v

# Run with coverage report
uv run python -m pytest tests/ -v --cov=core --cov=agents --cov=pipeline

# Test specific module
uv run python -m pytest tests/test_core_functionality.py -v
```

**Current test status:** 8/8 passing ✅

### **Environment Validation**

```bash
# Check if everything is set up correctly
uv run python -c "from utils.helpers import validate_environment; issues = validate_environment(); print('✅ All good!' if not issues else '\n'.join(f'⚠️ {i}' for i in issues))"

# Check Ollama status
curl http://localhost:11434/api/tags
```

### **Development Tools**

```bash
# Code linting (once configured)
uv run ruff check .

# Type checking (once configured)
uv run mypy core/ agents/ pipeline/

# Format code
uv run ruff format .
```

### **Project Structure**

```
insight-capsule/
├── agents/              # LLM agents (synthesizer, future: drafter)
├── core/                # Core functionality
│   ├── audio.py         # Audio recording
│   ├── transcription.py # Whisper integration
│   ├── local_generation.py  # Ollama/LLM generation
│   ├── storage.py       # File management
│   ├── tts.py          # Text-to-speech
│   ├── logger.py       # Centralized logging
│   └── exceptions.py   # Custom exceptions
├── pipeline/            # Orchestration
│   └── orchestrator.py  # Main pipeline logic
├── config/              # Configuration
│   └── settings.py      # Environment settings
├── utils/               # Utilities
│   └── helpers.py       # Validation, helpers
├── tests/               # Test suite
├── main.py             # Simple entry point
├── cli.py              # Advanced CLI
├── pyproject.toml      # Project configuration
└── requirements.txt    # Dependencies
```

---

## **🔧 Troubleshooting**

### **Environment Validation Failures**

```bash
# Check what's wrong
uv run python -c "from utils.helpers import validate_environment; print(validate_environment())"
```

Common issues:

**"ffmpeg not installed"**
- macOS: `brew install ffmpeg`
- Windows: `choco install ffmpeg` or download from [ffmpeg.org](https://ffmpeg.org)
- Linux: `sudo apt-get install ffmpeg`

**"Ollama not running"**
1. Download and install [Ollama](https://ollama.ai)
2. Start the Ollama application
3. Pull a model: `ollama pull llama3.2` (or deepseek-r1, mistral, etc.)
4. Verify: `curl http://localhost:11434/api/tags`

**"OPENAI_API_KEY not set"**
- Only needed if you set `USE_LOCAL_LLM=false` in your `.env`
- Get your key from [OpenAI Platform](https://platform.openai.com/api-keys)
- Add to `.env`: `OPENAI_API_KEY=sk-...`

### **Audio Issues**

**Recording not working**
- Check microphone permissions (System Preferences → Privacy → Microphone on macOS)
- List available devices: `uv run python -c "from utils.helpers import list_audio_devices; list_audio_devices()"`
- Test with another app to verify microphone works

**Empty or failed recordings**
- Check system logs: `tail -f data/logs/system/insight_capsule_*.log`
- Ensure microphone is set as default input device
- Try a different microphone if available

### **Transcription Issues**

**Whisper model fails to load**
- First load downloads the model (can take several minutes)
- Check internet connection for initial download
- Models stored in `~/.cache/whisper/`
- Try a smaller model: `--whisper-model tiny`

**Transcription is inaccurate**
- Try a larger model: `--whisper-model small` or `medium`
- Speak clearly and reduce background noise
- Ensure good microphone quality

### **LLM Generation Issues**

**"Local LLM failed after X attempts"**
1. Verify Ollama is running: `curl http://localhost:11434/api/tags`
2. Check Ollama logs for errors
3. Try a different model in `.env`: `LOCAL_LLM_MODEL=mistral`
4. Restart Ollama application

**Slow generation**
- Larger models are slower (deepseek-r1 > llama3.2)
- Check CPU/RAM usage during generation
- Consider using a smaller, faster model

**Fallback to OpenAI**
- If local fails, it automatically tries OpenAI (if configured)
- Set `OPENAI_API_KEY` in `.env` for fallback support

### **Text-to-Speech (TTS) Issues**

**TTS not working or crashing**
1. Check speakers/audio output is working
2. Try manual test: `uv run python tests/test_tts_minimal.py`
3. Disable if problematic: `TTS_ENABLED=false` in `.env`
4. Or use CLI flag: `uv run python cli.py --no-tts`

**TTS too fast/slow**
- Adjust in `.env`: `TTS_RATE=150` (range: 100-250)

### **Getting Help**

1. **Check logs**: `tail -f data/logs/system/insight_capsule_*.log`
2. **Run validation**: `uv run python -c "from utils.helpers import validate_environment; print(validate_environment())"`
3. **Run tests**: `uv run python -m pytest tests/ -v`
4. **Open an issue**: [GitHub Issues](https://github.com/ryan258/insight-capsule/issues)

---

## **💙 Accessibility Statement**

**This tool was built specifically for creators with physical limitations.**

If traditional input methods are challenging for you, this project aims to provide:

* ✅ **Voice-first interaction** - Minimal typing required
* ✅ **Intelligent error handling** - Graceful failures that don't break your flow
* ✅ **Clear audio feedback** - TTS guidance throughout the process
* ✅ **Local-first design** - Works offline, respects your privacy
* ✅ **Reliable operation** - Robust logging and error recovery

**If you're building something creative while working with constraints, this is for you.**

---

## **🤝 Contributing**

Contributions are welcome! This project is in active development.

### **Ways to Contribute**

1. **Report bugs** - Open an issue with reproduction steps
2. **Suggest features** - Share your use case and ideas
3. **Improve documentation** - Help others get started
4. **Write tests** - Increase code coverage (currently 27%)
5. **Add features** - See [ROADMAP.md](ROADMAP.md) for planned work

### **Development Setup**

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/insight-capsule.git
cd insight-capsule

# Install with dev dependencies
uv pip install -r requirements.txt
uv pip install pytest pytest-cov mypy ruff

# Make your changes, add tests

# Run tests
uv run python -m pytest tests/ -v

# Submit a pull request
```

---

## **📄 License**

MIT License - See [LICENSE](LICENSE) for details

## **🙏 Acknowledgments**

Built with:
- [OpenAI Whisper](https://github.com/openai/whisper) - Audio transcription
- [Ollama](https://ollama.ai) - Local LLM runtime
- [UV](https://astral.sh/uv) - Fast Python package manager
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3) - Text-to-speech

---

## **📞 Contact & Support**

- **Author**: Ryan Johnson
- **Website**: [ryanleej.com](https://ryanleej.com)
- **Issues**: [GitHub Issues](https://github.com/ryan258/insight-capsule/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ryan258/insight-capsule/discussions)

**Version**: 0.2.0 (Hardened Base)
**Status**: ✅ Production-ready foundation, ready for Phase 1 development

---

**Made with ❤️ for creators who think out loud**