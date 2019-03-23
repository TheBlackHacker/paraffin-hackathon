import speech_recognition as sr  # import the library
import requests
from gtts import gTTS 
import os
import json

while (1):
    r = sr.Recognizer()  # initialize recognizer
    with sr.Microphone() as source:  # mention source it will be either Microphone or audio files.
        print("Speak :")
        audio = r.listen(source)  # listen to the source
        try:
            text = r.recognize_google(audio)  # use recognizer to convert our audio into text part.
            print ('abc')
            print (text)
            while (text == 'hello'):
                mytext = 'Welcome to paraffin '
                language = 'en'
                myobj = gTTS(text=mytext, lang=language, slow=False)
                myobj.save("welcomez.mp3")
                os.system("welcomez.mp3")
                while (1):
                    r = sr.Recognizer()  # initialize recognizer
                    with sr.Microphone() as source:
                        print("Speak Anything :")
                        audio = r.listen(source)  # listen to the source
                        try:
                            text = r.recognize_google(audio)
                            print (text)
                            if text == 'bye-bye':
                                mytext = 'see you again '
                                language = 'en'
                                myobj = gTTS(text=mytext, lang=language, slow=False)
                                myobj.save("welcomez.mp3")
                                os.system("welcomez.mp3")
                                break
                            r = requests.get(
                                'http://sandbox.api.simsimi.com/request.p?key=f6619cf1-5d34-4532-b4f9-c3f9ce6f914d&lc=en&ft=1.0&text=' + text)
                            json_text = r.json()

                            print(json_text["response"])
                            language = 'en'

                            # Passing the text and language to the engine,
                            # here we have marked slow=False. Which tells
                            # the module that the converted audio should
                            # have a high speed
                            myobj = gTTS(text=json_text["response"], lang=language, slow=False)

                            # Saving the converted audio in a mp3 file named
                            # welcome
                            myobj.save("welcome.mp3")

                            # Playing the converted file
                            os.system("welcome.mp3")
                        except:
                            mytext = 'Sorry could not recognize your voice '
                            language = 'en'
                            myobj = gTTS(text=mytext, lang=language, slow=False)
                            myobj.save("welcomez.mp3")
                            os.system("welcomez.mp3")
        except:
            mytext = 'Sorry could not recognize your voice '

            # Language in which you want to convert
            language = 'en'

            # Passing the text and language to the engine,
            # here we have marked slow=False. Which tells
            # the module that the converted audio should
            # have a high speed
            myobj = gTTS(text=mytext, lang=language, slow=False)

            # Saving the converted audio in a mp3 file named
            # welcome
            myobj.save("welcomez.mp3")

            # Playing the converted file
            os.system("welcomez.mp3")

