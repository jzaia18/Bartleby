from voice import *
from tts import *
from makeresponse import get_moderated_text
import os, random
from weather import forecastFromLocation, getDetails, getTemp, getPrecipChance, getWindSpeed
import re
from datetime import datetime

WEATHER_PATTERN = re.compile(
r'\b(?:weather|temperature)\b(?:.+\bin ((?:\W*\b(?!right|now)\w+\b){1,2}\b))?', re.I)
TIME_PATTERN = re.compile(r'\b(:?what|tell me)\b.*\btime\b', re.I)


def get_stall_text(directory='audiofiles/stalling_messages'):
    return directory + '/' + random.choice(os.listdir(directory))

if __name__ == '__main__':
    # text = convert_wav_to_text()
    # print('Q:',text)

    context = ""
    text = input("> ")
    stallFile = get_stall_text('../audiofiles/stalling_messages')
    
    if (match := re.search(WEATHER_PATTERN, text)):
        forecastObj = forecastFromLocation((match.group(1) or 'Rochester, NY').strip())
        
        if forecastObj is None:
            stallFile = 'unsure'
            context = "Do not respond."
        else:
            details = getDetails(forecastObj)
            context = "Exaggerate the following, with specific numbers: " + details
            # text = "Comment strongly about the weather."
            
            if getPrecipChance(forecastObj) >= 90:
                if getTemp(forecastObj) <= 32:
                    stallFile = 'snow'
                else:
                    stallFile = 'rain'
            elif getWindSpeed(forecastObj) >= 30:
                stallFile = 'wind'
            else:
                tmp = getTemp(forecastObj)
                if tmp >= 80:
                    stallFile = 'hot'
                elif tmp <= 32:
                    stallFile = 'cold'
                else:
                    stallFile = 'average'
            
        stallFile = '../audiofiles/weather_messages/%s.mp3' % stallFile
        
        
    elif (match := re.search(TIME_PATTERN, text)):
        context = "Rephrase the following using strong idioms: It is currently " + \
            datetime.now().strftime('%I:%M %p')
        
        
        # text = "Comment strongly about the current time of day."

    print(context)
    
    response = get_moderated_text(text, context=context)
    if response == None:
        print('Canceled!')
        
        wait_tts(play_tts(get_stall_text('../audiofiles/canceled_messages')))
        
        exit()
    
    print(response)
    
    response = response.replace(" mph", " miles per hour")
    
    stalling = play_tts(stallFile)

    get_tts(response)
    
    wait_tts(stalling)
    
    wait_tts(play_tts())
    
    # mixer.music.load('response.mp3')
    # mixer.music.play()
    # while mixer.music.get_busy():  # wait for music to finish playing
    #     sleep(1)
