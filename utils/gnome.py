from voice import *
from tts import *
from makeresponse import get_gpt_response_text
from pygame import mixer

if __name__ == '__main__':
    mixer.init()
    # text = convert_wav_to_text()
    # print('Q:',text)

    text = input()

    response = get_gpt_response_text(text)
    print('A:', response)

    get_tts(response)
    play_tts()
    # mixer.music.load('response.mp3')
    # mixer.music.play()
    # while mixer.music.get_busy():  # wait for music to finish playing
    #     sleep(1)
