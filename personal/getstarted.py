import os

#Import the Openai Library
from openai import OpenAI

#Get the API Key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#Query für das KI Modell schreiben
query = "Who are you?"

#Die Rollen und Querys festlegen
message = [
    {"role": "system", "content": "You are a helpful AI Agent in my first Program."},
    {
        "role": "user",
        "content": query,
    }
]


completation = client.chat.completions.create(
    model="gpt-4o",
    messages=message
)

print(completation.choices[0].message.content)