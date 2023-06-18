import streamlit as st
from pytube import YouTube

def download_video(url):
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video.download('./downloads')
        st.success("Downloaden gelukt!")
    except Exception as e:
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
