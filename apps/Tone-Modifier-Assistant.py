import os
from google import genai
from dotenv import load_dotenv
from google.genai import types
import gradio as gr

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

tone_types = {
    "Formal": (
        "You are a tone translator that rewrites text into a formal, professional register. "
        "Produce a concise formal version preserving meaning, proper grammar, and polite phrasing."
    ),
    "Casual": (
        "You are a tone translator that rewrites text into a casual, friendly register. "
        "Use conversational phrasing, contractions, and a relaxed tone while preserving meaning."
    )
}

def tone_translator(text,tone):
    system_prompt = tone_types[tone]
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config = types.GenerateContentConfig(
            system_instruction = system_prompt,
            temperature = 0.3,
            max_output_tokens = 2000),
        contents=text
    )
    return response.text 

# tone = "Formal"
# res = study_assistant("I want to enter the class,can I",tone)
# print(res)

demo = gr.Interface(
    fn=tone_translator,
    inputs=[
        gr.Textbox(
            lines=3,
            placeholder="Enter a sentence to rewrite...",
            label="Input Text"
        ),
        gr.Radio(
            choices=list(tones.keys()),
            value="Formal",
            label="Tone"
        )
    ],
    outputs=gr.Textbox(lines=5, label="Rewritten Text"),
    title="Tone Translator",
    description="Rewrite text in a Formal or Casual tone using Gemini."
)

demo.launch(debug=True)