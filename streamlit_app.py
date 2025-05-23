import os
from dotenv import load_dotenv

# ✅ Load your .env into os.environ
load_dotenv()

import streamlit as st
import openai
from elevenlabs import set_api_key
from PIL import Image
from tinker_core import generate_story, generate_image, select_voice, narrate_story

# ✅ Pull API keys from the environment
openai.api_key   = os.getenv("OPENAI_API_KEY")
set_api_key(os.getenv("ELEVEN_API_KEY"))

# ——— Page config & CSS —————————————————————————————————
st.set_page_config(page_title="TinkerTales Storymaker", page_icon="✨")
st.markdown(
    """
    <style>
      /* 📖 Open-book two-page spread */
      .storybook {
        margin: 1rem 0;
        padding: 1rem;
        font-family: "Times New Roman", serif;
        line-height: 1.6;
        /* remove margin:auto and background */
      }
      .storybook p {
        margin: 0.5rem 0;
      }
      h1, h2, h3 {
        font-family: 'Comic Sans MS', cursive;
      }
    </style>
    """,
    unsafe_allow_html=True
)

# ——— Header & Logo —————————————————————————————————————
st.title("📖✨ TinkerTales Storymaker")
st.caption("Where imagination meets AI and comes to life.")
st.markdown("&nbsp;", unsafe_allow_html=True)
logo = Image.open("assets/logo.png")
st.image(logo, use_container_width=True)
st.markdown("&nbsp;", unsafe_allow_html=True)
st.markdown("### ✏️ Watch Your Brainstorm Come to Life!")

# ——— Sidebar: Inputs & “Generate Story” ————————————————————
with st.sidebar:
    st.header("🛠 Story Settings")
    name = st.text_input("Character name", value="Ani")
    age = st.selectbox("Age range", ["3-5", "6-8", "9-11"])
    theme = st.selectbox(
        "Theme",
        ["Adventure", "Bedtime", "Fairy Tale", "Fantasy", "Mystery", "Outer Space", "Spooky"]
    )
    story_prompt = st.text_area("Story prompt")
    custom_detail = st.text_area("Special detail")
    if st.button("✍️ Generate Story"):
        with st.spinner("Writing your story..."):
            try:
                st.session_state["story"] = generate_story(
                    name, age, theme, custom_detail, story_prompt
                )
            except Exception as e:
                st.error(f"Story generation failed: {e}")

# ——— Tabs for Story / Illustration / Narration ——————————————
st.markdown("**➡️ Click the tabs below to view your Illustration and Narration!**")
tab1, tab2, tab3 = st.tabs(["📖 Story", "🖼 Illustration", "🎧 Narration"])

# — Story Tab ——————————————————————————————————————————
with tab1:
    if "story" in st.session_state:
        # Pull out the first line as the title, and the rest as body
        full_story = st.session_state["story"].strip()
        lines      = full_story.split("\n", 1)
        title      = lines[0]
        body       = lines[1] if len(lines) > 1 else ""

        # Build a single HTML block with the heading inside .storybook
        story_html = f"""
          <div class='storybook'>
            <h1 style="margin-top:0;">{title}</h1>
        """
        for para in body.split("\n\n"):
            story_html += f"<p>{para}</p>"
        story_html += "</div>"

        st.markdown(story_html, unsafe_allow_html=True)
    else:
        st.info("Generate a story from the sidebar to get started.")

# — Illustration Tab ————————————————————————————————————
with tab2:
    if "story" in st.session_state:
        if st.button("🖼️ Generate Illustration", key="illustrate"):
            with st.spinner("Drawing your story..."):
                try:
                    img_prompt = f"A whimsical illustration of {name} in a {theme} children's story"
                    url = generate_image(img_prompt)
                    st.image(url, caption="AI-generated illustration", use_container_width=True)
                except Exception as e:
                    st.error(f"Image generation failed: {e}")
    else:
        st.info("First generate a story, then come here for an illustration.")

# — Narration Tab ——————————————————————————————————————
with tab3:
    if "story" in st.session_state:
        filename = f"{name.lower()}_{theme.lower().replace(' ', '_')}.mp3"
        if st.button("🎧 Generate Narration", key="narrate"):
            with st.spinner("Narrating…"):
                try:
                    voice_id = select_voice(theme, age)
                    narrate_story(st.session_state["story"], filename, voice_id)
                except Exception as e:
                    st.error(f"Narration failed: {e}")
        if os.path.exists(filename):
            audio_bytes = open(filename, "rb").read()
            st.audio(audio_bytes, format="audio/mp3")
            st.download_button("Download MP3", audio_bytes, file_name=filename, mime="audio/mpeg")
    else:
        st.info("Your story audio will appear here after generation.")