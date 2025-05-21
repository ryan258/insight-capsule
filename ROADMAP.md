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

## ⚠️ Phase 2: **Stabilization & Reliability Pass**

> We fix what hurts. Prioritize **resilience**, **feedback**, and **non-blocking failures**.

### 🧰 Fixes & Improvements (ASAP)

- [ ] 🔄 Replace edge-tts with a **working, cross-platform fallback TTS** (gTTS with MP3 + ffplay or `pyttsx3`)
- [ ] 🐞 Fix async/sync conflicts in TTS (don't mix asyncio.run inside event loops)
- [ ] ✅ Replace all "print & hang" flows with **failsafe debug messages + graceful fallback**
- [ ] ✅ Add a "Safe Mode" config flag: disables TTS entirely if it causes errors
- [ ] ✅ Ensure TTS plays actual spoken content before proceeding to next step (blocking play confirmed)

---

## 🧠 Phase 3: Usability Upgrades

> Improve the experience, reduce the need for any manual fiddling.

- [ ] 🔘 Add startup beep or tone to signal recording started
- [ ] ⏱️ Add speech duration countdown (text-based)
- [ ] 🔁 Add retry option after capsule generation (optional)
- [ ] 🧼 Clean log filenames (auto-slugify titles)
- [ ] 📜 Show progress bar or loading indicator between steps

---

## 🚀 Phase 4: Modularity & Agent Architecture

> Start modularizing the system into clear, testable "agent behaviors"

- [ ] 🤖 Agent: `clarifier_agent.py` — parse + reframe rough ideas
- [ ] 🤖 Agent: `fact_checker.py` — optional validation (optional)
- [ ] 🤖 Agent: `tone_controller.py` — modify emotional tone
- [ ] 🔀 Add agent configuration to `.env` or YAML file

---

## 🌍 Phase 5: Export & Distribution

> Share or build with this tool as a backbone

- [ ] 📦 Export as HTML/Markdown zine-style pages
- [ ] 📤 Send to Notion / Obsidian / Git-based journal
- [ ] 🔗 Simple GUI frontend (Tkinter or Streamlit-based)
- [ ] ☁️ (Optional) Add HuggingFace Spaces or web dashboard

---

## 🧯 Contingency: Known Pain Points

| Problem                       | Workaround (Temp)              |
| ----------------------------- | ------------------------------ |
| TTS fails silently            | Use `ffplay` beep fallback     |
| `asyncio.run()` conflict      | Wrap inside `try...except`     |
| Whisper crashing on CPU       | Use smaller model (tiny, base) |
| Long capsule generation hangs | Add timeout + retry prompt     |

---

## 🔚 Final Mission

To enable **voice-first**, hands-free creative workflows  
for users with **limited physical control**, without reliance on the cloud.

Every word should matter.  
Every process should serve your **cognitive clarity** — not clutter it.

---
