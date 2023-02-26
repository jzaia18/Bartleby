from voice import *
from tts import *
from makeresponse import get_gpt_response_text
from pygame import mixer
import os, random
from weather import forecastFromLocation
import re

WEATHER_PATTERN = re.compile(r'\bweather\b(?:.+\bin (.+))?')

def get_stall_text(directory='audiofiles/stalling_messages'):
    return directory + '/' + random.choice(os.listdir(directory))

if __name__ == '__main__':
    mixer.init()
    # text = convert_wav_to_text()
    # print('Q:',text)

    text = input()
    
    if (match := re.search(WEATHER_PATTERN, text)):
        text = forecastFromLocation(match.group(1) or 'Rochester, NY')
        print("Weather forecast:", repr(text))

    response = get_gpt_response_text(text)
    play_tts(get_stall_text('audiofiles/stalling_messages'))
    print('A:', response)

    get_tts(response)
    while mixer.music.get_busy():  # wait for music to finish playing
        sleep(1)

    play_tts()
    while mixer.music.get_busy():  # wait for music to finish playing
        sleep(1)
    
    # mixer.music.load('response.mp3')
    # mixer.music.play()
    # while mixer.music.get_busy():  # wait for music to finish playing
    #     sleep(1)
