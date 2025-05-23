# 🧠 Insight Capsule

**A local-first, privacy-focused voice-to-insight tool.**  
Speak your thoughts → get them transcribed, organized, and synthesized → all on your computer.

---

## 🎯 Why This Exists

If you have limited mobility, chronic pain, or just prefer voice-first workflows, Insight Capsule lets you:

- **Capture ideas hands-free** - just speak naturally
- **Get organized summaries** - turn rambling thoughts into clear insights  
- **Keep everything private** - no data leaves your computer
- **Work offline** - no internet required after setup
- **Save and search** - automatic organization and indexing

Built specifically for **accessibility** and **privacy**. Your thoughts stay yours.

---

## ✨ How It Works

1. **🎙️ Speak** - Press Enter, talk naturally, Press Enter again
2. **📝 Transcribe** - Whisper converts speech to text (locally)
3. **🧠 Synthesize** - Local AI creates a clear, insightful summary
4. **🔊 Hear** - Text-to-speech reads your insight back to you
5. **💾 Save** - Everything automatically organized and searchable

**No API keys. No cloud services. No ongoing costs.**

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** 
- **Microphone** (built-in or USB)
- **5GB free space** (for local AI model)

### Installation

```bash
# 1. Clone and setup
git clone https://github.com/your-name/insight-capsule.git
cd insight-capsule
python -m venv .venv

# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Ollama (local AI)
# Go to https://ollama.ai and install for your OS
# Then pull a model:
ollama pull llama3.2

# 4. Optional: Install ffmpeg for better audio
# Windows: choco install ffmpeg
# macOS: brew install ffmpeg  
# Ubuntu: sudo apt-get install ffmpeg
```

### First Run

```bash
# Simple mode - just run it
python main.py

# Or with options
python cli.py --help
```

That's it! No API keys, no configuration files, no accounts.

---

## 🎛️ Usage Options

### Simple Mode
```bash
python main.py
```
Uses all defaults: local AI, built-in microphone, automatic saving.

### Advanced Mode
```bash
# Use a pre-recorded audio file
python cli.py --audio path/to/recording.wav

# Disable text-to-speech
python cli.py --no-tts

# Use different Whisper model (faster but less accurate)
python cli.py --whisper-model tiny

# Fall back to OpenAI (requires OPENAI_API_KEY in .env)
python cli.py --external-llm
```

### Environment Configuration
Create `.env` file for optional settings:
```env
# Optional - only needed if using --external-llm
OPENAI_API_KEY=your_key_here

# Optional tweaks
TTS_ENABLED=true
WHISPER_MODEL=base
TTS_RATE=170
USE_LOCAL_LLM=true
LOCAL_LLM_MODEL=llama3.2
```

---

## 📁 What Gets Saved

Everything goes in the `data/` folder:

```
data/
├── input_voice/     # Your audio recordings
├── logs/           # Full session logs with timestamps
│   └── index.md    # Searchable index of all insights
└── briefs/         # Structured data (JSON format)
```

**Example log entry:**
```markdown
# Insight Capsule Log — 2024-01-15 14:30:22
**Title:** Weekend Project Ideas
**Tags:** #coding #weekend

**Transcript:** I was thinking about maybe building a small tool for...

**Insight Capsule:** This idea centers on creating a focused development...
```

---

## 🔧 Troubleshooting

### "No local LLM available"
```bash
# Install Ollama from ollama.ai, then:
ollama pull llama3.2
ollama serve  # Should start automatically but try this if issues
```

### Audio issues
```bash
# Test your microphone
python -c "import sounddevice as sd; print(sd.query_devices())"

# Try different Whisper model
python cli.py --whisper-model small
```

### TTS not working
```bash
# Test TTS separately
python -c "import pyttsx3; e=pyttsx3.init(); e.say('test'); e.runAndWait()"

# Disable if problematic
python cli.py --no-tts
```

### Performance issues
```bash
# Use faster models
python cli.py --whisper-model tiny

# Or in .env:
LOCAL_LLM_MODEL=mistral  # Smaller than llama3.2
```

---

## 🏗️ Architecture

**Local-first design:** Everything runs on your computer.

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   🎙️ Audio      │───▶│   📝 Whisper     │───▶│  🧠 Local LLM   │
│   Recording     │    │   Transcription  │    │  (Ollama)       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
┌─────────────────┐    ┌──────────────────┐             │
│  🔊 Text-to-    │◀───│   💾 Storage     │◀────────────┘
│  Speech         │    │   & Indexing     │
└─────────────────┘    └──────────────────┘
```

**Core modules:**
- `core/` - Audio, transcription, local AI, storage
- `agents/` - Specialized AI behaviors (clarify, synthesize)  
- `pipeline/` - Orchestrates the full workflow
- `config/` - Settings and environment handling

---

## 🆚 Why Local Instead of Cloud?

| Cloud Services | Insight Capsule |
|----------------|-----------------|
| 💰 Monthly fees | ✅ Free after setup |
| 🌐 Internet required | ✅ Works offline |
| 🔍 Data collection | ✅ Private by design |
| ⏰ API rate limits | ✅ No limits |
| 🔒 Terms of service | ✅ You own everything |
| 📡 Latency | ✅ Instant processing |

---

## 🧩 Extend & Customize

**Simple customization:**
- Edit prompts in `agents/clarifier.py` and `agents/synthesizer.py`
- Adjust model settings in `config/settings.py`
- Modify TTS voice/speed in the TTS settings

**Advanced:**
- Add new agents for different processing styles
- Connect to different local LLM backends
- Export to your preferred note-taking system
- Build custom workflows in `pipeline/orchestrator.py`

---

## 🤝 Contributing

This project prioritizes **accessibility** and **privacy**. Contributions welcome that:

- Improve accessibility for users with limited mobility
- Enhance local processing capabilities  
- Reduce complexity while maintaining functionality
- Add better error handling and user feedback

---

## 💙 Accessibility Statement

**This tool was built specifically for creators with physical limitations.**

If traditional input methods are challenging for you, this project aims to provide:
- ✅ Voice-first interaction requiring minimal typing
- ✅ Intelligent error handling that doesn't break your flow
- ✅ Multiple interface options (simple, advanced, legacy)
- ✅ Graceful fallbacks when components fail
- ✅ Clear audio feedback throughout the process
- ✅ No external dependencies that might fail unexpectedly

**If you're building something creative while working with constraints, this is for you.**

---

## 📄 License

MIT License - use, modify, distribute, improve.

---

**Philosophy:** You shouldn't have to fight technology just to capture a thought. Your ideas deserve better tools, and your privacy deserves respect.

*Local-first. Privacy-focused. Built for accessibility.*