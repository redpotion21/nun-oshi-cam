import cv2
import streamlink

url = "https://www.youtube.com/live/pmlucNPuIGw?si=4dm7lDHWxcUt_hdy"  # your link

session = streamlink.Streamlink()
streams = session.streams(url)
best = streams["best"]
stream_url = best.url

cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)

# Add reconnect magic for YouTube live
import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "reconnect;1|reconnect_streamed;1|timeout;60000000"

if not cap.isOpened():
    print("Can't open stream...")
    exit()

# Get original size once
ret, frame = cap.read()
if ret:
    h, w = frame.shape[:2]
    print(f"Stream size: {w}x{h}")
else:
    print("First frame failed...")
    exit()

# Decide crop region (change these numbers!!)
# Example: center 640x360 from 1920x1080 stream
x = 1200    # start x
y = 600     # start y
crop_w = 400   
crop_h = 480

print(f"Cropping: {crop_w}x{crop_h} from {x},{y}")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Stream ended or dropped...")
        break
    
    # Crop the region!!
    cropped = frame[y:y+crop_h, x:x+crop_w]
    
    # Show only cropped part
    cv2.imshow("Live screen", cropped)
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()

