# 🛣️ Insight Capsule — Project Roadmap

> Purpose: Build a local-first, voice-activated pipeline for generating high-quality, thought artifacts with minimal friction.

---

## ✅ Phase 1: Core Prototype (COMPLETED)

- [x] ✅ Local Python project setup with virtualenv
- [x] ✅ Voice recording until Enter is pressed
- [x] ✅ Whisper transcription (local)
- [x] ✅ GPT-based creative brief generation
- [x] ✅ GPT-based insight capsule generation
- [x] ✅ Save logs + index logs
- [x] ✅ Basic TTS fallback (ffplay beep, edge-tts, gTTS attempts)

---

## ✅ Phase 2: Stabilization & Reliability Pass (COMPLETED)

> We fixed what hurt. Prioritized **resilience**, **feedback**, and **non-blocking failures**.

### 🧰 Fixes & Improvements (COMPLETED)

- [x] ✅ **Replaced edge-tts with working pyttsx3 TTS** with proper cross-platform fallbacks
- [x] ✅ **Fixed async/sync conflicts** - clean separation of sync operations
- [x] ✅ **Replaced "print & hang" flows** with graceful error handling and user feedback
- [x] ✅ **Added "Safe Mode" via TTS_ENABLED config** - disables TTS entirely if needed
- [x] ✅ **Ensured TTS speaks actual content** with proper blocking and error recovery
- [x] ✅ **Comprehensive exception handling** with custom exception types
- [x] ✅ **Environment validation system** to catch issues before they break workflow

---

## ✅ Phase 3: Usability Upgrades (MOSTLY COMPLETED)

> Improved the experience, reduced manual fiddling.

- [x] ✅ **Added clear progress indicators** between pipeline steps with TTS feedback
- [x] ✅ **Clean log filenames** with automatic slugification of titles
- [x] ✅ **Advanced CLI interface** with options for audio files, TTS control, model selection
- [x] ✅ **Multiple entry points** (simple main.py, advanced cli.py, legacy record_and_run.py)
- [ ] 🔘 Add startup beep or tone to signal recording started
- [ ] ⏱️ Add speech duration countdown (text-based)
- [ ] 🔁 Add retry option after capsule generation (optional)

---

## ✅ Phase 4: Modularity & Agent Architecture (COMPLETED)

> Fully modularized system into clear, testable "agent behaviors"

- [x] ✅ **Full modular architecture** with core/, agents/, pipeline/, config/ separation
- [x] ✅ **Agent: ClarifierAgent** — parse + reframe rough ideas into structured briefs
- [x] ✅ **Agent: SynthesizerAgent** — generate concise insight capsules
- [x] ✅ **Agent: StorageManager** — handle file organization and indexing
- [x] ✅ **Agent: AudioRecorder** — manage voice recording with real-time feedback
- [x] ✅ **Agent: GPTGenerator** — handle all AI operations with role-based models
- [x] ✅ **Agent: TextToSpeech** — manage speech output with intelligent fallbacks
- [x] ✅ **Agent: Transcriber** — handle Whisper integration with lazy loading
- [x] ✅ **Full agent configuration** via settings.py and environment variables
- [ ] 🤖 Agent: `fact_checker.py` — optional validation system
- [ ] 🤖 Agent: `tone_controller.py` — modify emotional tone

---

## 🔄 Phase 5: Optimization & Polish (IN PROGRESS)

> Fine-tune the experience and performance

### 🚀 Performance Improvements
- [ ] ⚡ **Lazy loading optimization** for Whisper models (partially done)
- [ ] ⚡ **Concurrent processing** where possible (transcription + brief generation)
- [ ] ⚡ **Model caching** to reduce startup times
- [ ] 📊 **Usage analytics** and performance monitoring
- [ ] 🎯 **Smart model selection** based on input length/complexity

