import yt_dlp
import os

# Folder jahan humari MP3 files save hongi (Scripts folder se bahar nikal kar data folder mein)
SAVE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

# Bhai yahan par tu apni uss System Design wali playlist ka URL paste kar dena
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLQEaRBV9gAFvzp6XhcNFpk1WdOcyVo9qT"

def download_first_15_audio(playlist_url, save_path):
    print("Baba ji ka naam lekar downloading shuru karte hain! 🚀")
    print(f"Audio files yahan save hongi: {save_path}")

    # yt-dlp ki premium settings
    ydl_opts = {
        'format': 'bestaudio/best', # Sirf audio download karni hai
        'playlist_items': '1-15',   # Sirf pehli 15 videos uthayega
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        # File ka naam aise save hoga: 1_IntroToSystemDesign.mp3
        'outtmpl': os.path.join(save_path, '%(playlist_index)s_%(title)s.%(ext)s'), 
        'ignoreerrors': True, # Agar playlist mein koi video private hui, toh script crash nahi hogi
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
        print("✅ Bhai, saari 15 videos ki audio successfully download ho gayi hai! 🎉")
    except Exception as e:
        print(f"❌ Bhai kuch error aa gaya: {e}")

if __name__ == "__main__":
    # Agar data folder galti se delete ho gaya ho, toh yeh khud bana dega
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)
        
    download_first_15_audio(PLAYLIST_URL, SAVE_PATH)