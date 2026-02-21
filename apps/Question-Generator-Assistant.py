import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def question_generator(text):
    prompt = f"Generate questions from the following content:\n\n{text}"
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    # Extract the text
    questions_text = response.choices[0].message['content']
    return questions_text

content = "Large Language Models (LLMs) are AI systems trained on massive text data. They can understand, generate, and summarize human language."
questions = question_generator(content)
print(questions)