from yt_dlp import YoutubeDL

url = "https://www.youtube.com/live/1Hf0O4Du6ss?si=gBNe3LsGCWWLFR8J"  # change this!!

opts = {
    'quiet': True,          # no spam in console
    'no_warnings': True,
    'format': 'best',       # or 'bestvideo+bestaudio' if you want
    'skip_download': True   # super important, only get info!
}

with YoutubeDL(opts) as ydl:
    info = ydl.extract_info(url, download=False)
    
    # Find the best live/HLS URL
    if 'formats' in info:
        for f in info['formats']:
            if f.get('protocol') == 'm3u8_native' or 'm3u8' in f.get('url', ''):
                print("Live stream URL found~!")
                print(f['url'])
                break
        else:
            print("No m3u8 found... try checking formats?")
            # Or print all urls to see
            # print([f['url'] for f in info['formats'] if 'url' in f])
    else:
        print("Hmm... no formats? Is it really live?")

import subprocess
subprocess.run(['vlc', '-autoexit', f['url']])