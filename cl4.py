import socket
import pyaudio
import threading

# Audio configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def receive_audio(sock, p):
    # Open a stream for audio playback.
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
    while True:
        try:
            data = sock.recv(CHUNK)
            if not data:
                break
            stream.write(data)
        except Exception as e:
            print("Error receiving audio:", e)
            break
    stream.stop_stream()
    stream.close()

def send_audio(sock, p):
    # Open a stream for audio capture.
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    while True:
        try:
            data = stream.read(CHUNK)
            sock.sendall(data)
        except Exception as e:
            print("Error sending audio:", e)
            break
    stream.stop_stream()
    stream.close()

def main():
    host = "192.168.8.101"  # Change this to your server's IP address
    port = 50007
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print("Connected to voice chat server.")

    p = pyaudio.PyAudio()

    # Start threads for receiving and sending audio.
    receive_thread = threading.Thread(target=receive_audio, args=(sock, p))
    send_thread = threading.Thread(target=send_audio, args=(sock, p))
    receive_thread.start()
    send_thread.start()

if __name__ == "__main__":
    main()
