import pyaudio
from time import sleep
import os
import keyboard
import numpy as np  

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 28000
CHUNK = 512

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK)

table = {
    1:"B",
    3:"KB",
    6:"MB",
    9:"GB",
    12:"TB",
}

def gvolume(data):
    """Calculate stable RMS volume in dB."""
    samples = np.frombuffer(data, dtype=np.int16)
    if len(samples) == 0:
        return -100  # Treat silence as very low dB

    rms = np.sqrt(np.mean(np.square(samples)))  # Correct RMS calculation
    
    # Convert RMS to decibels (dB) for better sensitivity control
    if rms > 0:
        volume_db = 20 * np.log10(rms)  
    else:
        volume_db = -100  # Consider anything zero as silent

    return volume_db

def cacls(value: float):
    """Convert byte size into human-readable format (B, KB, MB, etc.)."""
    mps = list(table.keys())
    for x in range(len(mps)-1, -1, -1):
        if (value / (10**mps[x])) > 1:
            return f"{(value / (10**mps[x])):.02f} {table[mps[x]]}"
    return f"{value} B"

total = 0
mictype = 1  # 0 = Always Open, 1 = Push to Talk, 2 = Volume Gate
volume_threshold = 38  # Set a threshold for activation
push_key = 'z'

mpd = 8
mpa = mpd

while True:
    try:
        data = stream.read(CHUNK, exception_on_overflow=False)

        if mictype == 0:  # Always on
            stream.write(data)
            total += len(data)

        elif mictype == 1:  # Push to talk 
            if keyboard.is_pressed(push_key):
                stream.write(data)
                total += len(data)

        elif mictype == 2:  # Volume-gated activation
            volume = gvolume(data)
            if volume >= volume_threshold:  # Use threshold variable
                stream.write(data)
                total += len(data)

        else:
            pass

        # Display updates every few iterations
        mpa -= 1
        if mpa <= 0: 
            mpa = mpd
            os.system("cls" if os.name == "nt" else "clear")  # Windows/Linux support
            print(f"Mic Mode: {mictype} | Volume Gate: {volume_threshold}")
            print(f"Volume : {volume:.02f}")
            print(f"Total Read/Write : {cacls(total)}")

    except KeyboardInterrupt:
        print("\nStopping...")
        break

stream.stop_stream()
stream.close()
audio.terminate()
