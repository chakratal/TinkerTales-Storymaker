import streamlit as st
import openai
from elevenlabs import set_api_key
import os
from dotenv import load_dotenv

# ✅ Set Streamlit page config
st.set_page_config(page_title="TinkerTales Storymaker", page_icon="✨")

from PIL import Image

# ✅ Load secrets into environment
openai.api_key = st.secrets["OPENAI_API_KEY"]
set_api_key(st.secrets["ELEVEN_API_KEY"])

# ✅ Now import core logic
from tinker_core import generate_story, narrate_story, select_voice

# ✅ UI
st.title("📖✨ TinkerTales Storymaker")
st.caption("Where imagination meets AI and comes to life.")

# 👆 Add space above the image
st.markdown("&nbsp;", unsafe_allow_html=True)

# ✅ Load and display logo
logo_image = Image.open("assets/logo.png")
st.image(logo_image, use_container_width=True)

# 👇 Space below the image
st.markdown("&nbsp;", unsafe_allow_html=True)

st.markdown("## ✏️ Add Your Details and Make Your Story Come to Life!")

# Inputs
name = st.text_input("Character name", value="Ani")
age = st.selectbox("Age range", ["3-5", "6-8", "9-11"])
theme = st.selectbox("Theme", [
    "Fantasy", "Fairy Tale", "Bedtime", "Comedy", "Adventure",
    "Spooky", "Mystery", "Outer Space", "Science Fiction"
])
custom_detail = st.text_area("Have special details you'd like to include? Add them here", placeholder="e.g., Ani wears a shirt with stars...")

# Generate story
if st.button("Generate Story"):
    with st.spinner("Writing your story..."):
        story = generate_story(name, age, theme, custom_detail)
        st.session_state["story"] = story
        st.session_state["voice"] = select_voice(theme, age)

# ✅ Always show the story if it exists (even after rerun)
if "story" in st.session_state:
    st.text_area("Your Story", st.session_state["story"], height=350)

# Generate narration
if "story" in st.session_state and st.button("🎧 Generate Narration"):
    with st.spinner("Narrating your story..."):
        filename = f"{name.lower()}_{theme.lower().replace(' ', '_')}.mp3"
        narrate_story(st.session_state["story"], filename, st.session_state["voice"])
        with open(filename, "rb") as f:
            st.download_button("Download Narrated Story", f, file_name=filename, mime="audio/mpeg")