### 🎨 User Experience
- [ ] 🎙️ **Audio level visualization** during recording
- [ ] ⏸️ **Pause/resume recording** functionality
- [ ] 🔄 **Edit/retry individual steps** without full pipeline restart
- [ ] 📝 **Quick note mode** for shorter insights
- [ ] 🏷️ **Enhanced tagging system** with auto-suggestions

---

## 🌍 Phase 6: Export & Distribution (PLANNED)

> Share and integrate with existing workflows

### 📤 Export Capabilities
- [ ] 📦 **Export as HTML/Markdown** zine-style pages
- [ ] 📤 **Send to Notion / Obsidian** / Git-based journal
- [ ] 📧 **Email integration** for sharing insights
- [ ] 📱 **Mobile-friendly export** formats
- [ ] 🔗 **URL sharing** for generated insights

### 🖥️ Interface Options
- [ ] 🔗 **Simple GUI frontend** (Tkinter or Streamlit-based)
- [ ] 🌐 **Web dashboard** with session management
- [ ] ☁️ **HuggingFace Spaces deployment** option
- [ ] 📱 **Mobile companion app** for voice capture

---

## 🧠 Phase 7: Advanced AI Features (FUTURE)

> Enhance the AI capabilities and intelligence

### 🤖 Enhanced Agents
- [ ] 🧠 **Multi-modal input** (text + voice simultaneously)
- [ ] 🔍 **Context awareness** across sessions
- [ ] 📚 **Knowledge base integration** with personal documents
- [ ] 🎯 **Personalized output styles** based on user preferences
- [ ] 🔄 **Interactive refinement** of generated content

### 🔬 Advanced Processing
- [ ] 🧪 **Sentiment analysis** and emotional context
- [ ] 🔗 **Automatic cross-referencing** with previous insights
- [ ] 📈 **Trend analysis** across captured thoughts
- [ ] 🎨 **Creative expansion modes** (poetry, narrative, technical)

---

## 🧯 Resolved Pain Points

| Problem                       | Solution Implemented           | Status |
| ----------------------------- | ------------------------------ | ------ |
| TTS fails silently            | pyttsx3 with proper error handling + fallbacks | ✅ Fixed |
| `asyncio.run()` conflict      | Eliminated async mixing, pure sync pipeline | ✅ Fixed |
| Whisper crashing on CPU       | Lazy loading + configurable models | ✅ Fixed |
| Long capsule generation hangs | Proper error handling + user feedback | ✅ Fixed |
| Poor error messages           | Custom exceptions + validation system | ✅ Fixed |
| Inconsistent file organization| StorageManager with automatic indexing | ✅ Fixed |
| No progress feedback          | TTS + text feedback throughout pipeline | ✅ Fixed |

---

## 🚀 Current Development Priorities

1. **Complete Phase 5 optimizations** - focus on performance and UX polish
2. **Add fact-checking agent** for optional content validation
3. **Implement GUI frontend** for users who prefer visual interfaces
4. **Export system** for integration with existing note-taking workflows
5. **Enhanced tagging and organization** features

---

## 🔚 Final Mission

To enable **voice-first**, hands-free creative workflows  
for users with **limited physical control**, without reliance on the cloud.

Every word should matter.  
Every process should serve your **cognitive clarity** — not clutter it.

**Status: The core mission is achieved. Now we optimize and expand.**

---

## 🏗️ Technical Debt & Maintenance

### Code Quality
- [ ] 🧪 **Comprehensive test suite** for all agents and core functionality
- [ ] 📖 **API documentation** for all modules
- [ ] 🔍 **Code coverage analysis** and improvement
- [ ] 🏗️ **Refactor legacy modules** (gpt_interface.py, whisper_wrapper.py)

### Infrastructure
- [ ] 🐳 **Docker containerization** for easy deployment
- [ ] 📦 **Package distribution** via PyPI
- [ ] 🔄 **Automated CI/CD** pipeline
- [ ] 📋 **Version management** and release process