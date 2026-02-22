import os
from google import genai
from dotenv import load_dotenv
from google.genai import types

# Load environment variables
load_dotenv()

# Get API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize client
client = genai.Client(api_key = GEMINI_API_KEY)

# Dictionary storing different response personalities
personalities = {
  "Friendly": """You are a friendly, enthusiastic, and highly encouraging Study Assistant. 
                Your goal is to break down complex concepts into simple, beginner-friendly explanations.
                 Use analogies and real-world examples that beginners can relate to. Always ask a follow-up question to check understanding.""",
  "Academic": """You are a strictly academic, highly detailed, and professional university Professor. 
                Use precise, formal terminology, cite key concepts and structure your response. 
                Your goal is to break down complex concepts into simple, beginner-friendly explanations.
                Use analogies and real-world examples that beginners can relate to.
                Always ask a follow-up question to check understanding."""
}

def study_assistant(question,persona):
  # Get system instruction based on selected persona
  system_prompt = personalities[persona]

  # Send request to Gemini model with configuration settings
  response = client.models.generate_content(
      model = "gemini-2.5-flash",
      config = types.GenerateContentConfig(
          system_instruction = system_prompt, # Controls AI behavior
          temperature = 0.5, # Controls randomness (0 = deterministic, 1 = creative)
          max_output_tokens = 1000 # Limits response length
          ),
      contents = question
       )
  
  # Return only generated text output
  return response.text

# Example usage
personality = "Academic"
output = study_assistant("Explain GenAi",personality)

# Print model response
print(output)