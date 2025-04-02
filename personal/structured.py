import os

from openai import OpenAI
from pydantic import BaseModel

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 1 - Das Format der Antwort mit Pydantic definieren

class Car(BaseModel):
    brand: str
    colour: str
    price: int

# 2 - Das KI Modell aufrufen

# Query
query = "A Ferrari is red and costs 500000"

message = [
    {"role":"system", "content": "Extract the information about the car"},
    {
        "role": "user",
        "content": query
    }
]

completion = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=message,
    response_format=Car,
)


car1 = completion.choices[0].message.parsed
print(car1.brand)
print(car1.colour)
print(car1.price)