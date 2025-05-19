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
            "Write a funny story in the style of Sandra Boynton where a frog opens a lemonade stand on the moon and keeps forgetting the recipe. The tone should be silly and joyful.",
            "Tell a goofy tale like Mo Willems where a hippo thinks it's a helicopter and zooms through the playground.",
            "Craft a bouncy story like Dr. Seuss where a duck wears shoes on its head to a dance party.",
            "In the voice of Sandra Boynton, tell about a goat who invents a sandwich launcher that causes lunchroom chaos.",
            "Write a hilarious story where the main character turns into a banana and is totally fine with it — told like a giggly board book."
        ],
        "6-8": [
            "Write a funny story in the style of Dav Pilkey where a squirrel mayor declares war on spoons and holds a press conference inside a bouncy castle.",
            "Tell a ridiculous adventure where a kazoo parade accidentally attracts spaghetti from space. Think Captain Underpants.",
            "Create a story in the tone of Diary of a Wimpy Kid featuring a raccoon detective who only speaks in riddles.",
            "Write a comic tale where a kid battles a chicken over the last jelly donut — using interpretive dance. Go full Pilkey.",
            "End with a totally unnecessary glitter explosion. Make it chaotic, fast, and full of absurd visuals."
        ],
        "9-11": [
            "Write a satirical, dry-humored story in the style of Roald Dahl about a cheese rebellion led by a sock puppet with political ambitions.",
            "Tell a story like Lemony Snicket where a bureaucratic llama refuses to approve anything unless it's written in limerick.",
            "Include an evil villain whose master plan is to turn toilets into jazz musicians. Use witty narration.",
            "Have the narrator complain constantly about the ridiculousness of the plot while telling it anyway.",
            "End with a cosmic twist: it was all a dream dreamt by a hamster in space court. Make it absurd but clever."
        ]
    },

    "Spooky": {
        "3-5": [
            "Write a silly-spooky story in the tone of Scooby-Doo where a ghost gets stuck in a jelly jar and can only escape by sneezing.",
            "Tell a story like Sandra Boynton about a haunted blanket that insists on tucking people in — even at lunch.",
            "Create a mildly eerie setting: a creaky attic that giggles when someone says 'banana'. Keep it safe and silly.",
            "In the style of R.L. Stine’s funnier tales, tell about a skeleton who keeps losing its bones during hide-and-seek.",
            "End with the characters being scared of a broom that just wants a hug. Lighthearted spooks only."
        ],
        "6-8": [
            "Write a playful horror story in the style of Goosebumps about a vampire who moves into a treehouse but is afraid of pinecones.",
            "Include a glittery ghost who sings sea shanties and leaves confusing clues. Keep the tone eerie-funny.",
            "Set the tale in a haunted library where the books whisper nonsense like ‘pickle pancakes’.",
            "Tell a suspenseful but humorous story about a monster who politely asks to borrow socks from under the bed.",
            "End with a twist: the scary shadow was just a snoring platypus."
        ],
        "9-11": [
            "Write a spooky mystery in the tone of Neil Gaiman (Coraline-lite) where a creepy carnival appears overnight with cursed rides.",
            "Include an owl who gives cryptic warnings like ‘never trust your elbows’. Build atmosphere.",
            "Let the curse slowly turn people into vegetables — starting with their socks. Make it eerie with dark humor.",
            "Use odd imagery: fog that smells like bubblegum and clocks that run backward.",
            "End with the characters solving the mystery by performing a ghostly musical number. Slightly creepy, very weird."
        ]
    },

    "Fairy Tale": {
        "3-5": [
            "Write a whimsical fairy tale in the style of Julia Donaldson where a dragon hoards teddy bears and refuses to share.",
            "Tell a playful story about a frog prince who can only speak in bubbles. Make it rhyme if you like.",
            "Include a cupcake castle guarded by a yodeling mouse. Magical but silly.",
            "In the style of Mercer Mayer, have everyone wear socks on their hands to break a glitter curse.",
            "Make the hero’s best friend a spoon with a crown. Gentle and imaginative."
        ],
        "6-8": [
            "Write a fairy tale like Robert Munsch where a knight must rescue a prince from a syrup-filled waffle tower.",
            "Include a goose queen who insists everyone walk backward. Add magical logic.",
            "Make a spell turn people into goats unless they solve a cheese riddle. Add personality to the goats.",
            "Set it in a forest where the trees gossip and give confusing directions.",
            "End with a dance battle between fairies and a sandwich. Think Jon Scieszka."
        ],
        "9-11": [
            "Craft a clever fairy tale in the tone of Gail Carson Levine where villains must attend etiquette school taught by a sarcastic cat.",
            "Include enchanted contracts written in pudding. Magical realism encouraged.",
            "Have a magic mirror cursed to only tell dad jokes. Snarky tone.",
            "Include a puzzle-staircase that changes shape based on pizza toppings.",
            "End with a royal decree that Tuesdays are for pillow forts. Smart and playful."
        ]
    },

    "Adventure": {
        "3-5": [
            "Tell an adventure story in the style of Dora the Explorer where a lion leads a backyard treasure hunt past bouncy bridges.",
            "Include a banana vine, a peanut butter river, and a helpful flamingo with sunglasses.",
            "Make the quest snack-filled and silly, with talking sandwiches and a lost crayon map.",
            "Keep it upbeat and physical — lots of swinging, climbing, sliding.",
            "End with a treasure chest full of silly socks or singing juice boxes."
        ],
        "6-8": [
            "Write a chaotic adventure like Magic Tree House meets Dav Pilkey with volcano slides and booby-trapped snack caves.",
            "Let the villain be allergic to glitter. Include a sidekick who constantly misreads the map.",
            "Use fast pacing and silly challenges — lava made of soda, trampoline bridges, or a maze of mirrors.",
            "End with a twist: the treasure is a treehouse with every flavor of ice cream.",
            "Make it action-packed, lighthearted, and a little absurd."
        ],
        "9-11": [
            "Craft an exciting quest like Percy Jackson where the hero outwits magical traps using humor and snacks.",
            "Include a rival adventurer who only speaks in pirate slang. Let them argue constantly.",
            "Add a mystery subplot: a treasure map that changes when you sneeze.",
            "Keep the pace high and the tone funny-dramatic — danger with punchlines.",
            "End with either a wild twist or a heartfelt reward. Think Gordon Korman with a wink."
        ]
    },

        "Outer Space": {
        "3-5": [
            "Tell a silly space adventure in the tone of Sandra Boynton where a raccoon astronaut loses their juice box on Planet Noodle.",
            "Include a moon that sings lullabies and aliens shaped like marshmallows. Keep the tone dreamy and goofy.",
            "Have the spaceship run on giggles and burps. Make it bright, cheerful, and weird.",
            "Include a mission to find the moon’s missing pajamas, with friendly aliens helping out.",
            "End with a bedtime landing on Earth where everyone falls asleep mid-giggle."
        ],
        "6-8": [
            "Write a goofy space quest like Douglas Adams for kids where an asteroid turns into a dance floor.",
            "Include a space school field trip gone wrong involving teleporters and banana gravity.",
            "Make the aliens very confused about human things like socks and spoons. Channel middle-grade absurdism.",
            "Let the main character win a zero-gravity pie-eating contest to save the day.",
            "Wrap up with a celebration on a disco planet. Keep it unpredictable and fun."
        ],
        "9-11": [
            "Tell a clever sci-fi comedy where rival space crews must race through a jellyfish galaxy. Think Space Case meets Hitchhiker’s Guide.",
            "Include a snarky robot and a sarcastic alien plant that gives bad advice.",
            "Have time loops that result in silly consequences, like repeated birthday cake.",
            "Include dramatic space danger undercut by ridiculous tools, like a laser plunger.",
            "End with the discovery that Earth was just a space zoo for penguins. Keep the tone witty and weird."
        ]
    },

    "Science Fiction": {
        "3-5": [
            "Write a silly sci-fi tale like Ada Twist meets Phineas and Ferb, where a robot keeps sneezing glitter.",
            "Include inventions that do the opposite of what they’re supposed to — like a snack machine that gives you socks.",
            "Set it in a techy world with blinking buttons and squeaky gadgets. Keep it colorful and noisy.",
            "Have a kid build a rocket with jellybeans and rubber bands. Go full science chaos.",
            "End with the robot reading everyone a bedtime story through a kazoo."
        ],
        "6-8": [
            "Write a school science fair story gone wrong in the tone of Big Nate meets Timmy Failure.",
            "Include a shrinking ray that makes sandwiches huge and people tiny. Go for comic absurdity.",
            "Let the main character try to invent something cool and accidentally clone a talking hamster.",
            "Make the tech ridiculous but consistent — include malfunctioning teleporters and exploding bubble shields.",
            "End with the project winning a prize... for 'Weirdest Use of Cheese'."
        ],
        "9-11": [
            "Write a smart and ridiculous story like Cory Doctorow’s lighter fiction where kids hack reality using banana-powered laptops.",
            "Include a debate over whether AI should be allowed to eat nachos.",
            "Have a villain trying to erase recess from the space-time continuum.",
            "Let the main character be part of a secret science club that builds teleporting pajamas.",
            "End with a big idea... and an even bigger laugh. Keep it inventive, fast-paced, and weird."
        ]
    },

    "Bedtime": {
        "3-5": [
            "Tell a soothing, lyrical story in the tone of Margaret Wise Brown about a bunny who rides a cloud boat through a starlit sky.",
            "Include soft repetition, sleepy sounds, and cozy images like glowing windows and yawning kittens.",
            "Keep the pacing slow and gentle — perfect for winding down.",
            "Let the story feel like a lullaby, with tiny magical moments like whispering stars.",
            "End with the character drifting to sleep in a blanket shaped like the moon."
        ],
        "6-8": [
            "Write a dreamy tale like Owl Moon where a child explores a quiet forest of glowing trees and talking owls.",
            "Let the story unfold gently — no real danger, just wonder. Keep the tone meditative and poetic.",
            "Include soft images: misty hills, glowing fireflies, and calm rivers.",
            "Use language that flows like a bedtime song — drifting, shimmering, peaceful.",
            "End with the characters returning to bed, their adventure becoming a dream."
        ],
        "9-11": [
            "Write a reflective bedtime story in the style of Kate DiCamillo or Jacqueline Woodson about memories, safety, and inner stillness.",
            "Include metaphors and gentle sensory details like ‘wind that hums like a cello’ or ‘a blanket full of stories’.",
            "Make the tone nostalgic and thoughtful, with emotional resonance.",
            "Let the setting feel like a memory half-remembered: golden light, quiet voices, the warmth of a parent's hand.",
            "End on a quiet, hopeful note — ready for sleep but full of dreams."
        ]
    },

    "Mystery": {
        "3-5": [
            "Tell a giggly detective story in the tone of Blue’s Clues about a duck who investigates missing cookies with help from a talking crayon.",
            "Include silly suspects like a winking toaster and a sleepy sloth. Keep it light and clue-filled.",
            "Use visual-style clues — think rhyming riddles and colorful footprints.",
            "Make the twist fun: the thief was a sleepwalking teddy bear.",
            "Wrap it up with a group hug and a celebration dance party."
        ],
        "6-8": [
            "Write a junior mystery in the spirit of Nate the Great or Encyclopedia Brown, but funnier.",
            "Include red herrings like a ketchup trail and a chicken with a monocle.",
            "Make the detective use ridiculous gadgets like the Sniff-o-Meter 3000.",
            "Let the mystery unfold with confusion and laughs — the clues always almost make sense.",
            "End with a solved case and an award ceremony involving glitter and pancakes."
        ],
        "9-11": [
            "Write a smart, strange mystery in the tone of Lemony Snicket or The Mysterious Benedict Society.",
            "Include weird clues: invisible ink on bananas, secret tunnels under the art room, a whispering sock puppet.",
            "Make the tone witty, the stakes low-stress but intriguing.",
            "Let the sleuths have rivalries and quirks — one’s afraid of paperclips, another speaks in haiku.",
            "End with a surprise that’s clever and ridiculous: the culprit was the school mascot, possessed by a bored librarian ghost."
        ]
    },

        "Fantasy": {
        "3-5": [
            "Write a fun and magical story in the tone of Julia Donaldson where a tiny dragon loses its sparkle and goes on a giggly quest to get it back.",
            "Include friendly talking animals, silly spells, and a wizard who forgets everything. Keep it playful and rhyming where possible.",
            "Set it in a sparkly forest with rainbow trees and flying cupcakes. Keep the tone light and full of whimsy.",
            "The hero should solve problems through kindness, with a magic hiccup or two.",
            "End with the magic being restored through a hug and a dance party."
        ],
        "6-8": [
            "Tell a magical adventure in the tone of C.S. Lewis meets Mo Willems where a reluctant hero finds a map in their cereal and follows it to a hidden kingdom.",
            "Include clumsy sorcerers, riddle-speaking frogs, and a broom that thinks it's a dog.",
            "Keep the fantasy light, funny, and fast-moving with playful twists.",
            "Let the setting be full of odd logic — a castle that rotates and a pond that tells jokes.",
            "End with the main character learning something sweet and surprising — like how to talk to stars."
        ],
        "9-11": [
            "Write a rich, imaginative fantasy story like early Harry Potter or Keeper of the Lost Cities, filled with strange rules and heartfelt magic.",
            "Include magical objects with odd side effects, secret passageways, and creatures who act too human.",
            "Make the tone exciting, layered, and just a little mysterious — with funny moments mixed in.",
            "The hero should grow through the journey, facing weird but meaningful magical challenges.",
            "End with an unexpected magical twist that ties everything together — something clever and a little weird."
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