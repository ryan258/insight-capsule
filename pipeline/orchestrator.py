# pipeline/orchestrator.py
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
# import json # No longer needed for brief_json here

from core.audio import AudioRecorder
from core.transcription import Transcriber
from core.tts import TextToSpeech
from core.storage import StorageManager
# from agents.clarifier import ClarifierAgent # ClarifierAgent is no longer used
from agents.synthesizer import SynthesizerAgent
from config.settings import AUDIO_DIR, AUDIO_FILENAME

from core.local_generation import HybridGenerator

class InsightPipeline:
    def __init__(self, use_local: bool = True): # use_local can still determine HybridGenerator preference
        self.audio_recorder = AudioRecorder()
        self.transcriber = Transcriber()
        
        self.generator = HybridGenerator(prefer_local=use_local)
        
        self.tts = TextToSpeech()
        self.storage = StorageManager()
        # self.clarifier = ClarifierAgent(self.generator) # Removed
        self.synthesizer = SynthesizerAgent(self.generator) # Synthesizer uses the same generator
        
    def _generate_simple_title(self, text: str, max_length: int = 5) -> str:
        """Generates a simple title from the first few words of a text."""
        if not text.strip():
            return "Untitled Insight"
        words = text.split()
        title = " ".join(words[:max_length])
        if len(words) > max_length:
            title += "..."
        return title

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
            # "brief": None, # Brief removed
            "title": "Untitled Insight", # Added title to results
            "capsule": None,
            "log_path": None,
            "error": None
        }
        
        try:
            # Step 1: Audio Recording (if needed)
            if audio_path is None:
                audio_path = AUDIO_DIR / AUDIO_FILENAME
                success_recording = self.audio_recorder.record_to_file(
                    audio_path,
                    on_start=lambda: self.tts.speak("Recording started"),
                    on_stop=lambda: self.tts.speak("Recording complete. Processing audio.")
                )
                if not success_recording: # Check the return value
                    raise Exception("Audio recording failed or was cancelled")
            
            results["audio_path"] = str(audio_path)
            
            # Step 2: Transcription
            self.tts.speak("Transcribing audio")
            transcript = self.transcriber.transcribe(audio_path)
            results["transcript"] = transcript
            
            processed_transcript = transcript # Keep original for results
            if not transcript.strip():
                self.tts.speak("Transcript is empty")
                # Provide a placeholder if you want to continue processing
                # or raise an error to stop.
                processed_transcript = "User provided silent or very short audio." 
            else:
                self.tts.speak("Transcription complete")
            
            # Step 3: Generate Capsule (directly from transcript)
            # Brief generation step is removed
            # self.tts.speak("Generating creative brief locally") # Removed
            # brief = self.clarifier.generate_brief(processed_transcript) # Removed
            # results["brief"] = brief # Removed
            # self.tts.speak("Creative brief generated") # Removed
            
            # Generate a simple title from the transcript for logging purposes
            # This can be refined later.
            log_title = self._generate_simple_title(transcript)
            results["title"] = log_title

            self.tts.speak("Generating insight capsule")
            capsule = self.synthesizer.generate_capsule(processed_transcript) # No brief passed
            results["capsule"] = capsule
            self.tts.speak("Insight capsule generated") # Added feedback
            
            # Step 4: Save Everything
            tags = self.storage.extract_tags_from_text(transcript)
            timestamp = datetime.now()
            
            # Save brief step removed
            # brief_json = json.dumps(brief, indent=2) if isinstance(brief, dict) else str(brief) # Removed
            # self.storage.save_brief(brief, brief.get("title", "Untitled"), timestamp) # Removed
            
            # Save log
            log_path = self.storage.save_log(
                title=log_title, # Use the generated title
                transcript=transcript,
                # brief=None, # Pass None or an empty string for the brief parameter
                capsule=capsule,
                tags=tags,
                timestamp=timestamp
            )
            results["log_path"] = str(log_path)
            
            # Step 5: Speak Result
            self.tts.speak("Here is your insight capsule")
            if capsule and "error" not in capsule.lower() and "skipped" not in capsule.lower():
                 self.tts.speak(capsule)
            elif not capsule:
                 self.tts.speak("The insight capsule is empty.")
            else:
                 self.tts.speak("The insight capsule contains an error or was based on empty input.")

            results["success"] = True
            print("\n🎉 Pipeline completed successfully!")
            
        except Exception as e:
            results["error"] = str(e)
            print(f"\n🔴 Pipeline error: {e}")
            self.tts.speak("An error occurred during processing")
        
        return results