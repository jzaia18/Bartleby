# Butler Gnome
# BrickHack 9
# API caller for eleven labs to make chatgpt into a normal voice.

import requests
from time import sleep
from subprocess import Popen, DEVNULL

API_KEY_LOCATION = 'joerogansecrets.txt'
with open(API_KEY_LOCATION) as f:
    API_KEY = f.read().strip()

def get_tts(text, response_loc='response.mp3'):
    url = 'https://api.elevenlabs.io/v1/text-to-speech/t1u89Py5jDQcxymSnrch'
    headers = {'accept': 'audio/mpeg', 'xi-api-key': API_KEY, 'Content-Type': 'application/json'}
    data = {
        "text": text,
        "voice_settings": {"stability": 0.75, "similarity_boost": 0.75}
    }

    r = requests.post(url,headers=headers, json=data)

    print("Status Code", r.status_code)
    with open(response_loc, 'wb') as f:
        f.write(r.content)

def play_tts(fname='response.mp3'):
    return Popen(["cvlc", "--play-and-exit", fname], stdout=DEVNULL, stderr=DEVNULL)


def wait_tts(tts_obj):
    while tts_obj.poll() is None:
        sleep(1)

if __name__ == '__main__':
    get_tts(input())

