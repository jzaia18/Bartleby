# Butler Gnome
# BrickHack 9
# Module for google cloud speech to text

import speech_recognition as sr
from scipy.io.wavfile import write
import sounddevice as sd
from time import sleep
import wavio as wv


def recordAudio():
    fs = 44100  # Sample rate
    seconds = 6  # Duration of recording
    print('recording!')
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    print('finished')
    write('output.wav', fs, myrecording)  # Save as WAV file
    wv.write("recording1.wav", myrecording, fs, sampwidth=4)
    sleep(1)


# Reading Audio file as source
# listening the audio file and store in audio_text variable
def wavToText():
    # Initialize the recognizer
    r = sr.Recognizer()
    with sr.AudioFile('recording1.wav') as source:
        audio_text = r.listen(source)
        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:
            # using google speech recognition
            print('Moving to audio text')
            text = r.recognize_google(audio_text)
            print('Converting audio transcripts into text ...')
            print(text)
            if text == '':
                print('nothing')
        except:
            print('Sorry.. run again...')
            print("unknown error occurred")


if __name__ == '__main__':
    recordAudio()
    wavToText()
