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

if __name__ == "__main__":
    start_client()