import os
import socket
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("Connected to server. Start speaking...")

    while True:
        data = stream.read(CHUNK)
        client_socket.send(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    client_socket.close()

commands = [
    "help",
    "connect",
    "disconnect",
    "channel",
    "list",
]
data = {
    "conn":"",
    "id":"",
    "role":"",
    "channel":0,
}

def main():
    while True:
        inp = input("> ")
        command,args = '',''
        try: command,args = inp.split(" ")[0],inp.split(" ")[1:]
        except: command = inp
        finally: print(inp,"|",command,"|",args)
        
        if not command in commands:
            print("<Error> Command Not Found Or Not Registered !")
        
        if command == "help":
            print("write help <command> to see the command help")
            for x in commands:
                print(f"    {x.upper()}")
        elif command == 'clear': os.system('cls')
        elif command == 'cls': os.system('cls')
        elif command == 'connect':
            if not len(args): print("use connect <server> <port>")
            elif len(args) < 2: print("use connect <server> <port> | fill options")
            else: 
                data['conn'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                data['conn'].connect(('localhost',5000))

        elif command == 'ulist':
            if not data['conn']: print("no connection found")
            else:

                

if __name__ == "__main__":
    # start_client()
    main()