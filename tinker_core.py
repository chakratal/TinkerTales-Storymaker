import streamlit as st
from openai import OpenAI
from elevenlabs import generate, set_api_key, VoiceSettings
from dotenv import load_dotenv
import os

# Load environment and API keys
load_dotenv()  # optional, but safe to keep

# ElevenLabs from Streamlit secrets
set_api_key(st.secrets["ELEVEN_API_KEY"])

# ✅ THIS IS THE KEY LINE
openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def narrate_story(story_text, filename="story.mp3", voice="Amelia"):
    audio = generate(
        text=story_text,
        voice=voice,
        model="eleven_monolingual_v1",
        voice_settings=VoiceSettings(
            stability=0.7,
            similarity_boost=0.8
        )
    )
    with open(filename, "wb") as f:
        f.write(audio)
    print(f"🎧 Narration saved as {filename}")

def select_voice(theme, age_range):
    if theme == "Bedtime":
        return "Charlotte"
    elif theme == "Fairy Tale":
        return "Amelia"
    elif theme == "Spooky":
        return "Daniel"
    elif theme == "Comedy":
        if age_range == "6-8":
            return "Jessica"
        elif age_range == "9-11":
            return "Frederick Surrey"
        else:
            return "Amelia"
    elif theme == "Fantasy":
        return "Frederick Surrey"
    elif theme == "Adventure":
        return "Alice"
    elif theme == "Mystery":
        return "Adam Stone"
    elif theme == "Outer Space":
        return "Adam Stone"
    elif theme == "Science Fiction":
        return "Jessica"
    else:
        return "Amelia"

style_by_theme = {
    "Fairy Tale": "in a whimsical, magical style like J.K. Rowling",
    "Bedtime": "in a gentle, soothing voice like Margaret Wise Brown",
    "Outer Space": "in a blend of cosmic wonder and humor, like Carl Sagan meets Roald Dahl",
    "Science Fiction": "in a curious, thoughtful voice like Madeleine L'Engle",
    "Fantasy": "in a mythic, magical tone like C.S. Lewis",
    "Mystery": "in a clever, dramatic style like Lemony Snicket",
    "Spooky": "in a slightly eerie but fun tone like R.L. Stine"
}

comedy_style_by_age = {
    "3-5": "in a silly, rhythmic style like Sandra Boynton",
    "6-8": "in a wacky, outrageous style like Dav Pilkey (Dog Man)",
    "9-11": "in a clever, humorous tone like Roald Dahl"
}

adventure_style_by_age = {
    "3-5": "in a rhythmic, playful style like Julia Donaldson or Mo Willems",
    "6-8": "in a rhyming, action-packed style like Julia Donaldson",
    "9-11": "in a fast-paced, witty tone like Rick Riordan"
}

def generate_story(character_name, age_range, theme, custom_detail=None):
    age_sensitive_themes = ["Comedy", "Adventure"]

    if theme in age_sensitive_themes:
        if theme == "Comedy":
            style = comedy_style_by_age.get(age_range, "")
        elif theme == "Adventure":
            style = adventure_style_by_age.get(age_range, "")
    else:
        style = style_by_theme.get(theme, "")

    prompt = f"""
    Write a short story for a child aged {age_range}. The story should include a character named {character_name} and follow the theme "{theme}".
    {f"Include this detail: {custom_detail}." if custom_detail else ""}
    Write the story {style}.
    Include a creative, fun story title at the top.
    The story should have a clear beginning (introducing the character and setting), middle (a challenge or adventure), and end (a satisfying resolution).
    Make the story around 500-650 words long. Keep it age-appropriate and imaginative.
    """

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=1000
    )

    return response.choices[0].message.content