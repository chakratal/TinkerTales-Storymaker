# config.py
import json
from pathlib import Path

# Voice IDs for each theme/age combo
VOICE_IDS = {
    "Adventure":          "9BWtsMINqrJLrRacOk9x",
    "Bedtime":            "EXAVITQu4vr4xnSDxMaL",
    "Comedy-3-5":         "pFZP5JQG7iQjIQuC4Bku",
    "Comedy-6-8":         "cgSgspJ2msm6clMCkdW9",
    "Comedy-9-11":        "j9jfwdrw7BRfcR43Qohk",
    "Fairy Tale":         "ZF6FPAbjXT4488VcRRnw",
    "Fantasy":            "j9jfwdrw7BRfcR43Qohk",
    "Mystery":            "NFG5qt843uXKj4pFvR7C",
    "Outer Space":        "XrExE9yKIg1WjnnlVkGX",
    "Science Fiction":    "IKne3meq5aSn9XLyUdCD",
    "Spooky":             "onwK4e9ZLuTAKqWW03F9",
}

# Theme → GPT style prompts
STYLE_BY_THEME = json.loads(
    Path("theme_styles.json").read_text()
)