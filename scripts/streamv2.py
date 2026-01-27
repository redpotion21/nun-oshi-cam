from flask import Flask, send_from_directory
import subprocess
import os
import threading
import streamlink
import os

def get_stream_url():
    session = streamlink.Streamlink()
    streams = session.streams(youtube_url)
    if "best" in streams:
        return streams["best"].url
    return None

app = Flask(__name__)

youtube_url = "https://www.youtube.com/live/8aA0pTwqQd4?si=Fq665imPhRiKffED"

# Your crop settings
CROP = "crop=318:479:1400:600"  # width:height:x:y   ← change!!
INPUT_URL = get_stream_url()#'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8' # paste from streamlink or yt-dlp -g

HLS_DIR = "/scripts/hls"
os.makedirs(HLS_DIR, exist_ok=True)



def start_ffmpeg():
    cmd = [
        "ffmpeg",
        "-reconnect", "1",
        "-reconnect_streamed", "1",
        "-reconnect_delay_max", "5",
        "-i", INPUT_URL,
        "-vf", CROP,
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "28",
        "-an",  # no audio for test (remove if you want sound)
        "-f", "hls",
        "-hls_time", "2",
        "-hls_init_time", "1",
        "-hls_list_size", "3",
        "-hls_flags", "delete_segments+omit_endlist",
        "-hls_segment_filename", f"{HLS_DIR}/segment_%03d.ts",
        f"{HLS_DIR}/playlist.m3u8"
    ]
    subprocess.Popen(cmd)  # no DEVNULL for now → see output in console!
    print("ffmpeg launched~ wait 10-20 sec nya")

@app.route('/scripts/hls/<path:filename>')
def serve_hls(filename):
    return send_from_directory(HLS_DIR, filename)

@app.route('/')
def index():
    return '''
    <html>
      <head><title>crop</title></head>
      <body style="margin:0;background:black;">
        <video width="318" height="479" autoplay muted loop playsinline controls>
          <source src="/hls/playlist.m3u8" type="application/x-mpegURL">
          Your browser does not support the video tag.
        </video>
      </body>
    </html>
    '''

if __name__ == '__main__':
    import time
    #time.sleep(10)  # give ffmpeg time to create playlist
    #print("hls files now:", os.listdir(HLS_DIR))
    threading.Thread(target=start_ffmpeg, daemon=True).start()
    app.run(host='127.0.0.1', port=5000, threaded=True)