import openai
from elevenlabs import generate, set_api_key, VoiceSettings
from dotenv import load_dotenv
import os

# Load .env locally or rely on Streamlit secrets in the app
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

def select_voice(theme, age_range):
    if theme == "Bedtime":
        return "EXAVITQu4vr4xnSDxMaL"
    elif theme == "Fairy Tale":
        return "ZF6FPAbjXT4488VcRRnw"
    elif theme == "Spooky":
        return "onwK4e9ZLuTAKqWW03F9"
    elif theme == "Comedy":
        if age_range == "3-5":
            return "pFZP5JQG7iQjIQuC4Bku"
        elif age_range == "6-8":
            return "cgSgspJ2msm6clMCkdW9"
        elif age_range == "9-11":
            return "j9jfwdrw7BRfcR43Qohk"
    elif theme == "Fantasy":
        return "j9jfwdrw7BRfcR43Qohk"
    elif theme == "Adventure":
        return "9BWtsMINqrJLrRacOk9x"
    elif theme == "Mystery":
        return "NFG5qt843uXKj4pFvR7C"
    elif theme == "Outer Space":
        return "XrExE9yKIg1WjnnlVkGX"
    elif theme == "Science Fiction":
        return "IKne3meq5aSn9XLyUdCD"
    else:
        return "EXAVITQu4vr4xnSDxMaL"

style_by_theme = {
    "Comedy": "Make it funny, surprising, and absurd. Use outrageous situations, silly logic, wordplay, and visual gags. Include energetic pacing and unexpected turns. Think Dav Pilkey, Sandra Boynton, or Roald Dahl — chaotic, goofy, or dry, depending on age.",
    "Spooky": "Make it spooky-but-fun with mild suspense and strange but safe surprises. Use eerie settings, playful dread, and friendly monsters. Channel R.L. Stine for older kids and Scooby-Doo or silly ghost stories for younger ones.",
    "Fairy Tale": "Use whimsical language, magical settings, and talking creatures. Include a gentle moral, silly spells, and classic storybook structure. Think Julia Donaldson, Robert Munsch, or Gail Carson Levine.",
    "Fantasy": "Create imaginative worlds with odd magical rules and quirky characters. Balance wonder and humor, and include enchanted objects or unusual quests. Think C.S. Lewis, early J.K. Rowling, or Shannon Messenger.",
    "Mystery": "Make it puzzling and quirky with clever clues, red herrings, and weird logic. Include secret passages, strange suspects, and a satisfying twist. Think Lemony Snicket, The Mysterious Benedict Society, or a comedic Sherlock Holmes.",
    "Science Fiction": "Make it inventive, clever, and slightly absurd. Use futuristic gadgets, malfunctioning tech, and offbeat science logic. Think Phineas and Ferb meets Cory Doctorow or a junior version of Hitchhiker's Guide to the Galaxy.",
    "Outer Space": "Make it vibrant, silly, and full of space weirdness — talking aliens, gravity jokes, space pets. Keep the tone upbeat, adventurous, and zany, like a middle-grade Guardians of the Galaxy meets Sandra Boynton in zero gravity.",
    "Adventure": "Use fast pacing, physical action, and imaginative obstacles. Include treasure maps, wild villains, and big payoffs. Think Magic Tree House, Percy Jackson, or Gordon Korman — lighthearted and bold.",
    "Bedtime": "Use gentle rhythm, soft sensory language, and calming repetition. Keep the tone poetic, dreamy, and peaceful. Think Margaret Wise Brown, Owl Moon, or Kate DiCamillo's quietest moments — perfect for winding down."
}

def generate_story(character_name, age_range, theme, custom_detail=None):
    style = style_by_theme.get(theme, "")

    prompt = f"""
Write an imaginative, age-appropriate story for a child aged {age_range}.
The main character is named {character_name}, and the story should follow the theme: "{theme}".
{f"Include this detail: {custom_detail}" if custom_detail else ""}
{style}
Avoid narrator introductions — just dive into the story.

The story should include:
- A creative, fun title
- A clear beginning, middle, and end
- Around 500-650 words
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85,
        max_tokens=1000
    )
    return response["choices"][0]["message"]["content"]

def generate_image(prompt):
    response = openai.Image.create(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024",
        response_format="url"
    )
    return response["data"][0]["url"]