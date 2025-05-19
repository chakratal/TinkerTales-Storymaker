import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

try:
    response = openai.Image.create(
        model="dall-e-3",
        prompt="A friendly robot reading a bedtime story to kids, digital illustration",
        n=1,
        size="1024x1024"
    )
    print("✅ DALL·E 3 is available!")
    print("Image URL:", response["data"][0]["url"])
except Exception as e:
    print("❌ DALL·E 3 is NOT available.")
    print("Error:", e)