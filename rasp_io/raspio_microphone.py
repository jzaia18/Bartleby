import serial
import argparse
import wave

def write_serial(name, target):
    try: 
        serial_port = serial.Serial(name, 9600)
        print("The Port name is" + serial_port.name)
        while True:
            
            vals = serial_port.readline()
            
            print(str(vals))
            
            target.writeframes(vals)
             
    except:
        target.close()
        print("No Response from Port")
        exit()

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--port", required=True, help = "Enter name of serial port to monitor")
args = vars(ap.parse_args())

PORT = args['port']

wav = wave.open("test.wav", "wb")
wav.setnchannels(1)
wav.setsampwidth(3)
wav.setframerate(44100)

write_serial(PORT, wav)