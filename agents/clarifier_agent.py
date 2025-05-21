from utils.gpt_interface import ask_gpt

def generate_brief_from_transcript(transcript: str) -> str:
    prompt = f"""
You are an assistant helping to structure raw, spoken ideas into a usable creative brief.

Take the following transcript and return a JSON-style brief with the following fields:

- title: A punchy working title
- summary: One paragraph summarizing the intent
- core_themes: 3 to 5 key themes or angles
- desired_tone: e.g., analytical, poetic, skeptical, visionary
- format_type: e.g., insight capsule, short essay, illustrated scroll, simulated dialogue

Transcript:
\"\"\"
{transcript}
\"\"\"
"""
    response = ask_gpt(prompt, role="expander")
    return response
