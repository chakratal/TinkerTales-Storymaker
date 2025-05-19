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

import random

content_by_theme_and_age = {
    "Comedy": {
        "3-5": [
            "Use silly words and animal sounds.",
            "Include a dancing pickle.",
            "Add funny repetition.",
            "Mention a giggling chicken.",
            "A talking banana gets lost at the zoo."
        ],
        "6-8": [
            "Add fart jokes.",
            "Include banana peels.",
            "Talking animals everywhere.",
            "Zany surprises around every corner.",
            "Throw in a runaway toilet.",
            "Think Dav Pilkey-style chaos."
        ],
        "9-11": [
            "Use witty wordplay and absurd situations.",
            "Add a twist ending.",
            "Include a llama detective.",
            "Maybe some invisible spaghetti.",
            "A sarcastic robot joins the team."
        ]
    },

    "Spooky": {
        "3-5": [
            "Include silly ghosts with squeaky shoes.",
            "Use funny spooky sounds like 'booo-ooing!' and 'creakity creak'.",
            "Add a haunted sandwich that keeps vanishing.",
            "A skeleton keeps forgetting where he left his bones."
        ],
        "6-8": [
            "Add flickering lights and mysterious howls.",
            "Include a ghost who just wants to dance.",
            "A shadowy figure turns out to be a giant cat in a hat.",
            "Make it fun-scary with a magical twist."
        ],
        "9-11": [
            "Start with eerie clues that lead to a silly surprise.",
            "Include an abandoned library with books that whisper.",
            "Add an owl who knows everyone's secrets.",
            "Keep it creepy, but end on a funny or friendly note."
        ]
    },

    "Mystery": {
        "3-5": [
            "Include a missing sock that leads to an adventure.",
            "Add a detective cat with a monocle.",
            "Use rhyming clues and silly disguises.",
            "The mystery turns out to be about a surprise party."
        ],
        "6-8": [
            "Include clues hidden in snacks or drawings.",
            "Add red herrings like suspicious parrots.",
            "The solution is something unexpected but fun.",
            "Teamwork helps solve the case."
        ],
        "9-11": [
            "Begin with a puzzling event like vanishing shoes.",
            "Add plot twists and red herrings.",
            "A sidekick keeps solving things by accident.",
            "End with a clever reveal and satisfied 'aha!' moment."
        ]
    },

    "Bedtime": {
        "3-5": [
            "Include stars that sing lullabies.",
            "Add cozy animals like a snoring panda.",
            "The adventure winds down into a nap.",
            "End with a soft 'goodnight' from the moon."
        ],
        "6-8": [
            "Include flying beds or dreamy clouds.",
            "A moonbeam guides the character home to bed.",
            "Use soft, sleepy words like 'drift', 'float', and 'whisper'.",
            "End with a warm blanket and a cuddle."
        ],
        "9-11": [
            "The story should have gentle magic or wonder.",
            "Include stargazing, quiet music, or friendly dreams.",
            "End with peaceful thoughts and closing eyes.",
            "Keep the tone reflective and slow-paced."
        ]
    },

    "Fantasy": {
        "3-5": [
            "Include dragons that sneeze bubbles.",
            "Use magical pets like a unicorn puppy.",
            "Add talking trees that tell jokes.",
            "A rainbow slide leads to a treasure cave."
        ],
        "6-8": [
            "Include enchanted forests or spellbooks.",
            "A brave child solves a riddle from a talking frog.",
            "Magic misfires cause silly chaos.",
            "The villain turns out to be misunderstood."
        ],
        "9-11": [
            "Add ancient maps, secret portals, and wise mentors.",
            "Include magical battles or potion mix-ups.",
            "A prophecy is revealed—but hilariously wrong.",
            "Make the journey exciting, but character-driven."
        ]
    },

    "Adventure": {
        "3-5": [
            "Include bouncy bridges and slippery vines.",
            "Add treasure maps drawn in crayon.",
            "A friendly lion helps along the way.",
            "There’s a snack break before the final challenge."
        ],
        "6-8": [
            "Include booby traps, volcanoes, and ancient keys.",
            "A best friend joins for a wild jungle run.",
            "Add silly dangers like marshmallow quicksand.",
            "The villain is more goofy than scary."
        ],
        "9-11": [
            "Add daring escapes and clever thinking.",
            "Include riddles, mazes, and countdowns.",
            "Unexpected helpers arrive just in time.",
            "End with a funny twist or new quest hook."
        ]
    },

    "Outer Space": {
        "3-5": [
            "Include friendly aliens with three eyes and silly names.",
            "Planets made of cheese or ice cream.",
            "Add rocket ships that say 'zoom-zap!'",
            "The moon gives bedtime advice."
        ],
        "6-8": [
            "Add space pirates who dance instead of fight.",
            "Include a space disco on a rainbow asteroid.",
            "A robot keeps losing its bolts mid-sentence.",
            "End with a silly discovery like 'Planet Bubblegum'."
        ],
        "9-11": [
            "Include a malfunctioning ship and a talking AI.",
            "Aliens challenge Earth kids to a prank war.",
            "Add strange but helpful alien tech.",
            "Keep it adventurous but a little goofy."
        ]
    },

    "Science Fiction": {
        "3-5": [
            "Include robots who love to sing.",
            "Use funny sounds like 'bleep!' and 'buzz-bonk!'.",
            "Add a teleporting bunny that hiccups.",
            "The main gadget is powered by tickles."
        ],
        "6-8": [
            "Include hoverboards, shrinking lasers, or bubble shields.",
            "A robot tries to learn how to tell jokes.",
            "Add a science fair gone hilariously wrong.",
            "AI pets cause unexpected chaos."
        ],
        "9-11": [
            "Include time travel with pizza-themed paradoxes.",
            "A helpful AI turns out to be a trickster.",
            "Add malfunctioning lab experiments.",
            "Make it curious and futuristic, with comic relief."
        ]
    }
}

def generate_story(character_name, age_range, theme, custom_detail=None):
    if theme == "Comedy":
        style = comedy_style_by_age.get(age_range, "")
    elif theme == "Adventure":
        style = adventure_style_by_age.get(age_range, "")
    else:
        style = style_by_theme.get(theme, "")

    content_options = content_by_theme_and_age.get(theme, {}).get(age_range, "")
    if isinstance(content_options, list):
        content = " ".join(random.sample(content_options, min(3, len(content_options))))
    else:
        content = content_options

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