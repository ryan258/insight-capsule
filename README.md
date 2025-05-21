# 🧠 Insight Capsule Generator

A personal AI swarm system for generating concise, scrollable, high-insight artifacts from raw ideas or voice notes. Designed for long-term cognitive resilience, creative autonomy, and agentic orchestration.

> "Not to chase the world, but to map it. Not to keep up, but to keep _in_."

---

## 🔍 Purpose

This project serves as an evolving **AI-powered creative OS** — where you can:

- Converse with AI to clarify ideas
- Automatically generate structured insight capsules
- Render them as markdown logs and visual scrolls
- Preserve high-signal thinking as your own **Knowledge Atlas**

---

## ⚙️ Architecture

**Input → Agents → Output**

```text
[🗣️ Voice/Idea]
    ↓
[clarifier_agent] → [framer_agent] → [extractor_agent]
    ↓                    ↓                  ↓
[GPT core]         [capsule_writer]    [visual_mapper]
    ↓
[capsule_renderer → .md / .html]
    ↓
[index.md + logs]
```
