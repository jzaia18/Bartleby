# Butler Gnome
# BrickHack 9
# Module for google cloud speech to text

import speech_recognition as sr
#from scipy.io.wavfile import write
import sounddevice as sd
from time import sleep
import wavio as wv
import concurrent.futures

FS = 44100
# Initialize the recognizer
r = sr.Recognizer()


# For testing
def record_audio(duration, verbose=False):
    seconds = duration  # Duration of recording
    if verbose:
        print('recording!')
    myrecording = sd.rec(int(seconds * FS), samplerate=FS, channels=2)
    sd.wait()  # Wait until recording is finished
    if verbose:
        print('finished')
    #write('output.wav', FS, myrecording)  # Save as WAV file
    wv.write("recording1.wav", myrecording, FS, sampwidth=4)
    sleep(1)


def wait_for_wake(wakeWords, duration, recordingCache, verbose=False):
    if verbose:
        print("Waiting for Wake")

    if recordingCache:
        recordingCache.append(sd.rec(int(duration * FS), samplerate=FS, channels=2))
    else: 
        recordingCache = sd.rec(int(duration * FS), samplerate=FS, channels=2)

    sd.wait()
    wv.write("recordingCache.wav", recordingCache, FS, sampwidth=4)
    
    if len(recordingCache > 10*FS*duration):
        recordingCache = recordingCache[FS*duration:]

    response = convert_wav_to_text(fname="recordingCache.wav")
    
    if(response):
        response = response.split(" ")
        for i, word in enumerate(response):
            print(word)
            if word in wakeWords:
                if(verbose):
                    print("wake word found!")
                return 0, " ".join(response[i:])
    
    return 1, recordingCache


# Reading Audio file as source
# listening the audio file and store in audio_text variable
def convert_wav_to_text(fname='recording1.wav', verbose=False):
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
    wakeWords = ["bartleby", "hey", "servant", "listen"]
    recordingCache = []

    while(True):
        result, recordingCache = wait_for_wake(wakeWords, 1, recordingCache)
        if(result == 0):
            record_audio(8)
            print(recordingCache + " " + convert_wav_to_text())
            recordingCache = []
     
