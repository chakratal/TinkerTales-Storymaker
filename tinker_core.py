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
    "Adventure": """Write in a fast-paced, daring voice, like Gordon Korman mixed with Indiana Jones for kids...""",
    "Bedtime": """Use a soft, soothing voice like Margaret Wise Brown meets Kate DiCamillo at her gentlest...""",
    "Comedy": """Write in the voice of a chaotic and funny narrator, like Roald Dahl mixed with Dav Pilkey...""",
    "Fairy Tale": """Write in a whimsical, old-timey voice, like Julia Donaldson meets a friendly storyteller from long ago...""",
    "Fantasy": """Write in a strange, curious voice, like early J.K. Rowling meets Lewis Carroll...""",
    "Mystery": """
    Write in a playful, clever voice like Lemony Snicket or Gordon Korman. Use dry humor, dramatic exaggeration, and occasional asides to the reader.

    The story must revolve around a real mystery (not a prank), with strange suspects and absurd clues that seem useless at first but make sense later.

    Avoid repeating the main character's name too much. Use pronouns, reactions, and inner thoughts to vary the sentence structure and keep things engaging.

    Side characters should be odd, dramatic, or over-the-top. Think: someone who talks only in rhyme, a librarian who refuses to whisper, or a pigeon with a vendetta. Let them feel chaotic, suspicious, or weird — never generic.

    Make sure the twist isn't a quiet confession. Aim for something funny, dramatic, or ridiculous. It should feel surprising but consistent with the clues dropped earlier.

    The narrator should have a voice — let them make snarky comments, express disbelief, or joke with the reader. The story should feel like a mash-up of Snicket's mystery absurdism and Korman's fast, funny pacing.

    Finish with a satisfying or hilarious resolution and a final wink to the reader.
    """,
    "Outer Space": """Write with giddy excitement, like a space-obsessed kid telling you about their alien best friend...""",
    "Science Fiction": """Write like a madcap inventor crossed with a sarcastic robot...""",
    "Spooky": """Write in a playful spooky voice, like a camp counselor telling a ghost story..."""
}

# === Age-based guidance ===
def get_age_style(age_range):
    style_by_age = {
        "3-5": "Use simple vocabulary, short sentences, and lots of repetition...",
        "6-8": "Add more excitement, faster pacing, and slightly more complex language...",
        "9-11": "Use clever dialogue, deeper themes, and more layered plots..."
    }
    return style_by_age.get(age_range, "")

# === Theme-based style lookup ===
def get_theme_style(theme):
    return style_by_theme.get(theme, "")

# === story generator ===
def generate_story(character_name, age_range, theme, custom_detail=None, story_prompt=None):
    theme_style = get_theme_style(theme)
    age_style = get_age_style(age_range)

    prompt = f"""
    Write an imaginative, age-appropriate story for a child aged {age_range}.

    The main character is named {character_name}, and the story should follow the theme: "{theme}".

    The story must follow this setup exactly: "{story_prompt}". This prompt defines the main conflict and cannot be changed or reversed.

    Do not reinterpret or ignore the prompt. Do not make the main character disappear if the prompt says they are solving a disappearance.

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
    - Around 500-550 words
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85,
        max_tokens=1000
    )

    story_text = response["choices"][0]["message"]["content"]
    return story_text.replace("Title:", "").strip()

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