from voice import *
from tts import *
from makeresponse import get_moderated_text
import os, random
from weather import forecastFromLocation, getDetails, getTemp, getPrecipChance, getWindSpeed
import re
from datetime import datetime

WEATHER_PATTERN = re.compile(
r'\b(?:weather|temperature)\b(?:.+\bin ((?:\W*\b(?!right|now)\w+\b){1,3}\b))?', re.I)
TIME_PATTERN = re.compile(r'^(:?can|what|tell me)\b.*\btime\b(?!.*\bdo)', re.I)


def get_random_voice(directory='audiofiles/stalling_messages'):
    return directory + '/' + random.choice(os.listdir(directory))

if __name__ == '__main__':
    # text = convert_wav_to_text()
    # print('Q:',text)

    context = ""
    text = input("> ")
    stallFile = get_random_voice('../audiofiles/stalling_messages')
    
    if (match := re.search(WEATHER_PATTERN, text)):
        forecastObj = forecastFromLocation((match.group(1) or 'Rochester, NY').strip())
        
        if forecastObj is None:
            wait_tts(play_tts('../audiofiles/weather_messages/unsure.mp3'))
            exit()
        else:
            details = getDetails(forecastObj)
            context = 'Restate with precise numbers: "' + details + '"'
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
        context = "Restate with strong idioms: \"It is currently " + \
            datetime.now().strftime('%I:%M %p') + '"'
        # context = "Rephrase the following using strong idioms: It is currently " + \
        #     datetime.now().strftime('%I:%M %p')

    elif 'joke' in text.lower() and 'about' not in text.lower():
        wait_tts(play_tts(get_random_voice('../audiofiles/jokes')))
        exit()

    elif 'news' in text.lower():
        wait_tts(play_tts(get_random_voice('../audiofiles/news_messages')))
        exit()
        
        
        # text = "Comment strongly about the current time of day."

    print(context)
    
    stalling = play_tts(stallFile)
    
    response = get_moderated_text(text, context=context)
    if response == None:
        print('Canceled!')
        
        
        wait_tts(stalling)
        
        wait_tts(play_tts(get_random_voice('../audiofiles/canceled_messages')))
        
        exit()
    

    get_tts(response)
    
    wait_tts(stalling)
    
    print(response)
    response = response.replace(" mph", " miles per hour")
    response = response.replace("°", " degrees")
    wait_tts(play_tts())
    
    # mixer.music.load('response.mp3')
    # mixer.music.play()
    # while mixer.music.get_busy():  # wait for music to finish playing
    #     sleep(1)
