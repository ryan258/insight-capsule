import json
from typing import Dict, Any
from core.generation import GPTGenerator

class ClarifierAgent:
    def __init__(self, generator: GPTGenerator):
        self.generator = generator
    
    def generate_brief(self, transcript: str) -> Dict[str, Any]:
        """Generate structured creative brief from transcript."""
        prompt = f"""
You are an assistant helping to structure raw, spoken ideas into a usable creative brief.

Take the following transcript and return a JSON object with these fields:
- title: A punchy working title
- summary: One paragraph summarizing the intent
- core_themes: Array of 3-5 key themes or angles
- desired_tone: e.g., analytical, poetic, skeptical, visionary
- format_type: e.g., insight capsule, short essay, illustrated scroll

Return ONLY valid JSON, no additional text.

Transcript:
\"\"\"{transcript}\"\"\"
"""
        
        response = self.generator.generate(prompt, role="expander")
        
        # Parse JSON with fallback
        try:
            return json.loads(response.strip())
        except json.JSONDecodeError:
            # Fallback: extract what we can
            import re
            title_match = re.search(r'"title":\s*"(.+?)"', response)
            title = title_match.group(1) if title_match else "Untitled Insight"
            
            return {
                "title": title,
                "summary": "Brief parsing failed",
                "core_themes": [],
                "desired_tone": "analytical",
                "format_type": "insight capsule",
                "_raw": response
            }
