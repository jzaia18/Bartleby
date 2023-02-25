from voice import *
from makeresponse import get_gpt_response_text

if __name__ == '__main__':
    text = convert_wav_to_text()
    print('Q:',text)

    response = get_gpt_response_text(text)
    print('A:', response)
