# Butler Gnome
# BrickHack 9
# Module for google cloud speech to text

import speech_recognition as sr
from scipy.io.wavfile import write
import sounddevice as sd
from time import sleep
import wavio as wv


# For testing
def record_audio(verbose=False):
    fs = 44100  # Sample rate
    seconds = 6  # Duration of recording
    if verbose:
        print('recording!')
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    if verbose:
        print('finished')
    write('output.wav', fs, myrecording)  # Save as WAV file
    wv.write("recording1.wav", myrecording, fs, sampwidth=4)
    sleep(1)


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
    record_audio(verbose=True)
    print(convert_wav_to_text(verbose=True))
