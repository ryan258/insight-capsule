# agents/synthesizer.py
from typing import Dict, Any, Optional
# Ensure GPTGenerator is imported from the correct location if it's used by HybridGenerator
from core.generation import GPTGenerator 
from core.local_generation import HybridGenerator # Assuming HybridGenerator is the primary one now
from config.settings import MAX_CAPSULE_WORDS

class SynthesizerAgent:
    def __init__(self, generator: HybridGenerator): # Changed to HybridGenerator
        self.generator = generator
    
    def generate_capsule(self, 
                        transcript: str, 
                        max_words: int = MAX_CAPSULE_WORDS) -> str:
        """Generate insight capsule directly from transcript."""
        
        # Simplified prompt, no longer relies on a separate brief
        prompt = f"""Turn the following idea or transcript into a concise, 
high-insight capsule of approximately {max_words} words. 
The capsule should capture the essence and deeper implications of the thought.
Avoid conversational openings or closings; focus on delivering the core insight directly.

Transcript:
\"\"\"
{transcript}
\"\"\"

Insight Capsule:"""
        
        # Assuming 'writing' is a valid role for your generator
        return self.generator.generate(prompt, role="writing")