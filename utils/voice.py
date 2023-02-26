# Butler Gnome
# BrickHack 9
# Module for google cloud speech to text

import speech_recognition as sr
from scipy.io.wavfile import write
import sounddevice as sd
from time import sleep
import wavio as wv

FS = 44100

# For testing
def record_audio(duration, verbose=False):
    fs = FS  # Sample rate
    seconds = duration  # Duration of recording
    if verbose:
        print('recording!')
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    if verbose:
        print('finished')
    #write('output.wav', fs, myrecording)  # Save as WAV file
    wv.write("recording1.wav", myrecording, fs, sampwidth=4)
    sleep(1)


def wait_for_wake(wakeWords, duration, verbose=False):
    fs = FS
    if verbose:
        print("Waiting for Wake")
    
    recordingCache = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    wv.write("recordingCache.wav", recordingCache, fs, sampwidth=4)
    response = convert_wav_to_text(fname="recordingCache.wav")
    
    if(response):
        for word in response.split(" "):
            print(word)
            if word in wakeWords:
                if(verbose):
                    print("wake word found!")
                return 0
    
    return 1


# Reading Audio file as source
# listening the audio file and store in audio_text variable
def convert_wav_to_text(fname='recording1.wav', verbose=False):
    # Initialize the recognizer
    r = sr.Recognizer()
    with sr.AudioFile(fname) as source:
        audio_text = r.listen(source)
        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:
            # using google speech recognition
            if verbose:
                print('Moving to audio text')
            text = r.recognize_google(audio_text)
            if verbose:
                print('Converting audio transcripts into text ...')
            return text or 'no response'
        except:
            if verbose:
                print('Sorry.. run again...')
            print("unknown error occurred")


if __name__ == '__main__':
    wakeWords = ["bartleby", "hey", "servant"]

    while(True):
        if(wait_for_wake(wakeWords, 3, verbose=True) == 0):
            record_audio(15, verbose=True)
            print(convert_wav_to_text(verbose=True))
        else:
            sleep(.1)
