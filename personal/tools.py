import os
import json

import requests
from openai import OpenAI
from pydantic import BaseModel, Field


"""
docs: https://platform.openai.com/docs/guides/function-calling
"""

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#Define the tool

def get_weather(latitude, longitude):
    #This is public API which returns the wheater for a given location
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    data = response.json()
    return data["current"]

# Step 1 Call the wheater tools

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current temperature for provided coordinates in celsius.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                },
                "required": ["latitude", "longitude"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]

system_prompt = "You are a helpful wheater assistant."

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What's the wheater in Salzburg today."},
]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)


# 2 Model dicides to call functions

completion.model_dump()


# 3 Execute get_wheater function

def call_function(name, args):
    if name == "get_weather":
        return get_weather(**args)
    
for tool_call in completion.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    messages.append(completion.choices[0].message)
    
    #Testen
    print(name)
    print(args)
    print(messages)


    result = call_function(name, args)
    messages.append(
        {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)}
    )



    # 4 Supply result and call model again

    class WeatherResponse(BaseModel):
        temperature: float = Field(
            description="The current temperatur in celsius for the given location"
        )
        response: str=Field(
            description="A natrual languange response to the user's question"
        )

completion_2 = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    response_format=WeatherResponse,
)

# 5 Check model response

final_response = completion_2.choices[0].message.parsed
print(final_response.temperature)
print(final_response.response)