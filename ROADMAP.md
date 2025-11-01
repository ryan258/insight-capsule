# **🧠 Insight Capsule: The Full Project Roadmap**

**Mission:** To create a zero-friction, voice-first "thought partner" that moves with you. It captures, synthesizes, and retrieves your ideas locally, helping you turn passing thoughts into evergreen content for your creative work.

This document outlines the entire project journey, from the initial prototype to the ideal "happy path" we are now working towards.

## **✅ Completed Milestones (The Story So Far)**

We have successfully built the core foundation of the application, proving the concept and solving the hardest technical challenges.

* **Phase 1: Core Prototype (COMPLETED)**  
  * Established the initial Python project, voice recording, and Whisper transcription.  
* **Phase 2: Stabilization & Reliability (COMPLETED)**  
  * Replaced unstable components, fixed async/sync conflicts, and implemented a reliable pyttsx3 TTS fallback system.  
* **Phase 3: Usability Upgrades (COMPLETED)**  
  * Added clear TTS progress indicators between pipeline steps and built an advanced cli.py entry point.  
* **Phase 4: Modularity & Agent Architecture (COMPLETED)**  
  * Refactored the entire project into a clean, modular architecture with core/, agents/, and pipeline/ separation.  
* **Phase 5: Local-First Revolution (COMPLETED)**  
  * Successfully pivoted the project to be **local-first**. This involved:  
    * Building the LocalGenerator and HybridGenerator to use Ollama \[cite: core/local\_generation.py\].  
    * Removing the dependency on external (OpenAI) APIs for the default workflow.  
    * **Simplifying the pipeline** by removing the "creative brief" step, moving to a direct transcript \-\> insight workflow \[cite: pipeline/orchestrator.py\].   
* **Phase 6: Technical Debt & Cleanup (COMPLETED)**  
  * Removed legacy scripts and consolidated the project to a single, clean pipeline, making it ready for future development.

The base is now solid, tested, and production-ready. The interactive manual tests (test_tts_minimal.py, test_tts.py) are still there for manual TTS testing when needed, but they won't interfere with automated testing anymore.

## **🚀 The Path Forward (The "Happy Path" Plan)**

With a stable, local-first foundation, we can now focus on the "ideal" user experience, moving from a CLI tool to a true "thought partner."

### **✅ Phase 1: The "App-ification" — From CLI to Tray (COMPLETED)**

**Goal:** Move the tool from a script you *run* to an application that's *always available* in your system tray (menu bar on Mac, tray on Windows). This is the foundation for all future "ambient" features.

**Why:** To remove the first major point of friction: having to open a terminal. This makes capturing an idea as simple as clicking an icon.

**Key Tasks:**

* \[✓\] **Refactor InsightPipeline:** Turned the orchestrator \[cite: pipeline/orchestrator.py\] into a long-running service with state management, threading, and callbacks.
* \[✓\] **Build Tray Icon:** Created tray_app.py using pystray with dynamic color-coded icon (blue=ready, red=recording, orange=processing, green=complete).
* \[✓\] **Add Basic Controls:** The tray icon's menu includes:
  * "Start Recording" (enabled when not busy)
  * "Stop Recording" (enabled when recording)
  * "Open Logs Folder" (opens the data/logs directory)
  * "Launch on Startup" (toggle checkbox)
  * "Quit"
* \[✓\] **Launch on Startup:** Implemented cross-platform startup manager \[cite: utils/startup.py\] supporting macOS (LaunchAgent), Windows (Registry), and Linux (.desktop files).

**Success Metric:** ✅ You can now capture a full insight (record, transcribe, synthesize, save) without ever opening a terminal. The app runs persistently in your system tray.

### **✅ Phase 2: Frictionless Capture — The Global Hotkey (COMPLETED)**

**Goal:** Implement a global hotkey (e.g., Ctrl+Shift+Space) to start/stop recording from *any* application.

**Why:** This removes the *final* piece of physical friction. You no longer have to stop what you're doing, find the tray icon, and click. You can capture a thought while you're in the middle of writing or browsing, making it truly "ambient."

**Key Tasks:**

* \[✓\] **Implement Hotkey Listener:** Integrated pynput to listen for Ctrl+Shift+Space globally across all applications.
* \[✓\] **Connect Hotkey to Pipeline:** Wired the hotkey to toggle recording (start if idle, stop if recording) via InsightPipeline's async methods.
* \[✓\] **Refine Audio Feedback:** TTS feedback ("Recording started," "Processing...") provides immediate audio confirmation without visual terminal output.
* \[✓\] **Silence Detection:** Added optional auto-stop after configurable silence duration (default 3s) \[cite: config/settings.py, core/audio.py\]. Enable via `SILENCE_DETECTION_ENABLED=true`.

