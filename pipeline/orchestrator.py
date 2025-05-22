from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import json

from core.audio import AudioRecorder
from core.transcription import Transcriber
from core.generation import GPTGenerator
from core.tts import TextToSpeech
from core.storage import StorageManager
from agents.clarifier import ClarifierAgent
from agents.synthesizer import SynthesizerAgent
from config.settings import AUDIO_DIR, AUDIO_FILENAME

class InsightPipeline:
    def __init__(self):
        self.audio_recorder = AudioRecorder()
        self.transcriber = Transcriber()
        self.generator = GPTGenerator()
        self.tts = TextToSpeech()
        self.storage = StorageManager()
        self.clarifier = ClarifierAgent(self.generator)
        self.synthesizer = SynthesizerAgent(self.generator)
        
    def run(self, audio_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Run the complete insight generation pipeline.
        
        Args:
            audio_path: Optional pre-recorded audio file
            
        Returns:
            Dict with results from each stage
        """
        results = {
            "success": False,
            "audio_path": None,
            "transcript": None,
            "brief": None,
            "capsule": None,
            "log_path": None,
            "error": None
        }
        
        try:
            # Step 1: Audio Recording (if needed)
            if audio_path is None:
                audio_path = AUDIO_DIR / AUDIO_FILENAME
                success = self.audio_recorder.record_to_file(
                    audio_path,
                    on_start=lambda: self.tts.speak("Recording started"),
                    on_stop=lambda: self.tts.speak("Recording complete. Processing audio.")
                )
                if not success:
                    raise Exception("Audio recording failed")
            
            results["audio_path"] = str(audio_path)
            
            # Step 2: Transcription
            self.tts.speak("Transcribing audio")
            transcript = self.transcriber.transcribe(audio_path)
            results["transcript"] = transcript
            
            if not transcript.strip():
                self.tts.speak("Transcript is empty")
                transcript = "User provided silent or very short audio."
            else:
                self.tts.speak("Transcription complete")
            
            # Step 3: Generate Brief
            self.tts.speak("Generating creative brief")
            brief = self.clarifier.generate_brief(transcript)
            results["brief"] = brief
            self.tts.speak("Creative brief generated")
            
            # Step 4: Generate Capsule
            self.tts.speak("Generating insight capsule")
            capsule = self.synthesizer.generate_capsule(transcript, brief)
            results["capsule"] = capsule
            
            # Step 5: Save Everything
            tags = self.storage.extract_tags_from_text(transcript)
            timestamp = datetime.now()
            
            # Save brief
            brief_json = json.dumps(brief, indent=2) if isinstance(brief, dict) else str(brief)
            self.storage.save_brief(brief, brief.get("title", "Untitled"), timestamp)
            
            # Save log
            log_path = self.storage.save_log(
                title=brief.get("title", "Untitled Insight"),
                transcript=transcript,
                brief=brief_json,
                capsule=capsule,
                tags=tags,
                timestamp=timestamp
            )
            results["log_path"] = str(log_path)
            
            # Step 6: Speak Result
            self.tts.speak("Here is your insight capsule")
            self.tts.speak(capsule)
            
            results["success"] = True
            print("\n🎉 Pipeline completed successfully!")
            
        except Exception as e:
            results["error"] = str(e)
            print(f"\n🔴 Pipeline error: {e}")
            self.tts.speak("An error occurred during processing")
        
        return results
