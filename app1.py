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


import socket

def scan_network(port):
    active_servers = []
    base_ip = "192.168"  # Adjust based on your network
    for x in range(1,255):
        for i in range(1, 255):  # Scan all IPs in the range
            ip = f"{base_ip}.{x}.{i}"
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.001)  # Reduce timeout for faster scanning
                result = sock.connect_ex((ip, port))
                print(ip,port,result)
                if result == 0:
                    active_servers.append(ip)
                sock.close()
            except Exception as e:
                print(f"Error scanning {ip}: {e}")
    return active_servers

# Example usage
port = 58410  # Port your server is running on
servers = scan_network(port)
# print("Active servers:", servers)