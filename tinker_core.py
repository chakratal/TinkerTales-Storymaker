import openai
from elevenlabs import generate, set_api_key, VoiceSettings
from dotenv import load_dotenv
import os
from config import STYLE_BY_THEME, VOICE_IDS
from functools import lru_cache
from textwrap import dedent

@lru_cache(maxsize=None)
def select_voice(theme: str, age_range: str) -> str:
    key = f"{theme}-{age_range}" if theme == "Comedy" else theme
    return VOICE_IDS.get(key, VOICE_IDS["Bedtime"])

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
set_api_key(os.getenv("ELEVEN_API_KEY"))

def narrate_story(story_text, filename="story.mp3", voice_id="EXAVITQu4vr4xnSDxMaL"):
    print(f"🔊 Narrating with voice ID: {voice_id}")
    print(f"Story length: {len(story_text)} characters")
    audio = generate(
        text=story_text,
        voice=voice_id
    )
    with open(filename, "wb") as f:
        f.write(audio)
    print(f"🎧 Narration saved as {filename}")

def get_age_style(age_range):
    style_by_age = {
        "3-5": "Use simple vocabulary, short sentences, and lots of repetition...",
        "6-8": "Add more excitement, faster pacing, and slightly more complex language...",
        "9-11": "Use clever dialogue, deeper themes, and more layered plots..."
    }
    return style_by_age.get(age_range, "")

def generate_story(character_name, age_range, theme, custom_detail=None, story_prompt=None):
    theme_style = STYLE_BY_THEME.get(theme, "")
    age_style = get_age_style(age_range)

    prompt = dedent(f"""
    Write an imaginative, age-appropriate story for a child aged {age_range}.

    The main character is named {character_name}, and the story should follow the theme: "{theme}".

    {f"Include this detail: {custom_detail}" if custom_detail else ""}
    {f"The story prompt is: {story_prompt}" if story_prompt else ""}

    Style notes for the writer:
    {theme_style}

    Adjust your tone and structure to suit a child aged {age_range}:
    {age_style}

    Avoid narrator introductions — just dive into the story.

    The story should include:
    - A creative, fun title
    - A clear beginning, middle, and end
    - At least one surprising twist or unexpected character
    - Around 500-550 words
    """)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85,
        max_tokens=1000
    )

    story_text = response["choices"][0]["message"]["content"].strip()
    if story_text.endswith("The End.") or story_text.endswith("The End"):
        story_text = story_text.rsplit("The End", 1)[0].strip()
    cleaned_story = story_text.replace("Title:", "").strip()
    lines = cleaned_story.split("\n", 1)
    title = lines[0].strip()
    return title, cleaned_story

def generate_image(prompt):
    response = openai.Image.create(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024",
        response_format="url"
    )
    return response["data"][0]["url"]

def summarize_for_image(story_text):
    """
    Use the first 700 characters, trimmed to avoid splitting mid-sentence.
    """
    trimmed = story_text.strip().replace("\n", " ")
    return trimmed[:700].rsplit(".", 1)[0] + "."

def generate_image_from_story(name, theme, custom_detail=None, story_prompt=None):
    prompt_parts = [
        "Vibrant, imaginative children's book illustration. Focus only on visual storytelling.",
        f"Theme: {theme}.",
        f"Main character: {name}."
    ]
    if custom_detail:
        prompt_parts.append(f"Include: {custom_detail}.")
    if story_prompt:
        prompt_parts.append(f"Inspired by this scene: {story_prompt}.")

    prompt = " ".join(prompt_parts)
    return generate_image(prompt)