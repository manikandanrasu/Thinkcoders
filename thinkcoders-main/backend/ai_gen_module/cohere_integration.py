import os
import cohere
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

COHERE_TOKEN = os.getenv('COHERE_API_KEY')

co = cohere.Client(COHERE_TOKEN)

def generate_q(topic):
    prompt = f"""Generate a multiple choice questoin on the topic "{topic}".
    Format like:
    Question: ....
    Options:
    A) ....
    B) ....
    C) ....
    D) ....
    Answer: ....
"""
    response = co.generate(
    model='command',
    prompt=prompt,
    max_tokens=100,
    temperature=0.7
    )

    result = response.generations[0].text.strip()

    if not result:
        logger.error("Empty response received from cohera while generating question.")


    # Parse the generated text
    lines = result.split('\n')

    question = lines[0].replace("Question:", "").strip()

    options = {
        "A": lines[2].replace("A)", "").strip(),

        "B": lines[3].replace("B)", "").strip(),

        "C": lines[4].replace("C)", "").strip(),

        "D": lines[5].replace("D)", "").strip()
    }

    answer = lines[6].replace("Answer:", "").strip()

    return question, options, answer