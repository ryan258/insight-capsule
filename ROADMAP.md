# 🛣️ Insight Capsule — Project Roadmap (UPDATED)

> **New Mission**: Build a truly local-first, voice-activated pipeline for generating thoughtful insights with zero external dependencies and maximum accessibility.

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

- [x] ✅ **Replaced edge-tts with working pyttsx3 TTS** with proper cross-platform fallbacks
- [x] ✅ **Fixed async/sync conflicts** - clean separation of sync operations
- [x] ✅ **Replaced "print & hang" flows** with graceful error handling and user feedback
- [x] ✅ **Added "Safe Mode" via TTS_ENABLED config** - disables TTS entirely if needed
- [x] ✅ **Ensured TTS speaks actual content** with proper blocking and error recovery
- [x] ✅ **Comprehensive exception handling** with custom exception types
- [x] ✅ **Environment validation system** to catch issues before they break workflow

---

## ✅ Phase 3: Usability Upgrades (COMPLETED)

- [x] ✅ **Added clear progress indicators** between pipeline steps with TTS feedback
- [x] ✅ **Clean log filenames** with automatic slugification of titles
- [x] ✅ **Advanced CLI interface** with options for audio files, TTS control, model selection
- [x] ✅ **Multiple entry points** (simple main.py, advanced cli.py, legacy record_and_run.py)

---

## ✅ Phase 4: Modularity & Agent Architecture (COMPLETED)

- [x] ✅ **Full modular architecture** with core/, agents/, pipeline/, config/ separation
- [x] ✅ **Agent: ClarifierAgent** — parse + reframe rough ideas into structured briefs (Now removed due to workflow simplification)
- [x] ✅ **Agent: SynthesizerAgent** — generate concise insight capsules
- [x] ✅ **Agent: StorageManager** — handle file organization and indexing
- [x] ✅ **Agent: AudioRecorder** — manage voice recording with real-time feedback
- [x] ✅ **Agent: GPTGenerator** — handle all AI operations with role-based models
- [x] ✅ **Agent: TextToSpeech** — manage speech output with intelligent fallbacks
- [x] ✅ **Agent: Transcriber** — handle Whisper integration with lazy loading

---

## 🔄 Phase 5: Local-First Revolution (IN PROGRESS)

> **PRIORITY SHIFT**: Eliminate external dependencies and achieve true offline capability

### 🏠 Local LLM Integration (IN PROGRESS)

- [x] ✅ **LocalGenerator class** with Ollama integration
- [x] ✅ **HybridGenerator** for seamless local/external fallback
- [x] ✅ **Pipeline integration** with local model support
- [x] ✅ **CLI flags** for choosing local vs external models
- [ ] 🔧 **Model optimization** for specific insight generation tasks
- [ ] 🔧 **Local model caching** and startup optimization
- [ ] 🔧 **Custom prompts** tuned for local models (simpler, more direct)

### 🎯 Workflow Simplification (IN PROGRESS)

