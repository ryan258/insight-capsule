import os
import re
import queue
import sounddevice as sd
import soundfile as sf
from datetime import datetime
from utils.whisper_wrapper import transcribe_audio
from utils.gpt_interface import ask_gpt
from agents.clarifier_agent import generate_brief_from_transcript
import pyttsx3

# === Config ===
AUDIO_FILE = "data/input_voice/latest.wav"
BRIEFS_DIR = "data/briefs/"
LOGS_DIR = "data/logs/"
INDEX_FILE = os.path.join(LOGS_DIR, "index.md")
SAMPLE_RATE = 44100
CHANNELS = 1

# === TTS Speak ===
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 170)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[TTS Error] {e}")

# === Record Audio Until Enter ===
def record_voice_to_file():
    q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(status)
        q.put(indata.copy())

    input("📣 Press [Enter] to start recording...")
    print("🎙️ Recording... Press [Enter] again to stop.")
    speak("Recording started.")

    with sf.SoundFile(AUDIO_FILE, mode='w', samplerate=SAMPLE_RATE, channels=CHANNELS) as file:
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback):
            input()
            print("🛑 Stopping recording.")
            speak("Recording complete.")
            while not q.empty():
                file.write(q.get())

# === Main Logic ===
def run_pipeline():
    record_voice_to_file()

    print("\n🔍 Transcribing audio...")
    transcript = transcribe_audio(AUDIO_FILE)
    print("📝 Transcript:\n" + transcript)

    print("\n📐 Generating creative brief...")
    brief_raw = generate_brief_from_transcript(transcript)
    print(brief_raw)

    match = re.search(r'"title":\s*"(.+?)"', brief_raw)
    title = match.group(1).strip() if match else "Untitled"
    tags = re.findall(r"#(\w+)", transcript)

    print("\n🧠 Generating insight capsule...")
    prompt = f"Turn the following idea into a concise, high-insight 400-word capsule:\n\n{transcript}"
    capsule = ask_gpt(prompt, role="writing")
    print("\n✅ Insight Capsule:\n" + capsule)

    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    os.makedirs(BRIEFS_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)

    brief_path = os.path.join(BRIEFS_DIR, f"{timestamp}-brief.txt")
    with open(brief_path, "w", encoding="utf-8") as f:
        f.write(brief_raw)

    filename = f"{timestamp}-recording.md"
    log_path = os.path.join(LOGS_DIR, filename)

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"# Insight Capsule Log — {timestamp}\n")
        f.write(f"**Title:** {title}\n")
        f.write(f"**Tags:** {' '.join(['#' + tag for tag in tags]) if tags else 'None'}\n\n")
        f.write(f"## Transcript\n```\n{transcript}\n```\n\n")
        f.write(f"## Creative Brief\n```\n{brief_raw}\n```\n\n")
        f.write(f"## Insight Capsule\n\n{capsule}\n")

    entry = f"- [{title}](./{filename}) — {timestamp} {' '.join(['#' + tag for tag in tags])}\n"
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r", encoding="utf-8") as idx:
            existing = idx.read()
        with open(INDEX_FILE, "w", encoding="utf-8") as idx:
            idx.write(entry + existing)
    else:
        with open(INDEX_FILE, "w", encoding="utf-8") as idx:
            idx.write("# Capsule Log Index\n\n" + entry)

    print("\n🔊 Speaking final insight capsule...")
    speak("Here is your insight capsule.")
    speak(capsule)

if __name__ == "__main__":
    run_pipeline()
