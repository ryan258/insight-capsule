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
import json # Added for JSON parsing of the brief

# === Config ===
AUDIO_FILE = "data/input_voice/latest.wav"
BRIEFS_DIR = "data/briefs/"
LOGS_DIR = "data/logs/"
INDEX_FILE = os.path.join(LOGS_DIR, "index.md") # Ensure this path is correct
SAMPLE_RATE = 44100 #
CHANNELS = 1 #

# === Initialize TTS Engine Globally ===
TTS_ENABLED = False # Default to False
tts_engine = None   # Initialize tts_engine to None
try:
    print("[TTS] Attempting to initialize TTS engine...")
    tts_engine = pyttsx3.init() #
    if tts_engine: # Check if initialization returned an engine
        tts_engine.setProperty("rate", 170) #
        TTS_ENABLED = True
        print("[TTS] Engine initialized successfully.")
    else:
        # This case might occur if pyttsx3.init() itself returns None (less common)
        print("[TTS Initialization Error] pyttsx3.init() returned None. TTS will be disabled.")
except Exception as e:
    print(f"[TTS Initialization Error] Could not initialize TTS: {e}. TTS will be disabled.")
    # TTS_ENABLED remains False, tts_engine remains None

# === TTS Speak ===
def speak(text): #
    global TTS_ENABLED # Moved to the top of the function
    
    if not TTS_ENABLED or not tts_engine:
        print(f"[TTS SKIPPED | Disabled or Init Error]: {text}")
        return
    try:
        print(f"[TTS Speaking]: {text}")
        tts_engine.say(text) #
        tts_engine.runAndWait() #
        print(f"[TTS Finished Speaking]")
    except RuntimeError as re_runtime: # Catch specific runtime errors from pyttsx3 if needed
        print(f"[TTS Runtime Error] During speak for text '{text}': {re_runtime}")
        print("[TTS] Disabling TTS for the rest of the session due to runtime error.")
        TTS_ENABLED = False # Now correctly modifies the global variable
    except Exception as e:
        print(f"[TTS Error] During speak for text '{text}': {e}")
        # Optionally, if any other exception should also disable TTS:
        # TTS_ENABLED = False

# === Record Audio Until Enter ===
def record_voice_to_file(): #
    q = queue.Queue() #

    def callback(indata, frames, time, status): #
        if status:
            # This can be verbose, but useful for serious debugging
            # print(f"[Audio Callback Status] {status}")
            pass # Keep it minimal unless debugging
        q.put(indata.copy()) #

    input("📣 Press [Enter] to start recording...") #
    print("🎙️ Recording... Press [Enter] again to stop.") #
    speak("Recording started.") # TTS feedback

    # Ensure the directory for the audio file exists before trying to write
    audio_dir = os.path.dirname(AUDIO_FILE)
    if audio_dir: # Check if AUDIO_FILE includes a directory path
        os.makedirs(audio_dir, exist_ok=True)

    try:
        with sf.SoundFile(AUDIO_FILE, mode='w', samplerate=SAMPLE_RATE, channels=CHANNELS) as file: #
            # sd.default.samplerate = SAMPLE_RATE # Explicitly set default if issues persist
            # sd.default.channels = CHANNELS
            with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback): #
                input() # Wait for Enter to stop recording
                print("🛑 Stopping recording...") #
                speak("Recording complete. Processing audio.") # TTS feedback
                
                # Drain the queue into the file
                while not q.empty(): #
                    file.write(q.get()) #
        print(f"🎤 Audio successfully saved to {AUDIO_FILE}")
    except Exception as e:
        print(f"🔴 [Audio Recording Error] Failed to record or save audio: {e}")
        speak("An error occurred during audio recording.") # TTS feedback for error
        # To prevent further processing on a failed/empty recording:
        if os.path.exists(AUDIO_FILE): # Delete potentially corrupt/empty file
             os.remove(AUDIO_FILE)
        return False # Indicate failure
    return True # Indicate success

