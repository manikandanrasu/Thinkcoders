import os
import requests
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load variables from .env
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_q(topic):
    prompt = f"""Generate one multiple-choice question on the topic "{topic}".
Return it in the following format:
Question: ...
Options:
A) ...
B) ...
C) ...
D) ...
Answer: ... (just the correct option letter like A, B, C, or D)
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()

        content = response.json()['choices'][0]['message']['content'].strip()

        if not content:
            logger.error("Empty response from OpenRouter (Cohere Command R+)")
            return None, None, None

        # Parse output (possible parsing bugs might occur here)
        lines = content.split("\n")
        question = next((line.replace("Question:", "").strip() for line in lines if line.startswith("Question:")), "")
        options = {}

        for line in lines:
            if line.strip().startswith("A)"):
                options["A"] = line.replace("A)", "").strip()
            elif line.strip().startswith("B)"):
                options["B"] = line.replace("B)", "").strip()
            elif line.strip().startswith("C)"):
                options["C"] = line.replace("C)", "").strip()
            elif line.strip().startswith("D)"):
                options["D"] = line.replace("D)", "").strip()

        answer_line = next((line for line in lines if line.startswith("Answer:")), "")
        answer = answer_line.replace("Answer:", "").strip()

        return question, options, answer

    except Exception as e:
        logger.error(f"Unexpected error during question generation: {e}")
        return None, None, None
