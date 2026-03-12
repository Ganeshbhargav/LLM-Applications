# IMPORT NECESSARY LIBRARIES
import os
import json
import requests
import gradio as gr
from groq import Groq
from dotenv import load_dotenv

# LOAD ENV VARIABLES
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# CREATE GROQ CLIENT
client = Groq(api_key=GROQ_API_KEY)

# WEATHER FUNCTION (TOOL)
def get_weather(location):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    if data["cod"] == 200:
        return {
            "location": location,
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        }
    else:
        return {"error": "City not found"}

# TOOL DEFINITION
Tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name like Mumbai, London"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

# MAIN AI FUNCTION
def weather_agent(user_input):

    llm_messages = [
        {"role": "user", "content": user_input}
    ]

    # FIRST LLM CALL
    response = client.chat.completions.create(
        messages=llm_messages,
        model="llama-3.3-70b-versatile",
        tools=Tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message

    # CHECK IF TOOL IS CALLED
    if response_message.tool_calls:

        tool_call = response_message.tool_calls[0]

        arguments = json.loads(tool_call.function.arguments)
        location = arguments["location"]

        weather_data = get_weather(location)

        # ADD LLM MESSAGE
        llm_messages.append(response_message)

        # ADD TOOL RESPONSE
        llm_messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(weather_data)
        })

        # SECOND LLM CALL (FINAL ANSWER)
        final_response = client.chat.completions.create(
            messages=llm_messages,
            model="llama-3.3-70b-versatile"
        )

        return final_response.choices[0].message.content

    return "I could not fetch the weather."

# GRADIO UI
demo = gr.Interface(
    fn=weather_agent,
    inputs=gr.Textbox(placeholder="Ask something like: What is the weather in Hyderabad?"),
    outputs="text",
    title="🌤 AI Weather Assistant",
    description="Ask about the weather in any city"
)

# LAUNCH APP
demo.launch()