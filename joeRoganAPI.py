# Butler Gnome
# BrickHack 9
# API caller for eleven labs to make chatgpt into a normal voice.

import requests
from pygame import mixer
from time import sleep

url = 'https://api.elevenlabs.io/v1/text-to-speech/sIA6m5lChGWOhQao1cw5'
headers = {'accept': 'audio/mpeg', 'xi-api-key': '4f5b1bd5f2b4a6d931c7eaeb158734cc', 'Content-Type': 'application/json'}
text = "I have unlimited power. Seriously, bro. It's because of my gnomish muscle workout routine."
data = {
    "text": text,
    "voice_settings": {"stability": 0.75, "similarity_boost": 0.75}
  }

r = requests.post(url,headers=headers, json=data)

print("Status Code", r.status_code)
with open('movie.mp3', 'wb') as f:
    f.write(r.content)

mixer.init()
mixer.music.load("movie.mp3")
mixer.music.play()
while mixer.music.get_busy():  # wait for music to finish playing
    sleep(1)

