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

# === Theme-based styles ===
style_by_theme = {
    "Adventure": """Write in a fast-paced, daring voice, like Gordon Korman mixed with Indiana Jones for kids. Make the action big and bold — crashing waves, ancient ruins, jungle vines, and surprise lava. The main character should be brave (or accidentally heroic), with wild obstacles, clever escapes, and a satisfying payoff. Let the narrator egg them on like an excited sports commentator.""",

    "Bedtime": """Use a soft, soothing voice like Margaret Wise Brown meets Kate DiCamillo at her gentlest. Let the story drift like a lullaby — calm, dreamy, and filled with cozy imagery. Use rhythmic language, tender repetition, and gentle surprises (a moonbeam cat, a whispering wind). Keep everything safe and magical, perfect for winding down.""",

    "Comedy": """Write in the voice of a chaotic and funny narrator, like Roald Dahl mixed with Dav Pilkey. Use ridiculous metaphors, absurd logic, and over-the-top characters (e.g. a llama wearing underpants). Fill the story with recurring gags, surprising twists, and visual silliness. Make it feel like the narrator can barely keep up with how bonkers the story gets. Focus on joy, momentum, and pure ridiculous fun.""",

    "Fairy Tale": """Write in a whimsical, old-timey voice, like Julia Donaldson meets a friendly storyteller from long ago. Use poetic language, magical settings, and talking animals with big personalities. Include a silly spell or a gentle moral. Make the narrator feel like they’re telling this tale for the hundredth time — full of charm, rhythm, and wonder.""",

    "Fantasy": """Write in a strange, curious voice, like early J.K. Rowling meets Lewis Carroll. Let the magical world have bizarre rules (e.g. talking carrots, invisible staircases, whispering puddles). The narrator should be amused and slightly confused by the world, but excited to explore it. Fill the story with unexpected characters, imaginative landscapes, and logic that only kind of makes sense.""",

    "Mystery": """Use a sly, clever narrator voice like Lemony Snicket with a magnifying glass. Let the narrator drop hints, throw in fake clues, and act like they know more than they’re telling. Make the mystery just barely solvable, with odd characters and suspicious details. Build tension with humor and finish with a twist that makes kids gasp and laugh at once.""",

    "Outer Space": """Write with giddy excitement, like a space-obsessed kid telling you about their alien best friend. Use big, colorful imagery: zero-gravity cereal, giggling space goats, malfunctioning moon boots. The narrator should sound wide-eyed and a little breathless, like they just got back from the rocket. Keep it upbeat, weird, and full of surprise tech and aliens with silly customs.""",

    "Science Fiction": """Write like a madcap inventor crossed with a sarcastic robot. Let the story be full of wild gadgets, ridiculous inventions, and techno-mayhem. The narrator should love science but not quite understand it — use fake jargon, zany logic, and plenty of ‘uh-oh’ moments with machines gone haywire. Think junior Hitchhiker’s Guide with a dash of Phineas and Ferb.""",

    "Spooky": """Write in a playful spooky voice, like a camp counselor telling a ghost story with a flashlight under their chin. Use creaky floors, misty woods, glowing eyes — but make it all fun-scary, not real-scary. Let the narrator spook and reassure at the same time: “But don’t worry, the ghost just wanted a snack.” Keep it mysterious, a little eerie, but safe and silly at the end."""
}

# === New: Age-based guidance ===
def get_age_style(age_range):
    style_by_age = {
        "3-5": "Use simple vocabulary, short sentences, and lots of repetition. Keep the plot linear and the conflict gentle. Use funny sounds, talking animals, and a cozy resolution.",
        "6-8": "Add more excitement, faster pacing, and slightly more complex language. Include jokes, wordplay, and a strong emotional core. Let the characters solve a problem or face a challenge.",
        "9-11": "Use clever dialogue, deeper themes, and more layered plots. Include witty narration, surprising twists, and a mix of humor and stakes. The story can be longer and slightly more sophisticated."
    }
    return style_by_age.get(age_range, "")

# === New: Theme-based style lookup ===
def get_theme_style(theme):
    return style_by_theme.get(theme, "")

# === Updated story generator ===
def generate_story(character_name, age_range, theme, custom_detail=None):
    theme_style = get_theme_style(theme)
    age_style = get_age_style(age_range)

    prompt = f"""
Write an imaginative, age-appropriate story for a child aged {age_range}.

The main character is named {character_name}, and the story should follow the theme: "{theme}".

{f"Include this detail: {custom_detail}" if custom_detail else ""}

Style notes for the writer:
{theme_style}

Adjust your tone and structure to suit a child aged {age_range}:
{age_style}

Avoid narrator introductions — just dive into the story.

The story should include:
- A creative, fun title
- A clear beginning, middle, and end
- At least one surprising twist or unexpected character
- Around 500–550 words
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85,
        max_tokens=1000
    )
    return response["choices"][0]["message"]["content"]

# === Image generator ===
def generate_image(prompt):
    response = openai.Image.create(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024",
        response_format="url"
    )
    return response["data"][0]["url"]