from typing import Dict, Any, Optional
from core.generation import GPTGenerator
from config.settings import MAX_CAPSULE_WORDS

class SynthesizerAgent:
    def __init__(self, generator: GPTGenerator):
        self.generator = generator
    
    def generate_capsule(self, 
                        transcript: str, 
                        brief: Optional[Dict[str, Any]] = None,
                        max_words: int = MAX_CAPSULE_WORDS) -> str:
        """Generate insight capsule from transcript and brief."""
        
        context = ""
        if brief:
            context = f"""
Context from creative brief:
- Title: {brief.get('title', 'Untitled')}
- Tone: {brief.get('desired_tone', 'analytical')}
- Themes: {', '.join(brief.get('core_themes', []))}

"""
        
        prompt = f"""{context}Turn the following idea into a concise, 
high-insight {max_words}-word capsule that captures the essence and 
deeper implications of the thought:

{transcript}"""
        
        return self.generator.generate(prompt, role="writing")
