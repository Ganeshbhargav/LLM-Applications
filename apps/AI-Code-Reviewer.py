import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import gradio as gr

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

review_types = {
    "Bug Detection": (
        "You are a senior software engineer and code reviewer. "
        "Review the given {language} code and focus ONLY on finding bugs, "
        "syntax errors, logical issues, and potential runtime problems. "
        "Explain each issue clearly in simple language and suggest fixes. "
        "Respond in plain text only. Do not use markdown, headings, asterisks, "
        "bullet symbols, or special formatting. Use simple sentences or numbered lists."
    ),

    "Code Quality": (
        "You are a professional code reviewer. "
        "Analyze the given {language} code for readability, naming conventions, "
        "maintainability, and best practices without changing the original logic. "
        "Suggest improvements clearly and politely. "
        "Respond in plain text only. Do not use markdown, headings, asterisks, "
        "bullet symbols, or special formatting. Use simple sentences or numbered lists."
    ),

    "Optimization": (
        "You are an experienced performance-focused software engineer. "
        "Review the given {language} code and suggest performance and scalability "
        "optimizations. Explain why each optimization helps. "
        "Respond in plain text only. Do not use markdown, headings, asterisks, "
        "bullet symbols, or special formatting. Use simple sentences or numbered lists."
    ),

    "Time & Space Complexity": (
        "You are a data structures and algorithms expert. "
        "Analyze the given {language} code and explain its time and space complexity "
        "step by step in simple language. "
        "Respond in plain text only. Do not use markdown, headings, asterisks, "
        "bullet symbols, or special formatting. Use simple sentences or numbered lists."
    )
}
def codeReviewer(code,language,review_type):
    system_prompt = review_types[review_type].format(language=language)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.4,
            max_output_tokens=2000),
        contents= code
        )
    return response.text

demo = gr.Interface(
    fn=codeReviewer,
    inputs=[
        gr.Textbox(
            lines=12,
            label="Code Input",
            placeholder="Paste your code here...\n\nExample:\nfor i in range(5):\n    print(i)",
        ),
        gr.Radio(
            choices=["Python","Java","JavaScript"],
            label="Programming Language",
            value = "Python"
        ),
        gr.Dropdown(
            choices=list(review_types.keys()),
            label="Review Type",
            value="Bug Detection"
        )

    ],
    outputs=gr.Textbox(lines=14,label="Code Review Report"),
    title="AI CODE REVIEWER",
    description="An AI-powered tool that reviews your code for bugs, best practices, optimizations, and time & space complexity. Supports Python, JavaScript, and Java."
)

demo.launch(debug=True)
