import os 

from openai import OpenAI
from pydantic import BaseModel,Field

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


query = "Also ich hab mir hald in die hose gepisst"
messages = [
    {"role": "system", "content": "Korrigiere den folgenden deutschen Text auf Rechtschreibung, Grammatik und Zeichensetzung. Falls nötig, vereinfache unnötig komplizierte Sätze, um die Lesbarkeit zu verbessern, aber verändere nicht den Inhalt oder Stil des Autors."},
    {"role": "user", "content": query}
]

class Correction(BaseModel):
    title: str = Field(
        description="Der Titel des Textes. (Darf niemals leer bleiben)"
    )
    correction: str = Field(
        description="Die vollständig korrigierte Version des Textes."
    )
    feedback: str = Field(
        description="Ein allgemeines persönliches Feedback zu den wichtigsten gemachten Fehlern und Verbesserungsvorschläge"
    )
    

completion = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=messages,
    response_format=Correction,
)

text = completion.choices[0].message.parsed
text.title
text.correction
text.feedback