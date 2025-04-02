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

print(get_weather(47.8095,13.0550))