# === Main Logic ===
def run_pipeline(): #
    if not record_voice_to_file(): # This now returns True/False
        print("🔴 Pipeline halted due to audio recording failure.")
        return # Stop if recording failed

    if not os.path.exists(AUDIO_FILE) or os.path.getsize(AUDIO_FILE) == 0:
        print(f"🔴 Audio file {AUDIO_FILE} not found or is empty. Skipping further processing.")
        speak("Audio file is missing or empty.")
        return

    print("\n🔍 Transcribing audio...") #
    speak("Transcribing audio.")
    transcript = transcribe_audio(AUDIO_FILE) #
    if not transcript.strip(): # Check if transcript is empty or just whitespace
        print("⚠️ Transcript is empty. The audio might have been silent or too short.")
        speak("Transcription resulted in empty text.")
        # Decide if to continue; for now, we will, but capsule will be based on empty text.
    else:
        print("📝 Transcript:\n" + transcript) #
        speak("Transcription complete.")

    print("\n📐 Generating creative brief...") #
    speak("Generating creative brief.")
    brief_raw = generate_brief_from_transcript(transcript if transcript.strip() else "User provided a silent or very short audio.") #
    print(brief_raw) # Print the raw brief (JSON-like string)
    
    title = "Untitled Insight" # Default title
    if brief_raw:
        try:
            brief_json = json.loads(brief_raw.strip())
            title = brief_json.get("title", "Untitled Insight").strip()
        except json.JSONDecodeError:
            print("[Warning] Creative brief was not valid JSON. Using regex for title.")
            match = re.search(r'"title":\s*"(.+?)"', brief_raw, re.IGNORECASE) #
            if match:
                title = match.group(1).strip() #
        except Exception as e:
            print(f"[Error] Could not extract title from brief: {e}")
    speak("Creative brief generated.")
    
    tags = [] #
    if transcript.strip(): # Only extract tags if transcript has content
        tags = re.findall(r"#(\w+)", transcript) #

    print("\n🧠 Generating insight capsule...") #
    speak("Generating insight capsule.")
    if not transcript.strip(): # Check if transcript is empty before sending to GPT
        print("🔴 Transcript is empty. Generating a placeholder insight capsule.")
        capsule = "Insight generation skipped as the audio transcript was empty."
    else:
        prompt = f"Turn the following idea into a concise, high-insight 400-word capsule:\n\n{transcript}" #
        capsule = ask_gpt(prompt, role="writing") #
    print("\n✅ Insight Capsule:\n" + capsule) #

    # --- Logging ---
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S") #
    os.makedirs(BRIEFS_DIR, exist_ok=True) #
    os.makedirs(LOGS_DIR, exist_ok=True) #

    safe_title_segment = re.sub(r'[^\w\s-]', '', title.lower())
    safe_title_segment = re.sub(r'[\s-]+', '-', safe_title_segment).strip('-_')
    if not safe_title_segment: safe_title_segment = "untitled"
    
    brief_filename = f"{timestamp}-{safe_title_segment}-brief.txt" 
    brief_path = os.path.join(BRIEFS_DIR, brief_filename) #
    with open(brief_path, "w", encoding="utf-8") as f: #
        f.write(brief_raw if brief_raw else "Brief generation failed or was empty.") #

    log_filename_base = f"{timestamp}-{safe_title_segment}" 
    log_filename = f"{log_filename_base}.md" #
    log_path = os.path.join(LOGS_DIR, log_filename) #

    with open(log_path, "w", encoding="utf-8") as f: #
        f.write(f"# Insight Capsule Log — {timestamp}\n") #
        f.write(f"**Title:** {title}\n") #
        f.write(f"**Tags:** {' '.join(['#' + tag for tag in tags]) if tags else 'None'}\n\n") #
        f.write(f"## Transcript\n```\n{transcript if transcript.strip() else 'Transcript was empty.'}\n```\n\n") #
        f.write(f"## Creative Brief\n```json\n{brief_raw if brief_raw else '{}'}\n```\n\n") #
        f.write(f"## Insight Capsule\n\n{capsule if capsule else 'Capsule generation failed or was empty.'}\n") #
    print(f"📝 Log saved to {log_path}")

    # --- Index Update ---
    index_entry_title = title 
    index_file_link = f"./{log_filename}"  #
    entry_tags_str = (' '.join(['#' + tag for tag in tags]) if tags else '').strip()
    entry = f"- [{index_entry_title}]({index_file_link}) — {timestamp} {entry_tags_str}\n" #
    
    # Ensure INDEX_FILE directory exists if it's nested
    index_dir = os.path.dirname(INDEX_FILE)
    if index_dir: # Check if INDEX_FILE includes a directory path
        os.makedirs(index_dir, exist_ok=True)
    
    header = "# Capsule Log Index\n\n" #
    try:
        if os.path.exists(INDEX_FILE): #
            with open(INDEX_FILE, "r+", encoding="utf-8") as idx_file: #
                existing_content = idx_file.read() #
                idx_file.seek(0, 0) # Go to the beginning
                # Prepend new entry after header, keep existing content
                if existing_content.startswith(header):
                    idx_file.write(header + entry + existing_content[len(header):]) #
                else: # If header is missing for some reason, add it
                    idx_file.write(header + entry + existing_content) #
                idx_file.truncate() # Remove any trailing old content if new content is shorter
        else:
            with open(INDEX_FILE, "w", encoding="utf-8") as idx: #
                idx.write(header + entry) #
        print(f"📚 Index updated at {INDEX_FILE}")
    except Exception as e:
        print(f"🔴 [Error] Failed to update index file {INDEX_FILE}: {e}")
        print(f"Attempting to append entry to {INDEX_FILE} as a fallback.")
        try: # Fallback append
            with open(INDEX_FILE, "a", encoding="utf-8") as idx_file_append:
                 if not os.path.getsize(INDEX_FILE) > 0: # If file was just created or empty
                     idx_file_append.write(header)
                 idx_file_append.write(entry)
        except Exception as e_append:
            print(f"🔴 [Error] Fallback append to index file also failed: {e_append}")


    print("\n🔊 Speaking final insight capsule...") #
    speak("Here is your insight capsule.") #
    if capsule and "Error:" not in capsule and "skipped as the audio transcript was empty" not in capsule:
        speak(capsule) #
    elif capsule:
        speak("There was an issue or the transcript was empty, so the capsule content reflects that.")
    else:
        speak("No insight capsule content was generated to speak.")
    
    print("\n🎉 Pipeline finished.")

if __name__ == "__main__":
    run_pipeline() #