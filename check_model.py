import google.generativeai as genai
import os

# Configure with your API key
genai.configure(api_key="AIzaSyBz_WB6VdurZQGwfWSONlSYMr9w1FHX0f8")

# List all available models
print("Available Gemini models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"✅ {m.name}")