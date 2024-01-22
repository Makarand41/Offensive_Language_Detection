import categorize as cg
import pyttsx3 as spk
import speech_recognition as sr
from pydub import AudioSegment
from math import ceil

def mp3_to_wav(audio_file_path):
    sound = AudioSegment.from_file(audio_file_path)
    audio_file_path = 'audio/sample.wav'
    sound.export(audio_file_path, format="wav")
    return audio_file_path, ceil(sound.duration_seconds)

while True:
    try:
        print('--------------------------------Menu--------------------------------\n')
        print('1. Type your comment.\n2. Make a verbal comment.\n3. Upload the saved audio file.\n')
        print('--------------------------------------------------------------------\n')
        num = input('Enter your choice: ')
        if num == '1':
            comment = input('Enter your comment: ')
        elif num == '2':
            cnt = 0
            while True:
                if cnt == 3:
                    spk.speak("We are unable to recognize your voice due to following possible reasons")
                    print("\nReasons for Failure may include: \n1. Low Internet Connection.\n 2. Issue with microphone (Hardware/Software).\n3. Too much noise.")
                    spk.speak("1..Low Internet Connection.......2..Issue with microphone..Hardware or Software.....3..Too much noise.")
                    break
                spk.speak("Start speaking at the count of 3: ")
                spk.speak("1...........2 and ...........3")
                try:
                    r = sr.Recognizer()
                    mic = sr.Microphone()
                    with mic as source:
                        r.adjust_for_ambient_noise(source)
                        audio = r.listen(source)
                    comment = r.recognize_google(audio)
                    break
                except:
                    spk.speak("Can you please repeat it again...")
                    cnt += 1
        elif num == '3':
            path, ttl = mp3_to_wav(input("Enter the path to your audio file: "))
            r = sr.Recognizer()
            try:
                with sr.AudioFile(path) as source:
                    audio_listened = r.record(source)
                    comment = r.recognize_google(audio_listened)
            except:
                comment = '000000000000000000000000000'
        else:
            closures = ['close', 'exit', 'stop', '0','escape', 'esc', 'break']
            if(num.lower() in closures):
                break
            else:
                print("Enter the valid key!")

        print("\nYour Comment: " + comment)
        print('Comment you made is ' + cg.categorize(comment), end='\n')
    except:
        print('Something went wrong!')
print('Analysis complete....')