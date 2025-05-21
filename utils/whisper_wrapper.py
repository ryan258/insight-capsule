import whisper

model = whisper.load_model("base")  # Use "tiny" for faster, less accurate

def transcribe_audio(file_path):
    print(f"Transcribing: {file_path}")
    result = model.transcribe(file_path)
    return result["text"]
