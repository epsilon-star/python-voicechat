# import pyaudio
# import wave


# audio = pyaudio.PyAudio()

# stream = audio.open(format=pyaudio.paInt16,channels=1,rate=44100,input=True,frames_per_buffer=1024)

# frames = []

# try:
#     while True:
#         data = stream.read(1014)
#         frames.append(data)
# except KeyboardInterrupt: pass

# stream.stop_stream()
# stream.close()
# audio.terminate()


# fs = wave.open("recording_002.wav","wb")
# fs.setnchannels(1)
# fs.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
# fs.setframerate(44100)
# fs.writeframes(b''.join(frames))

from scapy.all import ARP, Ether, srp

def scan_network():
    # Create an ARP request packet
    arp = ARP(pdst="192.168.1.0/24")
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    # Send the packet and receive responses
    result = srp(packet, timeout=2, verbose=0)[0]

    # Extract active IPs
    active_ips = [received.psrc for sent, received in result]
    return active_ips

# Example usage
active_ips = scan_network()
print("Active IPs:", active_ips)