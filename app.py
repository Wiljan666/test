import streamlit as st
import youtube_dl

def download_video(url):
    try:
        ydl_opts = {
            'outtmpl': './downloads/%(title)s.%(ext)s',
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'verbose': True,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
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
