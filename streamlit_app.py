import os
import re
from dotenv import load_dotenv
import streamlit as st
import openai
from elevenlabs import set_api_key
from PIL import Image
from datetime import datetime
from tinker_core import (
    generate_story,
    generate_image,
    generate_image_from_story,
    summarize_for_image,
    select_voice,
    narrate_story,
)

# ——— Utility ———————————————————————————————————————
def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

# ——— Load environment variables ——————————————————————
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
set_api_key(os.getenv("ELEVEN_API_KEY"))

# ——— Page config & CSS —————————————————————————————————
st.set_page_config(page_title="TinkerTales Storymaker", page_icon="✨")
st.markdown("""
    <style>
      .storybook {
        margin: 1rem 0;
        padding: 1rem;
        font-family: "Times New Roman", serif;
        line-height: 1.6;
      }
      .storybook p {
        margin: 0.5rem 0;
      }
      h1, h2, h3 {
        font-family: 'Comic Sans MS', cursive;
      }
    </style>
""", unsafe_allow_html=True)

# ——— Header & Logo —————————————————————————————————————
st.title("📖✨ TinkerTales Storymaker")
st.caption("Where imagination meets AI and comes to life.")
st.markdown("&nbsp;", unsafe_allow_html=True)
st.image(Image.open("assets/logo.png"), use_container_width=True)
st.markdown("&nbsp;", unsafe_allow_html=True)
st.markdown("### ✏️ Watch Your Brainstorm Come to Life!")

# ——— Sidebar Inputs ————————————————————————————————————
with st.sidebar:
    st.header("🛠 Story Settings")
    name = st.text_input("Character name", value="Ani")
    age = st.selectbox("Age range", ["3-5", "6-8", "9-11"])
    theme = st.selectbox("Theme", ["Adventure", "Bedtime", "Fairy Tale", "Fantasy", "Mystery", "Outer Space", "Spooky"])
    story_prompt = st.text_area("Story prompt")
    custom_detail = st.text_area("Special detail")

# ——— Main Tabs ————————————————————————————————————————
st.markdown("**Click the tabs below&nbsp;⬇️**", unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(["📖 Story", "🖼 Illustration", "🎧 Narration", "📚 Library"])

# ——— Story Generation ———————————————————————————————
if st.sidebar.button("✍️ Generate Story"):
    with st.spinner("Writing your story..."):
        try:
            title, full_story = generate_story(name, age, theme, custom_detail, story_prompt)
            st.session_state["story"] = full_story
            st.session_state["title"] = title

            # ✅ Save to story library
            if "library" not in st.session_state:
                st.session_state["library"] = []
            st.session_state["library"].insert(0, {
                "title": title,
                "story": full_story,
                "theme": theme,
                "age": age,
                "character": name
            })
            st.session_state["library"] = st.session_state["library"][:10]

        except Exception as e:
            st.error(f"Story generation failed: {e}")

# ——— Tab 1: Story —————————————————————————————————————————
with tab1:
    if "story" in st.session_state:
        full_story = st.session_state["story"].strip()
        lines = full_story.split("\n", 1)
        title = lines[0]
        body = lines[1] if len(lines) > 1 else ""

        story_html = f"""
          <div class='storybook'>
            <h1 style="margin-top:0;">{title}</h1>
        """
        for para in body.split("\n\n"):
            story_html += f"<p>{para}</p>"
        story_html += "</div>"

        st.markdown(story_html, unsafe_allow_html=True)
    else:
        st.info("Add details to the sidebar on the left to generate a story.")

# ——— Tab 2: Illustration ———————————————————————————————
with tab2:
    if "story" in st.session_state:
        story_text = st.session_state["story"]
        display_caption = st.session_state.get("title")

        if st.button("🖼️ Generate Illustration", key="illustrate"):
            with st.spinner("Drawing your story..."):
                try:
                    from tinker_core import generate_image_from_story  # Make sure this is imported!
                    url = generate_image_from_story(name, theme, custom_detail, story_prompt)
                    st.session_state["illustration"] = url
                    if st.session_state.get("library"):
                        st.session_state["library"][0]["illustration"] = url
                except Exception as e:
                    st.error(f"Image generation failed: {e}")

        if "illustration" in st.session_state:
            st.image(st.session_state["illustration"], caption=display_caption, use_container_width=True)

    else:
        st.info("Come here after you generate a story to create a custom illustration.")

# ——— Tab 3: Narration ———————————————————————————————————
with tab3:
    if "story" in st.session_state:
        if st.button("🎧 Generate Narration", key="narrate"):
            with st.spinner("Narrating…"):
                try:
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    story_title = slugify(st.session_state.get("title", "story"))
                    filename = f"{name.lower()}_{theme.lower().replace(' ', '_')}_{story_title}_{timestamp}.mp3"
                    voice_id = select_voice(theme, age)
                    narrate_story(st.session_state["story"], filename, voice_id)
                    st.session_state["audio_filename"] = filename
                except Exception as e:
                    st.error(f"Narration failed: {e}")

        if "audio_filename" in st.session_state and os.path.exists(st.session_state["audio_filename"]):
            audio_bytes = open(st.session_state["audio_filename"], "rb").read()
            st.audio(audio_bytes, format="audio/mp3")
            st.download_button("Download MP3", audio_bytes, file_name=st.session_state["audio_filename"], mime="audio/mpeg")
    else:
        st.info("Your story audio will appear after your story generates.")

# ——— Tab 4: Library —————————————————————————————————————
with tab4:
    st.subheader("📚 Story Library")
    if "library" in st.session_state and st.session_state["library"]:
        for idx, entry in enumerate(st.session_state["library"]):
            with st.expander(f"{entry['title']} — {entry['character']} ({entry['theme']}, age {entry['age']})", expanded=(idx == 0)):
                if "illustration" in entry:
                    st.markdown("<div style='margin: 1rem 0;'><img src='{}' width='300'/></div>".format(entry["illustration"]), unsafe_allow_html=True)
                for para in entry["story"].split("\n\n"):
                    st.markdown(f"<p style='margin:0 0 0.5rem 0;'>{para}</p>", unsafe_allow_html=True)
    else:
        st.info("Your library will get bigger and bigger with each story you write.")