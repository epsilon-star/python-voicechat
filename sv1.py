import socket
import threading
import pyaudio
import random

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

roles = {
    "n":0,
    "a":10,
    "x":20,
    "z":30,
    "q":40,
}
channes = {}
channel_template = {
    "id":"1234",
    "Name":"Public Channel",
    "password":"1234",
    "role":"a",
    "users": ["conn","id","role"]
}

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

    while True:
        data = conn.recv(CHUNK)
        if not data:
            break
        stream.write(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    conn.close()
    print(f"[DISCONNECTED] {addr} disconnected.")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()
    print("[LISTENING] Server is listening on localhost:5000")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

def main():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('localhost',5000))
    server.listen()
    print("[SERVER] Server is listening on localhost:5000")

    clients = {}
    threads = {}

    def serial(length) -> str:
        hashs = 'abcdefghijklmnopqrstuvwxyz'.upper()
        return ''.join([hashs[random.randint(0,len(hashs)-1)] for x in range(length)])

    def newClient():
        mps = False
        while not mps:
            buff = serial(10)
            if buff not in list(clients.values()): mps = True
        return buff
    
    def handleClient(conn,addr):
        idx = newClient()
        clients[idx] = {
            "conn":conn,
            "addr":addr,
            "channel":None,
            "role":"n",
            "speaker":False,
            "mic":False
        }
        while True:
            try: 
                data = conn.recv(CHUNK)
                if data:
                    conn.send(bytes(f"Welcome To epsilon-voicechat, ID: [{idx}]"))
            except: conn.close()

    while True:
        conn,addr = server.accept()
        buff = newClient()
        threads = threading.Thread(target=handleClient,args=(conn,addr))
        

if __name__ == "__main__":
    # start_server()
    main()