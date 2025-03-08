# import os
# import socket
# import pyaudio

# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 32000
# CHUNK = 1024

# IP = "192.168.8.101"
# PORT = 58410

# def start_client():
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect((IP,PORT))

#     p = pyaudio.PyAudio()
#     stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK)

#     print("Connected to server. Start speaking...")

#     while True:
#         data = stream.read(CHUNK)
#         client_socket.send(data)
#         data = client_socket.recv(CHUNK)
#         if not data:
#             pass
#         else:
#             stream.write(data)

#     stream.stop_stream()
#     stream.close()
#     p.terminate()
#     client_socket.close()

# if __name__ == "__main__":
#     start_client()

# import os
# import socket
# import pyaudio
# import asyncio

# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 32000
# CHUNK = 1024

# IP = "192.168.8.101"
# PORT = 58410

# async def send_audio(client_socket, stream):
#     while True:
#         data = await stream.read(CHUNK)
#         client_socket.send(data)
#         # await asyncio.sleep(0)  # Yield control to the event loop

# async def receive_audio(client_socket, stream):
#     while True:
#         data = await client_socket.recv(CHUNK)
#         if data:
#             stream.write(data)
#         # await asyncio.sleep(0)  # Yield control to the event loop

# async def start_client():
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect((IP, PORT))

#     p = pyaudio.PyAudio()
#     stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK)

#     print("Connected to server. Start speaking...")

#     # Run send and receive tasks concurrently
#     send_task = asyncio.create_task(send_audio(client_socket, stream))
#     receive_task = asyncio.create_task(receive_audio(client_socket, stream))

#     await asyncio.gather(send_task, receive_task)

#     stream.stop_stream()
#     stream.close()
#     p.terminate()
#     client_socket.close()

# if __name__ == "__main__":
#     asyncio.run(start_client())

import os
import asyncio
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 32000
CHUNK = 1024

IP = "192.168.8.101"
PORT = 58410

# async def send_audio(writer, stream):
#     try:
#         while True:
#             data = stream.read(CHUNK)
#             writer.write(data)
#             await writer.drain()  # Ensure data is sent
#             # await asyncio.sleep(0)  # Yield control to the event loop
#     except Exception as e:
#         print(f"Send error: {e}")

# async def receive_audio(reader, stream):
#     try:
#         while True:
#             data = await reader.read(CHUNK)  # Non-blocking read
#             if data:
#                 stream.write(data)
#             # await asyncio.sleep(0)  # Yield control to the event loop
#     except Exception as e:
#         print(f"Receive error: {e}")

# async def start_client():
#     # Connect to the server
#     reader, writer = await asyncio.open_connection(IP, PORT)

#     # Initialize PyAudio
#     p = pyaudio.PyAudio()
#     stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK)

#     print("Connected to server. Start speaking...")

#     # Run send and receive tasks concurrently
#     send_task = asyncio.create_task(send_audio(writer, stream))
#     receive_task = asyncio.create_task(receive_audio(reader, stream))

#     await asyncio.gather(send_task, receive_task)

#     # Cleanup
#     stream.stop_stream()
#     stream.close()
#     p.terminate()
#     writer.close()
#     await writer.wait_closed()

async def main():

    async def clrecv(conn): 
        while True:
            datas = await conn.recv(CHUNK)
            if datas: stream.
    async def clsend(conn):
        while True:
            data = stream.read(CHUNK)
            if data: await conn.send(data)

if __name__ == "__main__":
    asyncio.run(start_client())

