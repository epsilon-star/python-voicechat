# import speech_recognition as sr

# recognizer = sr.Recognizer()

# with sr.Microphone() as source:
#     print("Please Speak Something ...")
#     audio = recognizer.listen(source)

#     print(type(audio),id(audio),audio)

# import os
# import time
# import playsound
# import speech_recognition as sr
# from gtts import gTTS


# def speak(text):
#     tts = gTTS(text=text, lang="en")
#     # filename = "voice.mp3"
#     # tts.save(filename)
#     playsound.playsound(tts)


# def get_audio():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         audio = r.listen(source)
#         said = ""

#         try:
#             said = r.recognize_google(audio)
#             print(said)
#         except Exception as e: pass
#             # print("Exception: " + str(e))

#     return said

# while True:
#     text = get_audio()
#     if text and len(text):
#         speak(text)
#     else: pass

# if "hello" in text:
#     speak("hello, how are you?")
# elif "what is your name" in text:
#     speak("My name is Tim")