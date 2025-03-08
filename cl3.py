import socket
import pyaudio
import threading

# Audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 32000
CHUNK = 1024

# Server settings
HOST = "192.168.8.101"  # Replace with the server's IP
PORT = 58410

def send_audio(client_socket, stream):
    """Send audio data from the microphone to the server."""
    try:
        while True:
            data = stream.read(CHUNK)
            client_socket.send(data)
    except Exception as e:
        print(f"Send error: {e}")

def receive_audio(client_socket, stream):
    """Receive audio data from the server and play it."""
    try:
        while True:
            data = client_socket.recv(CHUNK)
            if data:
                stream.write(data)
    except Exception as e:
        print(f"Receive error: {e}")

def start_client():
    """Connect to the server and start sending/receiving audio."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK)

    print("Connected to server. Start speaking...")

    # Start send and receive threads
    send_thread = threading.Thread(target=send_audio, args=(client_socket, stream))
    receive_thread = threading.Thread(target=receive_audio, args=(client_socket, stream))

    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.join()

    stream.stop_stream()
    stream.close()
    p.terminate()
    client_socket.close()

if __name__ == "__main__":
    start_client()