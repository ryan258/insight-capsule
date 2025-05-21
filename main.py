import os
from utils.whisper_wrapper import transcribe_audio
from utils.gpt_interface import ask_gpt

if __name__ == "__main__":
    # === 1. Load audio ===
    audio_path = "data/input_voice/test-idea.wav"
    
    if not os.path.exists(audio_path):
        print(f"⚠️ Audio file not found: {audio_path}")
        exit()

    # === 2. Transcribe with Whisper ===
    transcript = transcribe_audio(audio_path)
    print("🎧 TRANSCRIPT:")
    print(transcript)

    # === 3. Create prompt for GPT ===
    prompt = f"Turn the following idea into a concise, high-insight 400-word capsule:\n\n{transcript}"

    # === 4. Send to GPT and get capsule ===
    result = ask_gpt(prompt, role="writing")

    # === 5. Output result to terminal ===
    print("\n🧠 INSIGHT CAPSULE:\n")
    print(result)
