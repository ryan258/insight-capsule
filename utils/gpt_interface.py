from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_gpt(prompt, role="writing", temperature=0.7):
    model_map = {
        "writing": "gpt-4.1-mini-2025-04-14",
        "fact_check": "gpt-4o-mini",
        "expander": "gpt-4.1-mini-2025-04-14"
    }
    model = model_map.get(role, "gpt-4.1-mini-2025-04-14")
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a precise, thoughtful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )
    return response.choices[0].message.content.strip()
