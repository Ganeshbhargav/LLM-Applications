import os
import gradio as gr
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

question_types = {
    "MCQs": """
                Rules:
                - Generate multiple-choice questions.
                - Each question must test conceptual understanding, not just direct copying.
                - Each question must have exactly 4 options labeled A, B, C, and D.
                - Only one option should be correct.
                - Avoid ambiguous wording.
                - After all questions, provide a separate section titled 'Answer Key' listing correct answers like:
                1. B
                2. A
                3. D
                Keep formatting clean and consistent.""",

    "Short Answer": """
                    Rules:
                    - Generate short-answer questions.
                    - Questions should require 2–4 sentence answers.
                    - Focus on key concepts, definitions, and explanations.
                    - Avoid yes/no questions.
                    - Do not provide the answers.
                    - Ensure clarity and academic tone.
                    - Keep numbering consistent.""",

    "Interview": """
                    Rules:
                    - Generate interview-style questions.
                    - Questions should assess deep understanding and practical knowledge.
                    - Include scenario-based or application-based questions.
                    - Questions should be suitable for a technical interview.
                    - Avoid overly theoretical or textbook-style phrasing.
                    - Do not provide answers.
                    - Keep formatting clean and professional."""
}

difficulty_rules = {
    "Easy": "Questions should test basic definitions and direct concepts.",
    "Medium": "Questions should test understanding and application of concepts.",
    "Hard": "Questions should test deep analysis, critical thinking, and real-world application."
}

def question_generator(content, q_type,num_questions,difficulty):
    base_rules = question_types[q_type]
    difficulty_instructions = difficulty_rules[difficulty]
    system_prompt = f"""
                        You are an expert academic question paper setter.

                        Generate exactly {num_questions} {difficulty}-level {q_type} questions 
                        based strictly on the provided content.

                        IMPORTANT OUTPUT RULES:
                        - Do NOT write any introduction sentence.
                        - Do NOT write any explanation before the questions.
                        - Start directly from Question 1.
                        - Do NOT include phrases like "Here are the questions".
                        - Output only the questions and required sections.
                        - Follow formatting strictly.

                        {difficulty_instructions}

                        {base_rules}
                        """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.4,
           max_output_tokens = max(1200, num_questions * 250)
        ),
        contents=content
    )
    return response.text


demo = gr.Interface(
    fn=question_generator,
    inputs=[
        gr.Textbox(
            lines=6,
            placeholder="Paste study material or content here...",
            label="Input Content"
        ),
        gr.Radio(
            choices=list(question_types.keys()),
            value="MCQs",
            label="Question Type"
        ),
        gr.Slider(1,10,value=5, label="Number of Questions"),
        gr.Radio(
                choices=["Easy", "Medium", "Hard"],
                value="Medium",
                label="Difficulty Level",
                info="Select the difficulty level of the questions"
        )
    ],
    outputs=gr.Textbox(lines=12, label="Generated Questions"),
    title="Question Generator",
    description="Generate MCQs, short-answer, or interview-style questions from given content using Gemini."
)

demo.launch(debug=True)