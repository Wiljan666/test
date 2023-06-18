import streamlit as st
import subprocess

# Functie voor het downloaden van de video
def start_download_video(url, switch_value):
    try:
        options = [
            "youtube-dl",
            "-o",
            "%(title)s.%(ext)s",
            "-f",
            "bestaudio/best" if switch_value else "bestvideo+bestaudio",
            url,
        ]
        subprocess.run(options, check=True)
        if switch_value:
            st.success("Downloaden audio gelukt")
        else:
            st.success("Downloaden video gelukt")
    except subprocess.CalledProcessError:
        st.error("Download link niet correct")

# UI-elementen
st.title("YouTube Downloader")
st.subheader("Geef een YouTube URL op")
yt_link = st.text_input("YouTube URL")
switch_checkbox = st.checkbox("Alleen audio")
start_download_button = st.button("Download", key="download_button")

if start_download_button:
    start_download_video(yt_link, switch_checkbox)
