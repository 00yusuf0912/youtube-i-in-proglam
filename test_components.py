import yt_dlp
import customtkinter as ctk

# Test yt-dlp
print("Testing yt-dlp...")
try:
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        print("yt-dlp: OK")
except Exception as e:
    print(f"yt-dlp error: {e}")

# Test customtkinter
print("Testing CustomTkinter...")
try:
    ctk.set_appearance_mode("dark")
    print("CustomTkinter: OK")
except Exception as e:
    print(f"CustomTkinter error: {e}")

print("All tests passed!")