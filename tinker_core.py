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
        voice=voice_id  # <- uses ID now
    )
    with open(filename, "wb") as f:
        f.write(audio)
    print(f"🎧 Narration saved as {filename}")

def select_voice(theme, age_range):
    if theme == "Bedtime":
        return "EXAVITQu4vr4xnSDxMaL"  # Sarah (formerly Rachel Legacy)
    elif theme == "Fairy Tale":
        return "ZF6FPAbjXT4488VcRRnw"  # Amelia
    elif theme == "Spooky":
        return "onwK4e9ZLuTAKqWW03F9"  # Daniel
    elif theme == "Comedy":
        if age_range == "3-5":
            return "pFZP5JQG7iQjIQuC4Bku"  # Lily
        elif age_range == "6-8":
            return "cgSgspJ2msm6clMCkdW9"  # Jessica
        elif age_range == "9-11":
            return "j9jfwdrw7BRfcR43Qohk"  # Frederick Surrey
    elif theme == "Fantasy":
        return "j9jfwdrw7BRfcR43Qohk"  # Frederick Surrey
    elif theme == "Adventure":
        return "9BWtsMINqrJLrRacOk9x"  # Aria
    elif theme == "Mystery":
        return "NFG5qt843uXKj4pFvR7C"  # Adam Stone - late night radio
    elif theme == "Outer Space":
        return "XrExE9yKIg1WjnnlVkGX"  # Matilda
    elif theme == "Science Fiction":
        return "IKne3meq5aSn9XLyUdCD"  # Charlie
    else:
        return "EXAVITQu4vr4xnSDxMaL"  # Sarah (default fallback)

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
    "6-8": "in a wacky, outrageous style like Dav Pilkey",
    "9-11": "in a clever, humorous tone like Roald Dahl"
}

adventure_style_by_age = {
    "3-5": "in a rhythmic, playful style like Julia Donaldson or Mo Willems",
    "6-8": "in a rhyming, action-packed style like Julia Donaldson",
    "9-11": "in a fast-paced, witty tone like Rick Riordan"
}

content_by_theme_and_age = {
    "Comedy": {
        "3-5": "Use silly words, animal sounds, and funny repetition. Include a dancing pickle or a giggling chicken.",
        "6-8": "Add fart jokes, banana peels, talking animals, and zany surprises. Think Dav Pilkey-style chaos.",
        "9-11": "Use witty wordplay, absurd situations, and a twist ending. Maybe a llama detective or invisible spaghetti."
    },
    "Spooky": {
        "3-5": "Include spooky sounds like 'creak' and 'whoosh', but keep it fun and not too scary. Think silly ghosts.",
        "6-8": "Add creaky floors, flickering lights, and a friendly monster. The scare should turn into something funny.",
        "9-11": "Make it suspenseful with eerie clues and an unexpected twist. Keep the ending fun and not too dark."
    },
    "Mystery": {
        "3-5": "Add a lost toy, silly detective tools, and a mystery solved by teamwork.",
        "6-8": "Include clues, red herrings, and a clever reveal. Think junior detective squad.",
        "9-11": "Make it clever and dramatic, with twists and a satisfying conclusion. The reader should feel like a sleuth."
    },
    "Bedtime": {
        "3-5": "Use soft, cozy language. Include stars, cuddly animals, and a peaceful ending.",
        "6-8": "Add gentle adventures that wind down to sleep, like flying beds or cloud races.",
        "9-11": "Keep it dreamy and imaginative, with quiet magic and a reflective, sleepy ending."
    },
    "Fairy Tale": {
        "3-5": "Include talking animals, silly spells, and a kind hero. A cupcake crown might be fun too.",
        "6-8": "Add enchanted forests, quirky villains, and a funny fairy godparent.",
        "9-11": "Make it rich with clever twists on classic tropes—maybe a dragon who wants to be a librarian."
    },
    "Outer Space": {
        "3-5": "Include aliens that giggle, colorful planets, and space snacks.",
        "6-8": "Add rocketships, talking robots, and a surprise space disco.",
        "9-11": "Make it adventurous and funny, with strange planets and smart alien friends."
    },
    "Science Fiction": {
        "3-5": "Add friendly robots and buttons that go ‘beep’ and ‘zap’.",
        "6-8": "Include cool gadgets, hoverboards, and kids who outsmart the machines.",
        "9-11": "Make it techy and thoughtful, with AI gone silly or time travel gone weird."
    },
    "Fantasy": {
        "3-5": "Include dragons that sneeze bubbles, and magical animals.",
        "6-8": "Add enchanted forests, magical riddles, and brave kids.",
        "9-11": "Make it epic and mysterious, with ancient maps and secret spells."
    },
    "Adventure": {
        "3-5": "Include bouncing bridges, treasure hunts, and animal guides.",
        "6-8": "Add volcanoes, traps, jungle paths, and daring escapes.",
        "9-11": "Make it exciting and funny, with quick decisions and thrilling obstacles."
    }
}

def generate_story(character_name, age_range, theme, custom_detail=None):
    if theme == "Comedy":
        style = comedy_style_by_age.get(age_range, "")
    elif theme == "Adventure":
        style = adventure_style_by_age.get(age_range, "")
    else:
        style = style_by_theme.get(theme, "")

    content = content_by_theme_and_age.get(theme, {}).get(age_range, "")

    prompt = f"""
    Write a short story for a child aged {age_range}. The story should include a character named {character_name} and follow the theme "{theme}".
    {f"Include this detail: {custom_detail}." if custom_detail else ""}
    {content}
    Write the story {style}.
    Include a creative, fun story title at the top.
    The story should have a clear beginning (introducing the character and setting), middle (a challenge or adventure), and end (a satisfying resolution).
    Make the story around 500-650 words long. Keep it age-appropriate and imaginative.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=1000
    )
    return response["choices"][0]["message"]["content"]

def generate_image(prompt):
    response = openai.Image.create(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024",  # DALL·E 3 only supports this size
        response_format="url"
    )
    return response["data"][0]["url"]