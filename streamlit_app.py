import streamlit as st
import openai
from elevenlabs import set_api_key
import os
from dotenv import load_dotenv
from PIL import Image
from tinker_core import generate_story, narrate_story, select_voice, generate_image

# ✅ Set Streamlit page config
st.set_page_config(page_title="TinkerTales Storymaker", page_icon="✨")

# ✅ Load secrets into environment
openai.api_key = st.secrets["OPENAI_API_KEY"]
set_api_key(st.secrets["ELEVEN_API_KEY"])

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

st.markdown("### ✏️ Watch Your Brainstorm Come to Life!")

# Inputs
name = st.text_input("Character name", value="Ani")
age = st.selectbox("Age range", ["3-5", "6-8", "9-11"])
theme = st.selectbox("Theme", [
    "Adventure", "Bedtime", "Fairy Tale", "Fantasy", 
    "Mystery", "Outer Space", "Spooky"
])
story_prompt = st.text_area("Story prompt")
custom_detail = st.text_area("Add any special details you'd like!")

# Generate story
if st.button("Generate Story"):
    with st.spinner("Writing your story..."):
        story = generate_story(name, age, theme, custom_detail, story_prompt)
        st.session_state["story"] = story
        st.session_state["voice"] = select_voice(theme, age)

# ✅ Simple story display (persists after rerun)
if "story" in st.session_state:
    st.text_area("Your Story", st.session_state["story"], height=350)

    # Generate and display image
    if st.button("🖼️ Generate Illustration"):
        with st.spinner("Drawing your story..."):
            image_prompt = f"A whimsical illustration of {name} in a {theme} story for children"
            image_url = generate_image(image_prompt)
            st.image(image_url, caption="AI-generated illustration", use_container_width=True)

# Generate narration
if "story" in st.session_state and st.button("🎧 Generate Narration"):
    with st.spinner("Narrating your story..."):
        filename = f"{name.lower()}_{theme.lower().replace(' ', '_')}.mp3"
        narrate_story(st.session_state["story"], filename, st.session_state["voice"])
        with open(filename, "rb") as f:
            st.download_button("Download Narrated Story", f, file_name=filename, mime="audio/mpeg")