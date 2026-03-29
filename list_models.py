import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")

with open("models_list.txt", "w") as f:
    if not api_key:
        f.write("Error: GOOGLE_API_KEY not found.\n")
    else:
        genai.configure(api_key=api_key)
        f.write("Listing available models...\n")
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    f.write(f"Model Name: {m.name}\n")
        except Exception as e:
            f.write(f"Failed to list models: {e}\n")
