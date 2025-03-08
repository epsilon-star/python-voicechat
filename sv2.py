# import socket
# import threading
# # import pyaudio
# import random
# import asyncio

# # FORMAT = pyaudio.paInt16
# # CHANNELS = 1
# # RATE = 44100
# CHUNK = 1024

# IP = "0.0.0.0"
# PORT = 58410

# conns = []

# def handle_client(conn, addr):
#     print(f"[NEW CONNECTION] {addr} connected.")

#     # p = pyaudio.PyAudio()
#     # stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

#     while True:
#         data = conn.recv(CHUNK)
#         if not data:
#             pass
#         else:
#             for x in conns:
#                 if x != conn:
#                     x.send(data)
#         # stream.write(data)

#     # stream.stop_stream()
#     # stream.close()
#     # p.terminate()
#     # conn.close()
#     print(f"[DISCONNECTED] {addr} disconnected.")

# def start_server():
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind((IP, PORT))
#     server_socket.listen()
#     print(f"[LISTENING] Server is listening on {IP}:{PORT}")

#     while True:
#         conn, addr = server_socket.accept()
#         if not conn in conns: conns.append(conn)
#         thread = threading.Thread(target=handle_client, args=(conn, addr))
#         thread.start()

# start_server()


import asyncio
import socket
import threading

CHUNK = 1024

IP = "0.0.0.0"
PORT = 58410

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"[NEW CONNECTION] {addr} connected.")

    try:
        while True:
            data = await reader.read(CHUNK)  # Non-blocking read
            if not data:
                break
            for client_writer in clients:
                if client_writer != writer:
                    client_writer.write(data)
                    await client_writer.drain()  # Ensure data is sent
    except Exception as e:
        print(f"Error with {addr}: {e}")
    finally:
        print(f"[DISCONNECTED] {addr} disconnected.")
        clients.remove(writer)
        writer.close()
        await writer.wait_closed()

clients = []

async def start_server():
    server = await asyncio.start_server(handle_client, IP, PORT)
    addr = server.sockets[0].getsockname()
    print(f"[LISTENING] Server is listening on {addr}")

    async with server:
        await server.serve_forever()


async def main():
    conlist = []

    async def handle_client(conn,addr):
        print(f"[New Connection] {addr} connected.")

        async def clpool(client):
            data = await client.recv(CHUNK)
            if data:
                for x in conlist:
                    if x != client: await clsend(client,data)
        
        async def clsend(client,data):
            if data: await client.send(data)

        if not conn in conlist: conlist.append(conn)

        while True:
            try:
                await clpool(conn)
            except ConnectionError: conlist.pop(conn)
            except ConnectionRefusedError: conlist.pop(conn)
            except ConnectionResetError: conlist.pop(conn)
            except ConnectionAbortedError: conlist.pop(conn)
            except: pass

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        try:
            conn, addr = server_socket.accept()
            # thread = threading.Thread(target=handle_client, args=(conn, addr))
            # thread.start()
            await handle_client(conn,addr)
        except: pass

if __name__ == "__main__":
    asyncio.run(main())