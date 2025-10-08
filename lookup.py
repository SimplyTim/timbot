from google.genai import types

#from key import SYSTEM_INSTRUCTIONS

# For Railway deployment
import os
SYSTEM_INSTRUCTIONS = os.environ['SYSTEM_INSTRUCTIONS']

def getAnswers(phrase, client):
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        config=types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTIONS),
        contents=phrase
    )
    print(response.text)
    return response.text