import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from elevenlabs import generate, set_api_key, VoiceSettings

from tinker_core import generate_story, narrate_story, select_voice

# Load secrets
load_dotenv()
set_api_key(st.secrets["ELEVEN_API_KEY"])
openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="TinkerTales Storymaker", page_icon="✨")
st.title("📖✨ TinkerTales Storymaker")
st.caption("Where imagination meets AI and comes to life.")

# Inputs
name = st.text_input("Character name", value="Ani")
age = st.selectbox("Age range", ["3-5", "6-8", "9-11"])
theme = st.selectbox("Theme", [
    "Fantasy", "Fairy Tale", "Bedtime", "Comedy", "Adventure",
    "Spooky", "Mystery", "Outer Space", "Science Fiction"
])
custom_detail = st.text_area("Optional detail", placeholder="e.g., Ani wears a shirt with stars...")

if st.button("Generate Story"):
    with st.spinner("Writing your story..."):
        story = generate_story(name, age, theme, custom_detail)
        st.session_state["story"] = story
        st.session_state["voice"] = select_voice(theme, age)
        st.text_area("Your Story", story, height=350)

if "story" in st.session_state and st.button("🎧 Generate Narration"):
    with st.spinner("Narrating your story..."):
        filename = f"{name.lower()}_{theme.lower().replace(' ', '_')}.mp3"
        narrate_story(st.session_state["story"], filename, st.session_state["voice"])
        with open(filename, "rb") as f:
            st.download_button("Download Narrated Story", f, file_name=filename, mime="audio/mpeg")