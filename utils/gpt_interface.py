from dotenv import load_dotenv
import os
from openai import OpenAI
import logging
from datetime import datetime

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

logging.basicConfig(level=logging.INFO)

def ask_gpt(prompt, role="writing", temperature=0.7):
    model_map = {
        "writing": "gpt-4o-mini",
        "fact_check": "gpt-4o-mini",
        "expander": "gpt-4o-mini"
    }
    model = model_map.get(role, "gpt-4o-mini")

    try:
        logging.info(f"Calling GPT with model: {model} for role: {role}")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a precise, thoughtful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )

        content = response.choices[0].message.content.strip()

        # Timestamp + filename
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        filename = f"{timestamp}-{role}.md"
        log_path = os.path.join("data", "logs", filename)

        # Write log
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"# AI Capsule Log — {timestamp}\n")
            f.write(f"**Role:** {role}\n\n")
            f.write(f"**Model:** {model}\n\n")
            f.write(f"**Prompt:**\n```\n{prompt}\n```\n\n")
            f.write(f"**Response:**\n\n{content}\n")

        # Update index
        index_path = os.path.join("data", "logs", "index.md")
        entry = f"- [{timestamp} – {role}](./{filename})\n"

        if os.path.exists(index_path):
            with open(index_path, "r", encoding="utf-8") as idx:
                existing = idx.read()
            with open(index_path, "w", encoding="utf-8") as idx:
                idx.write(entry + existing)
        else:
            with open(index_path, "w", encoding="utf-8") as idx:
                idx.write(f"# Capsule Log Index\n\n{entry}")

        return content

    except Exception as e:
        logging.error(f"GPT call failed: {e}")
        return "⚠️ Error: Could not get a response from the language model."
