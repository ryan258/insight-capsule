# Release Notes

## **v1.0.0** - Insight Capsule Launch (2025-11-01)

We're excited to announce the first official release of **Insight Capsule** - your voice-first thought partner for capturing, synthesizing, and acting on your ideas.

### **🎯 What is Insight Capsule?**

Insight Capsule is a local-first, privacy-focused application that helps you:
- **Capture** thoughts via voice with zero friction (global hotkey or tray menu)
- **Synthesize** raw ideas into structured insights using local AI
- **Draft** blog posts, outlines, and takeaways from your insights
- **Search** your entire thought library using natural language
- **Never lose** a fleeting idea that could become your next great piece of content

### **✨ Key Features**

#### **🎤 Frictionless Voice Capture**
- **System Tray App**: Runs persistently in your menu bar (macOS) or system tray (Windows/Linux)
- **Global Hotkey**: Press `Ctrl+Shift+Space` from anywhere to toggle recording
- **Silence Detection**: Optionally auto-stop after detecting silence
- **Audio Feedback**: Voice prompts guide you through each step
- **Non-blocking**: Record and process in the background while you work

#### **🧠 Local AI Processing**
- **Privacy-First**: All processing happens on your machine via Ollama
- **Fast Transcription**: OpenAI Whisper converts voice to text locally
- **Smart Synthesis**: Transforms rambling thoughts into coherent insight capsules
- **No Cloud Required**: Works completely offline once set up

#### **✍️ Content Drafting**
Generate from any insight via the Actions menu:
- **Blog Outlines**: 5-point structured outlines ready for expansion
- **First Drafts**: ~500 word drafts for your evergreen guides
- **Key Takeaways**: Extract 3 actionable points from any insight
- **Section Expansion**: Develop specific sections in detail

All drafts are automatically appended to your insight log files.

#### **🔍 Semantic Search**
- **Natural Language Queries**: Ask questions like "what have I thought about productivity?"
- **Vector Search**: Uses ChromaDB and sentence-transformers locally
- **LLM Synthesis**: Combines relevant insights into comprehensive answers
- **Source Citations**: See which insights contributed to each answer
- **Fully Local**: Your search index never leaves your machine

#### **⚙️ Cross-Platform Support**
- **Launch on Startup**: Toggle auto-start with one click
- **macOS**: Full support with LaunchAgent integration
- **Windows**: Registry-based startup (ready for packaging)
- **Linux**: XDG autostart support

### **📦 Installation**

#### **For End Users**

**Prerequisites**:
1. macOS 10.15+ (Catalina or later)
2. [Ollama](https://ollama.ai) - Local LLM runtime

**Installation Steps**:
```bash
# 1. Install Ollama
brew install ollama

# 2. Start Ollama and pull the model
ollama serve &
ollama pull llama3.2

# 3. Install Insight Capsule
# Download InsightCapsule.app from releases
cp -r InsightCapsule.app /Applications/

# 4. Launch and grant permissions
open /Applications/InsightCapsule.app
```

#### **For Developers**

```bash
# Clone the repository
git clone https://github.com/yourusername/insight-capsule.git
cd insight-capsule

# Install dependencies
uv pip install -r requirements.txt

# Run from source
uv run python tray_app.py

# Build distributable app
./build.sh
```

See [DISTRIBUTION.md](DISTRIBUTION.md) for complete build and packaging instructions.

### **🎨 Usage**

#### **Basic Workflow**

1. **Start Recording**:
   - Click the tray icon → "Start Recording", OR
   - Press `Ctrl+Shift+Space` from anywhere

2. **Speak Your Thought**:
   - Talk naturally for as long as you need
   - The app will say "Recording started"

3. **Stop Recording**:
   - Press `Ctrl+Shift+Space` again, OR
   - Wait for silence (if silence detection is enabled), OR
   - Click tray icon → "Stop Recording"

4. **Processing Happens Automatically**:
   - Transcription → Synthesis → Save to log
   - Watch the tray icon change colors:
     - 🔵 Blue = Ready
     - 🔴 Red = Recording
     - 🟠 Orange = Processing
     - 🟢 Green = Complete

5. **Take Action** (Optional):
   - Click "Search My Thoughts..." to query your insights
   - Use "Actions" menu to generate blog content
   - Click "Open Logs Folder" to see all your insights

#### **Tray Menu Reference**

- **Start Recording** - Begin capturing audio
- **Stop Recording** - Stop and process current recording
- **Search My Thoughts...** - Query your insight library
- **Actions** →
  - Generate Blog Outline
  - Generate First Draft
  - Generate Key Takeaways
- **Open Logs Folder** - View saved insights
- **Launch on Startup** - Toggle auto-start
- **Quit** - Exit the application

### **⚙️ Configuration**

Create a `.env` file in the app's data directory (or copy `.example.env`):

```bash
# Local LLM Settings
USE_LOCAL_LLM=true
LOCAL_LLM_URL=http://localhost:11434
LOCAL_LLM_MODEL=llama3.2

# Audio Recording
SILENCE_DETECTION_ENABLED=false  # Auto-stop on silence
SILENCE_THRESHOLD=0.01           # Amplitude threshold
SILENCE_DURATION=3.0             # Seconds of silence

# Text-to-Speech
TTS_ENABLED=true                 # Voice feedback
TTS_RATE=170                     # Words per minute

# Whisper Transcription
WHISPER_MODEL=base              # tiny, base, small, medium, large

# Pipeline Settings
MAX_CAPSULE_WORDS=400           # Max insight capsule length
DEFAULT_TEMPERATURE=0.7          # LLM creativity (0.0-1.0)
```

### **📊 Technical Details**

**Architecture**:
- **Core**: Audio recording, transcription, TTS, storage
- **Agents**: Synthesizer, Drafter, Searcher
- **Pipeline**: Orchestrates the full capture → process → store workflow
- **Vector Store**: ChromaDB for semantic search
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)

