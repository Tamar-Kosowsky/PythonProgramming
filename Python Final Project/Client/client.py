import socket
from constants_config import HOST, PORT, BUFFER_SIZE


def send_request(request):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.settimeout(5)  # Set a timeout of 5 seconds
            client_socket.connect((HOST, PORT))
            client_socket.send(request.encode('utf-8'))
            response = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        return response
    except (socket.timeout, socket.gaierror, ConnectionError, ConnectionRefusedError, OSError, OverflowError) as e:
        if isinstance(e, socket.timeout):
            return "Error: Connection timed out"
        elif isinstance(e, socket.gaierror):
            return "Error: Failed to resolve the address."
        else:
            return f"Error: Failed to connect to the server. {str(e)}"
