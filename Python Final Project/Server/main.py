import socket
from constants_config import HOST, PORT
from server import Server

if __name__ == "__main__":
    server = Server(HOST, PORT)
    try:
        server.start()
    except socket.gaierror:
        print("An error occurred while resolving the address.")
    except socket.error as e:
        print(f"An error occurred while starting the server: {e}")
    except OverflowError as e:
        print("Error: Invalid port number. Port must be within the range of 0 to 65535.")
