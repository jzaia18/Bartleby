from voice import *
from tts import *
from makeresponse import get_moderated_text
import os, random
from weather import forecastFromLocation
import re

WEATHER_PATTERN = re.compile(r'\bweather\b(?:.+\bin (.+))?')

def get_stall_text(directory='audiofiles/stalling_messages'):
    return directory + '/' + random.choice(os.listdir(directory))

if __name__ == '__main__':
    # text = convert_wav_to_text()
    # print('Q:',text)

    preface = ""
    text = input("> ")
    
    if (match := re.search(WEATHER_PATTERN, text)):
        preface = "Current forecast: " + forecastFromLocation(match.group(1) or 'Rochester, NY')
        text = "Tell me about the weather"
        print("Weather forecast:", repr(preface))
    

    response = get_moderated_text(text)
    if response == None:
        print('Canceled!')
        
        wait_tts(play_tts(get_stall_text('../audiofiles/canceled_messages')))
        
        exit()
    
    print(response)
    
    stalling = play_tts(get_stall_text('../audiofiles/stalling_messages'))

    get_tts(response)
    
    wait_tts(stalling)
    
    wait_tts(play_tts())
    
    # mixer.music.load('response.mp3')
    # mixer.music.play()
    # while mixer.music.get_busy():  # wait for music to finish playing
    #     sleep(1)
