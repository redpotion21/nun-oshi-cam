import streamlink
import subprocess

urls = {'biboo' : "https://www.youtube.com/live/pmlucNPuIGw?si=4dm7lDHWxcUt_hdy",
         'sora' : "https://www.youtube.com/live/1Hf0O4Du6ss?si=X1Sgr8wQJ4e11iP2"}

url =  urls['biboo'] # or direct m3u8 if you have it

# Create session (options if needed)
session = streamlink.Streamlink()

# Get available streams
streams = session.streams(url)

if not streams:
    print("No streams found... maybe not available anymore?")
else:
    best = streams["best"]  # or "720p", "audio_only" etc
    print("Best stream URL~!", best.url)
    
    # Play it with mpv (best choice) or vlc/ffplay
    # Make sure mpv is installed! (or change to "vlc" or "ffplay")
    subprocess.run(["mpv", best.url])
    # Or: subprocess.run(["vlc", best.url])