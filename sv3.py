import socket
import selectors
import pyaudio

# Audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 32000
CHUNK = 1024

# Server settings
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 58410

# Global variables
clients = []
selector = selectors.DefaultSelector()

def broadcast(data, exclude_socket=None):
    """Broadcast audio data to all connected clients except the sender."""
    for client_socket in clients:
        if client_socket != exclude_socket:
            try:
                client_socket.send(data)
            except Exception as e:
                print(f"Error broadcasting to client: {e}")
                clients.remove(client_socket)
                client_socket.close()

def handle_client(client_socket):
    """Handle audio data from a client."""
    try:
        while True:
            data = client_socket.recv(CHUNK)
            if not data:
                break
            broadcast(data, exclude_socket=client_socket)
    except Exception as e:
        print(f"Client error: {e}")
    finally:
        print("Client disconnected.")
        clients.remove(client_socket)
        selector.unregister(client_socket)
        client_socket.close()

def start_server():
    """Start the server and listen for incoming connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    server_socket.setblocking(False)  # Non-blocking mode

    # Register the server socket for incoming connections
    selector.register(server_socket, selectors.EVENT_READ, data=None)

    print(f"Server is listening on {HOST}:{PORT}")

    try:
        while True:
            events = selector.select(timeout=None)
            for key, _ in events:
                if key.data is None:
                    # New client connection
                    client_socket, addr = server_socket.accept()
                    print(f"New connection from {addr}")
                    client_socket.setblocking(False)
                    clients.append(client_socket)
                    selector.register(client_socket, selectors.EVENT_READ, data=handle_client)
                else:
                    # Handle client data
                    callback = key.data
                    callback(key.fileobj)
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        # Clean up
        for client_socket in clients:
            client_socket.close()
        selector.unregister(server_socket)
        server_socket.close()
        selector.close()

if __name__ == "__main__":
    start_server()