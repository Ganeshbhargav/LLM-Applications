import os
from google import genai
from dotenv import load_dotenv

load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


def language_translator(text, target_language):
    prompt = f"Translate the following text to {target_language} : {text}"
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = prompt
        )
    return response.text

Output = language_translator("Welcome to the course, Building LLM Applications","Hindi")
print(Output)