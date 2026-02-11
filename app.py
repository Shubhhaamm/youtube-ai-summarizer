import streamlit as st
import re
import os
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai


genai.configure(api_key="AIzaSyAlx9bdhQcgLP-WhFUUDoWqv_urKzFZimM")

model = genai.GenerativeModel("gemini-2.5-flash-lite")


def get_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

st.set_page_config(page_title="YouTube AI Summarizer", page_icon="🎥")

st.title("🎥 YouTube Transcript Summarizer")
st.write("Generate English summary + Hindi translation using Gemini AI")

url = st.text_input("Enter YouTube URL")

if st.button("Generate Summary"):

    if not url:
        st.warning("Please enter a YouTube URL.")
    else:
        video_id = get_video_id(url)

        if not video_id:
            st.error("Invalid YouTube URL.")
        else:
            try:
                with st.spinner("Fetching transcript..."):
                    api = YouTubeTranscriptApi()
                    transcript = api.fetch(video_id)

                    text = " ".join([t.text for t in transcript])

                with st.spinner("Generating summary using Gemini..."):

                    prompt = f"""
                    Summarize the following transcript in 8-10 clear bullet points.
                    Then provide the final summary in Hindi.

                    Transcript:
                    {text[:20000]}
                    """

                    response = model.generate_content(prompt)

                st.success("Summary Generated!")

                st.subheader("📌 AI Output")
                st.write(response.text)

            except Exception as e:
                st.error(f"Error: {str(e)}")