- [x] ✅ **Remove creative brief step** - go directly from transcript to insight
- [x] ✅ **Focus on core value**: voice → clean transcription → meaningful summary → organized storage (Achieved by removing brief)
- [ ] 🎯 **Streamline agent interactions** - reduce complexity without losing modularity (Partially addressed by removing ClarifierAgent. Further review might be needed for SynthesizerAgent's directness.)
- [ ] 🎯 **Accessibility testing** with actual users who have mobility constraints

### 🔒 Privacy & Offline

- [ ] 🔒 **Complete offline mode** validation and testing
- [ ] 🔒 **Data retention controls** - user decides what gets saved and where
- [ ] 🔒 **Export capabilities** without external services
- [ ] 🔒 **Remove all external API dependencies** from default workflow

---

## 🧹 Phase 6: Technical Debt & Cleanup (IN PROGRESS)

> Clean up the codebase and remove legacy complexity

### 🗑️ Legacy Removal

- [x] 🗑️ **Remove record_and_run.py** - consolidate to single pipeline approach
- [x] 🗑️ **Remove utils/gpt_interface.py** and **utils/whisper_wrapper.py** - superseded by core modules
- [x] 🗑️ **Remove agents/clarifier_agent.py** - duplicate of agents/clarifier.py
- [x] 🗑️ **Clean up test files** - integrate into proper test suite (Initial cleanup: moved to tests/ directory)

### 🧪 Testing & Quality

- [ ] 🧪 **Comprehensive test suite** for all core functionality
- [ ] 🧪 **Integration tests** for full pipeline with local models
- [ ] 🧪 **Performance benchmarking** of local vs external models
- [ ] 🧪 **Memory usage optimization** for long-running sessions

---

## 🎨 Phase 7: User Experience Refinement (PLANNED)

> Polish the experience for daily use by people with accessibility needs

### 🎙️ Audio Improvements

- [ ] 🎙️ **Audio level visualization** during recording
- [ ] 🎙️ **Configurable recording sensitivity** for different microphone setups
- [ ] 🎙️ **Background noise filtering** for cleaner transcription
- [ ] 🎙️ **Multiple audio format support** beyond WAV

### 📝 Output Improvements

- [ ] 📝 **Configurable insight lengths** (short summaries vs detailed analysis)
- [ ] 📝 **Multiple output formats** (plain text, markdown, structured notes)
- [ ] 📝 **Smart tagging system** based on content analysis
- [ ] 📝 **Search functionality** across historical insights

### ⌨️ Accessibility Features

- [ ] ⌨️ **Voice commands** for basic control (start, stop, repeat, save)
- [ ] ⌨️ **Configurable TTS voices** and speeds
- [ ] ⌨️ **Large text mode** for visual output
- [ ] ⌨️ **Keyboard shortcut alternatives** for all mouse actions

---

## 📦 Phase 8: Distribution & Sharing (FUTURE)

> Make it easy for others to use while maintaining local-first principles

### 🚀 Packaging

- [ ] 📦 **Simple installer** for non-technical users
- [ ] 📦 **Docker containerization** for cross-platform consistency
- [ ] 📦 **Portable executable** version (no Python installation required)
- [ ] 📦 **Model bundling** options for completely offline distribution

### 🔗 Export & Integration

- [ ] 🔗 **Export to common note-taking apps** (Obsidian, Notion, Markdown files)
- [ ] 🔗 **Email integration** for sharing insights
- [ ] 🔗 **Calendar integration** for scheduled insight sessions
- [ ] 🔗 **Backup and sync** options that respect privacy

---

## 🎯 Current Priorities (Next 2-4 Weeks)

1. **Complete local LLM integration** - ensure Ollama setup is smooth and reliable. Focus on model optimization, caching, and custom prompts.
2. **Continue Workflow Simplification** - Focus on streamlining remaining agent interactions and prepare for accessibility testing.
3. **Test with real users** - validate the accessibility value proposition (after current simplification).
4. **Documentation update** - reflect the new local-first architecture and recent changes.

---

## 🧯 Updated Pain Points & Solutions

| Old Problem         | New Local-First Solution          | Status                         |
| ------------------- | --------------------------------- | ------------------------------ |
| OpenAI API costs    | Local LLM with Ollama             | ✅ Implemented                 |
| Internet dependency | Fully offline pipeline            | 🔄 In Progress                 |
| Privacy concerns    | Zero external data sharing        | 🔄 In Progress                 |
| Complex workflow    | Simplified voice→insight→storage  | ✅ Implemented (brief removed) |
| Over-engineering    | Focus on core accessibility value | 🔄 In Progress                 |

---

## 🎯 Refined Mission Statement

**Enable voice-first, hands-free creative workflows for users with limited physical control, using entirely local processing to ensure privacy, reliability, and zero ongoing costs.**

**Core Values:**

- **Local-first**: No internet required after initial setup
- **Accessibility-focused**: Designed for users with mobility constraints
- **Privacy-respecting**: Your thoughts stay on your computer
- **Reliability**: Works when you need it, regardless of external services
- **Simplicity**: Complex under the hood, simple to use

---

## 🔚 Success Metrics

- [ ] **Zero external API calls** in default operation mode
- [ ] **Sub-10 second** end-to-end processing time for typical voice notes
- [ ] **Accessible to non-technical users** with simple installation
- [ ] **Positive feedback** from users with accessibility needs
- [ ] **Daily use viability** - stable enough for regular workflow integration

**Status: Pivoting to true local-first architecture. Core mission clarified and focused. Legacy code cleanup significantly progressed. Workflow simplification (brief removal) completed.**
