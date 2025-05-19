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
            "Tell a silly story using animal sounds, repeating phrases, and unexpected rhymes. Think Sandra Boynton-style goofiness.",
            "Include a dancing pickle, a giggling chicken, and lots of 'boing!' and 'splat!' moments. Keep it short, loud, and playful.",
            "Make everything exaggerated and wobbly — a hat that sneezes, a frog that forgets how to hop. Think Sandra Boynton meets Dr. Seuss.",
            "Use a super simple plot, but fill it with silly characters, made-up words, and a joyful tone. Channel the joyful chaos of Boynton.",
            "Make the story musical and bouncy, like a song. Include clapping, stomping, or even burping cows. Inspired by Sandra Boynton's rhythmic style."
        ],
        "6-8": [
            "Create a wild story filled with banana peels, fart jokes, and talking animals. Think Dav Pilkey-style chaos!",
            "Include a mischievous animal sidekick, a ridiculous hat, and one totally unnecessary explosion. Channel Captain Underpants energy.",
            "Let the main character accidentally start a conga line at the zoo using a kazoo and spaghetti. Make it cartoon-level silly — Pilkey meets Looney Tunes.",
            "Make everything go wrong in the funniest way: banana peels, runaway toilets, and a giggling goat included. Inspired by Dog Man's energetic absurdity.",
            "Write the story like it's being told by a hyper kid with a wild imagination and zero filter. Think Pilkey with a sugar rush."
        ],
        "9-11": [
            "Use dry, witty humor with a touch of absurdity. Include clever wordplay and awkward situations. Think Roald Dahl or Lemony Snicket.",
            "Let the main character try to act serious while everything around them spirals into ridiculous chaos. Channel Dahl's Matilda energy.",
            "Include an over-the-top villain with an embarrassing weakness, a hero who just wants lunch, and at least one talking object. Inspired by Snicket's dramatic flair.",
            "Make the narrator part of the joke — someone who clearly doesn't believe this story should be happening. Use snarky commentary, like Snicket.",
            "Tell the story like it's a formal report… about something completely ridiculous, like a cheese rebellion or a llama election. Think a parody of bureaucratic seriousness, Dahl-style."
        ]
    },

    "Fantasy": {
        "3-5": [
            "Tell a magical story with friendly dragons, sparkly spells, and talking animals. Think Cressida Cowell meets Julia Donaldson.",
            "Include a rainbow waterfall, a crown made of cupcakes, or a unicorn who forgets how to fly. Channel Cowell and Donaldson's whimsy.",
            "Let the magic be simple and fun — no dark wizards, just giggly goblins and accidental enchantments. Inspired by Cowell's playful style.",
            "End with a magical friendship or a silly lesson learned through a wand mishap. Think Julia Donaldson with a fantasy twist."
        ],
        "6-8": [
            "Write a quest involving magical maps, enchanted forests, or riddle-speaking frogs. Think C.S. Lewis meets Mo Willems.",
            "Include a clumsy wizard-in-training or a kid who accidentally becomes royalty. Inspired by Lewis's sense of discovery.",
            "Make the magical world full of surprises — invisible pets, floating snacks, or spells that backfire. Channel Willems' chaotic energy.",
            "Keep the tone adventurous, light, and just a bit goofy. Like a blend of early Narnia and Elephant & Piggie mischief."
        ],
        "9-11": [
            "Write a rich, character-driven fantasy with a hint of mystery. Think early Harry Potter or Keeper of the Lost Cities.",
            "Include magical objects with odd rules, and characters who are learning who they are through magic. Inspired by J.K. Rowling's early storytelling.",
            "Make the world feel deep and weird: secret tunnels, flying libraries, and a prophecy with the wrong name on it. Channel Shannon Messenger's layered fantasy.",
            "The fantasy should serve both excitement and growth — fun but meaningful. Think coming-of-age through enchanted adventure."
         ]
    },
    "Spooky": {
        "3-5": [
            "Tell a spooky-but-silly story with friendly ghosts and silly shadows. Think Halloween through the eyes of a giggly toddler.",
            "Include funny 'boo!' sounds and a ghost who gets scared of its own reflection. Channel Scooby-Doo energy for little ones.",
            "Set the story in a haunted treehouse or a creaky attic filled with goofy echoes. Inspired by silly, not scary Halloween tales.",
            "Let the characters be scared of something silly — like a broom or a dancing skeleton. Think R.L. Stine meets a bedtime book."
        ],
        "6-8": [
            "Include flickering lights, friendly monsters, and mysterious sounds. Think Goosebumps Lite with a twist of humor.",
            "Set it in a haunted library or spooky sleepover where the ghost wants to play board games. Inspired by playful horror.",
            "Use suspense that turns funny — like a vampire who only drinks tomato juice. Channel a young R.L. Stine's goofy side.",
            "Let the story feel like a Halloween night full of laughs and mild shivers. Think Are You Afraid of the Dark? for kids."
        ],
        "9-11": [
            "Craft a mystery with eerie clues, creepy settings, and strange rules. Think Coraline meets R.L. Stine.",
            "Include an abandoned carnival, a whispering mirror, or an owl that delivers warnings. Inspired by light gothic horror.",
            "End with a twist — the monster was a misunderstood friend. Channel early Neil Gaiman for kids.",
            "Keep it thrilling but safe: spooky enough to be cool, but not nightmare fuel."
        ]
    },

    "Fairy Tale": {
        "3-5": [
            "Tell a whimsical story with talking animals, sparkly crowns, and kind heroes. Think classic fairy tales with a Mo Willems twist.",
            "Include a silly spell, a helpful mouse, and a giggling dragon. Inspired by Julia Donaldson's playful storytelling.",
            "Make the setting magical but friendly — a cupcake castle or a forest made of jellybeans. Channel the gentle charm of Mercer Mayer.",
            "End with a fun moral — like 'always say thank you to frogs who give directions.' Think Arnold Lobel meets fairy dust."
        ],
        "6-8": [
            "Write a fractured fairy tale where classic characters behave in surprising ways. Think Jon Scieszka meets Roald Dahl.",
            "Include a princess who refuses to be rescued and a knight afraid of glitter. Inspired by The Paper Bag Princess by Robert Munsch.",
            "Set it in a silly kingdom — one ruled by a goose who loves jam. Channel the quirky satire of Chris Colfer's Land of Stories.",
            "End with a happily-ever-after that no one expected — and maybe a dance party. Think fairy tale meets Dav Pilkey."
        ],
        "9-11": [
            "Craft a clever twist on fairy tale tropes — villains who turn out to be misunderstood, or heroes who mess things up. Think Gail Carson Levine or Shannon Hale.",
            "Include enchanted contracts, shape-shifting sidekicks, or kingdoms under weird curses. Inspired by The School for Good and Evil by Soman Chainani.",
            "Make the magic logical in strange ways — like only working when someone tells the truth while dancing. Channel the wit of E. Nesbit's fairy tales.",
            "Let the story question fairy tale logic while still honoring the magic. Witty, smart, and whimsical like Neil Gaiman's Fortunately, the Milk."
        ]
    },

    "Mystery": {
        "3-5": [
            "Write a mystery with a missing toy and a detective duck. Think Blue's Clues meets a giggly caper.",
            "Include visual clues, silly suspects, and a big group 'Aha!' moment. Inspired by toddler whodunits.",
            "Use rhyming clues and gentle tension — like a sock thief who turns out to be a sleepwalking puppy.",
            "Make the twist fun — the 'crime' was a surprise party in disguise."
        ],
        "6-8": [
            "Tell a junior detective tale with snacks as clues and a best friend sidekick. Think Nate the Great meets Diary of a Wimpy Kid.",
            "Include red herrings, goofy gadgets, and a silly disguise montage. Inspired by amateur kid sleuths.",
            "Let the case unfold with surprises and humor — like an investigation about missing homework that was never assigned.",
            "End with a pie chart made of real pie or a chalkboard full of cat doodles."
        ],
        "9-11": [
            "Create a layered mystery with secret passages, suspicious teachers, and hidden codes. Think Lemony Snicket or The Mysterious Benedict Society.",
            "Let the reader follow clues with the main character — solve puzzles, misinterpret things, and laugh along the way.",
            "Include a rival sleuth or a shadowy organization. Inspired by middle-grade thrillers with flair.",
            "The solution should surprise but make perfect sense — a big 'OHHHH!' moment."
        ]
    },

    "Bedtime": {
        "3-5": [
            "Tell a gentle tale with cuddly animals and glowing stars. Think Margaret Wise Brown's Goodnight Moon with extra giggles.",
            "Include soft repetition, nighttime sounds, and cozy blankets. Inspired by Sandra Boynton's calming books.",
            "Let the setting be magical — a cloud bed, a moonlit meadow, or a floating dream boat."
        ],
        "6-8": [
            "Craft a dreamlike story with slow adventure — like racing clouds or riding moonbeams. Think a lullaby with plot.",
            "Let the world be soothing — no danger, just wonder. Inspired by The House in the Night or Owl Moon.",
            "Use language that gets softer and sleepier — drifting, floating, shimmering."
        ],
        "9-11": [
            "Write a reflective bedtime tale about memories, dreams, or safe places. Think Kate DiCamillo meets Jacqueline Woodson.",
            "Let the tone be poetic and calm, like a meditation in story form.",
            "Include metaphors and sensory details — warm wind, distant stars, a mother's voice humming."
        ]
    },

    "Adventure": {
        "3-5": [
            "Write about a backyard quest with bouncy bridges, friendly lions, and treasure maps in crayon. Think Eric Carle meets Dora the Explorer.",
            "Include animals who act as guides and silly surprises like slippery banana vines. Inspired by The Little Explorers by Pat Hutchins.",
            "Let the hero swing, climb, and snack their way through the adventure. Channel Giraffes Can't Dance-level energy.",
            "End with a funny reward like a golden banana or a sandwich that sings."
        ],
        "6-8": [
            "Write a cartoon-style adventure with volcanoes, booby traps, and wacky races. Think Indiana Jones meets Captain Underpants.",
            "Include a goofy villain, a clumsy sidekick, and clever teamwork. Inspired by The Magic Tree House series.",
            "Let the plot be fast, silly, and surprising — jungle paths, ancient puzzles, and hidden snacks. Channel Dav Pilkey's chaos.",
            "End with a twist — like the treasure being a secret clubhouse or an ice cream coupon."
        ],
        "9-11": [
            "Craft a high-energy quest with narrow escapes, rival adventurers, and wild obstacles. Think Rick Riordan or Gordon Korman.",
            "Let the main character joke through danger, outwit traps, and accidentally save the day. Inspired by Percy Jackson's tone.",
            "Include a mystery subplot — like a map that changes or a legend that might be fake. Channel Artemis Fowl-style smarts.",
            "End with either a wild twist or an emotional reward — something worth the risk."
        ]
    },

    "Outer Space": {
        "3-5": [
            "Send the characters to a bouncy planet with friendly aliens and snack-shaped stars. Think Sandra Boynton meets Buzz Lightyear.",
            "Include rocket ships powered by giggles and planets made of cheese. Inspired by Goodnight Spaceman by Michelle Robinson.",
            "Make the mission silly — like finding the moon's lost pajamas or throwing a space parade.",
            "End with a cozy bedtime landing back on Earth."
        ],
        "6-8": [
            "Write a galactic adventure with robot sidekicks, rainbow asteroids, and zero-gravity dance-offs. Think Douglas Adams for kids.",
            "Include a space school field trip gone wrong or aliens with very weird customs. Inspired by Cosmic by Frank Cottrell-Boyce.",
            "Let the story be vibrant, unpredictable, and a little ridiculous. Channel Max Crumbly-style fun in space.",
            "Wrap up with an unexpected discovery — like a disco planet or a marshmallow black hole."
        ],
        "9-11": [
            "Launch a fast-paced space quest with malfunctioning tech, rival crews, and strange planets. Think Space Case by Stuart Gibbs.",
            "Include goofy AI, time loops, or a mysterious alien prank war. Inspired by quirky middle-grade sci-fi.",
            "Let the tone balance action and comedy — space danger that's also a little silly. Channel The Hitchhiker's Guide for tweens.",
            "End with a clever solution or weird friendship — like adopting a sarcastic alien plant."
        ]
    },

    "Science Fiction": {
        "3-5": [
            "Create a goofy tech world with singing robots and ticklish gadgets. Think Phineas and Ferb meets Sandra Boynton.",
            "Include inventions that do the wrong thing — like a snack machine that shoots socks. Inspired by Ada Twist, Scientist.",
            "Make the tech bright, beepy, and unexpected — and powered by laughter. Channel comic strip energy for little ones.",
            "Wrap up with a silly bedtime twist — the robot tucks the kid in or does a chicken dance."
        ],
        "6-8": [
            "Write a school science fair story gone wrong — shrinking rays, bubble shields, or cloning chaos. Think Asimov Jr. meets Big Nate.",
            "Let the hero be a genius-in-training with wild ideas and no filter. Inspired by Timmy Failure-style logic.",
            "Add talking gadgets, teleporters, or socks that run away. Keep the tone unpredictable and funny.",
            "End with a disaster that accidentally solves everything."
        ],
        "9-11": [
            "Create a clever, comic sci-fi world with slime reactors, AI teachers, or secret tech labs. Think Carl Hiaasen in space.",
            "Let the characters break the rules of time or physics — for fun. Inspired by Cory Doctorow's playful side.",
            "Include a tech mystery, a ridiculous solution, and a talking hamster who quotes Shakespeare.",
            "Wrap it up with a big idea… and an even bigger laugh."
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

    # Get randomized content flavor text
    content_options = content_by_theme_and_age.get(theme, {}).get(age_range, [])
    selected_elements = random.sample(content_options, min(3, len(content_options)))
    content_snippets = "\n".join(f"- {item}" for item in selected_elements)

    # Build clean, no-nonsense prompt
    prompt = f"""
Write an imaginative, age-appropriate story for a child aged {age_range}. 
The main character is named {character_name}, and the story should follow the theme: "{theme}".

Include:
{content_snippets}
{f"- A specific detail: {custom_detail}" if custom_detail else ""}

The story should have:
- A creative title
- A clear beginning (introduce setting and character)
- A fun middle (a problem or adventure)
- A satisfying ending (with resolution or twist)
- Around 500-650 words

Use a tone and storytelling style {style}.
Avoid narrator commentary or introductions — just start the story.
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
        size="1024x1024",  # DALL·E 3 only supports this size
        response_format="url"
    )
    return response["data"][0]["url"]