**Success Metric:** ✅ You can now be typing an email, have a thought, press Ctrl+Shift+Space, speak your mind, press it again (or wait for silence detection), and continue your email, knowing the idea is captured and being processed.

### **✅ Phase 3: The "Closed Loop" — From Insight to Draft (COMPLETED)**

**Goal:** Connect your captured insights directly to your primary content creation workflow for ryanleej.com.

**Why:** This is the *payoff*. The tool stops being just a *library* and becomes an *active assistant*. It helps you battle the "blank page" by turning your raw, spoken ideas (like your MS journey insights) into structured outlines and first drafts for your evergreen guides.

**Key Tasks:**

* \[✓\] **Create a "Drafting" Agent:** Built DrafterAgent \[cite: agents/drafter.py\] with methods for generating blog outlines, first drafts, key takeaways, and section expansions.
* \[✓\] **Define New Prompts:** Created specialized prompts for:
  * `generate_blog_outline()` - Produces 5-point structured blog outlines
  * `generate_first_draft()` - Creates ~500 word first drafts for evergreen guides
  * `generate_key_takeaways()` - Extracts 3 actionable takeaways
  * `expand_section()` - Develops specific sections in detail
* \[✓\] **Add "Actions" Menu:** Added "Actions" submenu to tray icon with:
  * "Generate Blog Outline" (creates structured outline)
  * "Generate First Draft" (writes full draft)
  * "Generate Key Takeaways" (extracts main points)
  * All actions enabled when a recent insight exists
* \[✓\] **Improve Log Format:** All drafts are automatically appended to the original log file with clear section headers, keeping everything together.

**Success Metric:** ✅ You can now go from a spoken thought to a blog post outline or first draft in under 60 seconds, all within the same tool. The drafts are saved alongside your original insights for easy reference.

### **✅ Phase 4: The Insight Library — Your Personal Search Engine (COMPLETED)**

**Goal:** Make your entire log history searchable using natural language.

**Why:** To find old ideas and connect concepts. Instead of just *storing* thoughts, you can *ask questions* of your past self (e.g., "What ideas did I have for my 'MS and fatigue' guide?").

**Key Tasks:**

* \[✓\] **Local Vector DB:** Installed ChromaDB and sentence-transformers for local vector search.
* \[✓\] **Embedding Generation:** Created VectorStore module \[cite: core/vectorstore.py\] using sentence-transformers (all-MiniLM-L6-v2) for generating embeddings.
* \[✓\] **"Search" Interface:** Added "Search My Thoughts..." command to tray menu that prompts for natural language queries.
* \[✓\] **Search Pipeline:** Built SearcherAgent \[cite: agents/searcher.py\] that:
  1. Takes user's natural language query
  2. Generates embedding for the query
  3. Finds 5-10 most semantically similar insights from vector DB
  4. Feeds relevant insights to local LLM with context
  5. Synthesizes a comprehensive answer
  6. Speaks the answer via TTS with source citations
* \[✓\] **Automatic Indexing:** All new insights are automatically added to the vector store during processing.

**Success Metric:** ✅ You can now ask your app a question like "what have I thought about productivity?" and get a synthesized answer based on *your own* past recordings, with source citations, all powered by local models.

### **✅ Phase 5: Distribution — The "One-Click" Install (COMPLETED)**

**Goal:** Package the entire application so it can be installed by a non-technical user (especially others who need an accessibility-first tool).

**Why:** This fulfills the highest goal of accessibility: making the tool available to *everyone* who needs it, not just developers.

**Key Tasks:**

* \[✓\] **Package with PyInstaller:** Created InsightCapsule.spec file that bundles the entire Python app and all dependencies into a standalone .app bundle for macOS.
* \[✓\] **Build Automation:** Added build.sh script for one-command building (`./build.sh`).
* \[✓\] **Distribution Guide:** Created comprehensive DISTRIBUTION.md \[cite: DISTRIBUTION.md\] with:
  - Complete build instructions for developers
  - Installation steps for end users
  - DMG creation guide for professional distribution
  - Code signing and notarization instructions
  - Troubleshooting section
* \[✓\] **Ollama Integration:** Documented clear Ollama installation process with step-by-step commands for end users.
* \[✓\] **Launch on Startup:** Built-in toggle in tray menu (already implemented in Phase 1).

**Success Metric:** ✅ A developer can run `./build.sh` to create `dist/InsightCapsule.app`. An end user can install Ollama (one-time), drag the app to Applications, grant permissions, and start capturing insights within 5 minutes. See [DISTRIBUTION.md](DISTRIBUTION.md) for complete instructions.