**Dependencies**:
- Python 3.11+
- OpenAI Whisper (local transcription)
- Ollama (local LLM)
- ChromaDB (vector database)
- pystray (system tray)
- pynput (global hotkeys)

**Privacy & Security**:
- ✅ All processing happens locally
- ✅ No data sent to cloud services
- ✅ Your insights stay on your machine
- ✅ Open source and auditable

### **🔧 Known Issues & Limitations**

1. **macOS Only** (for v1.0.0):
   - Windows/Linux support exists in code but packaging not yet tested
   - Future releases will include cross-platform builds

2. **Ollama Required**:
   - Users must install Ollama separately (not bundled)
   - Future versions may include easier setup

3. **First Launch**:
   - May take a moment to download sentence-transformer model
   - Subsequent launches are fast

4. **Permissions**:
   - Requires microphone access (for recording)
   - Requires accessibility access (for global hotkeys)

### **🛠️ Troubleshooting**

**App won't open**:
```bash
# Remove quarantine flag
xattr -cr /Applications/InsightCapsule.app
```

**Global hotkey not working**:
- Go to System Preferences → Security & Privacy → Privacy → Accessibility
- Add InsightCapsule to the allowed apps

**No audio recording**:
- Check microphone permissions in System Preferences
- Ensure Whisper model is downloaded (happens automatically on first use)

**Search not working**:
- Create at least one insight first
- Check that ChromaDB initialized (look for `data/vectorstore` directory)

**See logs**:
```bash
# View application logs
tail -f data/logs/*.log
```

### **📚 Documentation**

- [README.md](README.md) - Quick start guide
- [ROADMAP.md](ROADMAP.md) - Complete development journey
- [DISTRIBUTION.md](DISTRIBUTION.md) - Build and packaging guide
- [BASE_HARDENING_SUMMARY.md](BASE_HARDENING_SUMMARY.md) - Technical architecture

### **🙏 Acknowledgments**

Built with:
- OpenAI Whisper - Speech-to-text
- Ollama - Local LLM runtime
- ChromaDB - Vector database
- sentence-transformers - Semantic embeddings

Special thanks to the open-source community for making local-first AI accessible to everyone.

### **🚀 What's Next?**

Potential future enhancements:
- **Cross-platform builds** (Windows .exe, Linux AppImage)
- **Custom voices** for TTS
- **Export formats** (Markdown, HTML, PDF)
- **Sync options** (optional cloud backup)
- **Plugin system** for custom agents
- **Mobile companion** (iOS/Android)

### **📝 License**

[Your chosen license - e.g., MIT, GPL, etc.]

### **💬 Feedback & Support**

- **Issues**: [GitHub Issues](https://github.com/yourusername/insight-capsule/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/insight-capsule/discussions)
- **Email**: [your@email.com]

---

**Thank you for trying Insight Capsule!** We hope it helps you capture, develop, and act on your best ideas. 🧠✨
