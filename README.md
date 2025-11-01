# **🧠 Insight Capsule**

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

This project has a stable, local-first foundation and is now being developed into a full application.

* **✅ COMPLETED:** Core CLI tool, local Whisper transcription, local LLM (Ollama) integration$$cite: \`core/local\_generation.py\`$$  
  , and a stable pipeline.  
* **🚀 IN PROGRESS:** See our full [**ROADMAP.md**](https://www.google.com/search?q=ROADMAP.md) for the "happy path" plan, which includes:  
  * **Phase 1: Tray App** \- Moving from a CLI to an always-on tray application.  
  * **Phase 2: Global Hotkey** \- For true, frictionless "ambient" capture.  
  * **Phase 3: Content Drafting** \- The "closed loop" for turning ideas into outlines.  
  * **Phase 4: Personal Search** \- A natural language search for all your past insights.  
  * **Phase 5: One-Click Install** \- A distributable app for non-technical users.

## **🛠️ Developer Quick Start (Current Version)**

While we build the full app, you can use the stable CLI version today.

### **Prerequisites**

* **Python 3.10+**  
* **Microphone**  
* [**uv**](https://astral.sh/uv) (or pip and venv)  
* [**Ollama**](https://ollama.ai) (Install and run: ollama pull llama3.2)  
* **ffmpeg** (brew install ffmpeg or choco install ffmpeg)

### **Installation & Running**

\# 1\. Clone the repo  
git clone \[https://github.com/ryan258/insight-capsule.git\](https://github.com/ryan258/insight-capsule.git)  
cd insight-capsule

\# 2\. Create environment and install packages (using uv)  
uv venv  
uv pip install \-r requirements.txt

\# 3\. Run the main pipeline\!  
\# This uses the default "press Enter to record" flow  
uv run python main.py

\# 4\. (Optional) Run with advanced CLI options  
uv run python cli.py \--help

### **Environment Configuration**

Create .env file for optional settings:

\# Optional \- only needed if using \--external-llm  
OPENAI\_API\_KEY=your\_key\_here

\# Optional tweaks  
TTS\_ENABLED=true  
WHISPER\_MODEL=base  
TTS\_RATE=170  
USE\_LOCAL\_LLM=true  
LOCAL\_LLM\_MODEL=llama3.2

## **📁 What Gets Saved**

Everything goes in the data/ folder. This is **your** private database.

data/  
├── input\_voice/     \# Your raw audio recordings (.wav)  
└── logs/           \# Full session logs  
    ├── index.md    \# A searchable index of all your insights  
    └── 2025-11-01-123000-my-new-idea.md

*Note: The briefs/ directory has been removed as part of our pipeline simplification.*

**Example log entry (.md):**

\# Insight Capsule Log — 2025-11-01 12:30:00  
\*\*Title:\*\* My New Idea  
\*\*Tags:\*\* \#website \#ms

\*\*Transcript:\*\*  
\> I was thinking about maybe building a small tool for...

\*\*Insight Capsule:\*\*  
This idea centers on creating a focused development...

\*\*Generated Draft: (Blog Post Outline)\*\*  
1\.  Introduction: The challenge of...  
2\.  ...

## **🔧 Troubleshooting**

### **"No local LLM available"**

Make sure the Ollama application is running on your desktop. You can test it by running ollama pull llama3.2 in your terminal.

### **TTS not working**

pyttsx3 can be finicky.

1. Make sure your speakers are on and not muted.  
2. Run the minimal test: uv run python tests/test\_tts\_minimal.py  
3. If all else fails, you can disable it in your .env file with TTS\_ENABLED=false or by running uv run python cli.py \--no-tts.

## **💙 Accessibility Statement**

**This tool was built specifically for creators with physical limitations.**

If traditional input methods are challenging for you, this project aims to provide:

* ✅ Voice-first interaction requiring minimal typing  
* ✅ Intelligent error handling that doesn't break your flow  
* ✅ Clear audio feedback throughout the process  
* ✅ A local-first design that works offline and respects your privacy

**If you're building something creative while working with constraints, this is for you.**