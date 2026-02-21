import os
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize client
client = genai.Client(api_key = GEMINI_API_KEY)


def study_assistant(user_prompt):
  # Send request to Gemini model
  response = client.models.generate_content(
      model = "gemini-2.5-flash",
      contents = user_prompt
       )
   # Return only the generated text output
  return response.text


# Call the function with a sample prompt
output = study_assistant("Explain GenAi")

# Print the model's response
print(output)