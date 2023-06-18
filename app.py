import streamlit as st
import subprocess

def download_video(url):
    try:
        options = [
            "youtube-dl",
            "-o",
            "./downloads/%(title)s.%(ext)s",
            "--format",
            "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--verbose",
            url,
        ]
        subprocess.run(options, check=True)
        st.success("Downloaden gelukt!")
    except subprocess.CalledProcessError as e:
        st.error(f"Er is een fout opgetreden bij het downloaden: {e}")

# Streamlit-app
st.title("YouTube Downloader")

# Invoerveld voor URL
url = st.text_input("Voer de YouTube-video URL in")

# Downloadknop
if st.button("Download"):
    if url:
        download_video(url)
    else:
        st.warning("Voer een geldige YouTube-video URL in.")
