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

## **🚀 The Path Forward (The "Happy Path" Plan)**

With a stable, local-first foundation, we can now focus on the "ideal" user experience, moving from a CLI tool to a true "thought partner."

### **Phase 1: The "App-ification" — From CLI to Tray**

**Goal:** Move the tool from a script you *run* to an application that's *always available* in your system tray (menu bar on Mac, tray on Windows). This is the foundation for all future "ambient" features.

**Why:** To remove the first major point of friction: having to open a terminal. This makes capturing an idea as simple as clicking an icon.

**Key Tasks:**

* \[ \] **Refactor InsightPipeline:** Turn the orchestrator \[cite: pipeline/orchestrator.py\] into a long-running service or class that can be triggered on demand.  
* \[ \] **Build Tray Icon:** Use a library like pystray (cross-platform) to create a persistent icon in the system tray.  
* \[ \] **Add Basic Controls:** The tray icon's menu should have, at minimum:  
  * "Start Recording" (triggers the audio recording \[cite: core/audio.py\])  
  * "Stop Recording"  
  * "Open Logs Folder" (opens the data/logs directory \[cite: core/storage.py\])  
  * "Quit"  
* \[ \] **Launch on Startup:** Add a preference (and code) to make the app launch when the computer starts.

**Success Metric:** You can capture a full insight (record, transcribe, synthesize, save) without ever opening a terminal.

### **Phase 2: Frictionless Capture — The Global Hotkey**

**Goal:** Implement a global hotkey (e.g., Ctrl+Shift+Space) to start/stop recording from *any* application.

**Why:** This removes the *final* piece of physical friction. You no longer have to stop what you're doing, find the tray icon, and click. You can capture a thought while you're in the middle of writing or browsing, making it truly "ambient."

**Key Tasks:**

* \[ \] **Implement Hotkey Listener:** Use a library like keyboard or pynput to listen for a global hotkey combination.  
* \[ \] **Connect Hotkey to Pipeline:** Wire the hotkey to the "Start/Stop Recording" function from Phase 1\.  
* \[ \] **Refine Audio Feedback:** Ensure the TTS feedback ("Recording started," "Processing...") \[cite: core/tts.py\] is crisp and immediate, as you won't have visual confirmation from a terminal.  
* \[ \] **(Optional) Silence Detection:** Upgrade the audio recorder to *optionally* stop recording automatically after 5-10 seconds of silence.

**Success Metric:** You can be typing an email, have a thought, press the hotkey, speak your mind, press it again, and continue your email, knowing the idea is captured.

### **Phase 3: The "Closed Loop" — From Insight to Draft**

**Goal:** Connect your captured insights directly to your primary content creation workflow for ryanleej.com.

**Why:** This is the *payoff*. The tool stops being just a *library* and becomes an *active assistant*. It helps you battle the "blank page" by turning your raw, spoken ideas (like your MS journey insights) into structured outlines and first drafts for your evergreen guides.

**Key Tasks:**

* \[ \] **Create a "Drafting" Agent:** Build a new function (similar to your Synthesizer \[cite: agents/synthesizer.py\]) that uses the local LLM.  
* \[ \] **Define New Prompts:** This agent will take a *capsule* as input and follow a new prompt, such as:  
  * "You are a content strategist. Turn the following insight into a 5-point blog post outline."  
  * "Create a 'first draft' of 3 paragraphs based on this idea, intended for an evergreen guide."  
* \[ \] **Add "Actions" Menu:** Add a new "Actions" submenu to your tray icon. When you complete an insight, it could ask:  
  * "What's next?"  
    * "Draft Blog Outline"  
    * "Export to Markdown"  
* \[ \] **Improve Log Format:** Save these new drafts alongside the original transcript and capsule in the log file \[cite: core/storage.py\].

**Success Metric:** You can go from a spoken thought to a blog post outline in under 60 seconds, all within the same tool.

### **Phase 4: The Insight Library — Your Personal Search Engine**

**Goal:** Make your entire log history searchable using natural language.

**Why:** To find old ideas and connect concepts. Instead of just *storing* thoughts, you can *ask questions* of your past self (e.g., "What ideas did I have for my 'MS and fatigue' guide?").

**Key Tasks:**

* \[ \] **Local Vector DB:** Integrate a simple, file-based vector database (like LanceDB or ChromaDB).  
* \[ \] **Embedding Generation:** When a new log is saved, create a background task that generates vector embeddings (using a local model) for the transcript and capsule.  
* \[ \] **"Search" Interface:** Add a "Search My Thoughts..." command to the tray icon that opens a simple prompt.  
* \[ \] **Search Pipeline:**  
  1. User types a query ("ideas about diet").  
  2. The query is embedded.  
  3. You find the 5-10 most relevant log files from your vector DB.  
  4. You feed those relevant texts to your local LLM with a prompt like: "Based on these past thoughts, answer the user's query: 'ideas about diet'."  
  5. The LLM synthesizes an answer, and your TTS speaks it.

**Success Metric:** You can ask your app a question and get a synthesized answer based on *your own* past recordings, not the public internet.

### **Phase 5: Distribution — The "One-Click" Install**

**Goal:** Package the entire application so it can be installed by a non-technical user (especially others who need an accessibility-first tool).

**Why:** This fulfills the highest goal of accessibility: making the tool available to *everyone* who needs it, not just developers.

**Key Tasks:**

* \[ \] **Package with PyInstaller:** Use a tool like PyInstaller or Nuitka to bundle your entire Python app and its dependencies into a single .exe (Windows) or .app (macOS) file.  
* \[C\] **Create a Simple Installer:** Use Inno Setup (Windows) or create a .dmg (macOS) to make it user-friendly.  
* \[ \] **The "Hard Part": Bundle Ollama:** The installer must:  
  1. Check if Ollama is installed.  
  2. If not, bundle and run the Ollama installer.  
  3. Run the necessary command (ollama pull llama3.2) on the user's behalf.  
  4. Set your app to launch at login.

**Success Metric:** You can give a single file to a friend, and they can install and use Insight Capsule without ever touching a terminal or knowing what Python or uv is.