import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def modify_tone(tone,text):
    prompt =  f"Rewrite the following text in a {tone} tone.Text:{text}"
    response = client.models.generate_content(
        model= "gemini-2.5-flash",
        contents = prompt
        )
    return response.text 

modify_tone_message = modify_tone("Formal","Knowledge is Power.")
print(modify_tone_message)