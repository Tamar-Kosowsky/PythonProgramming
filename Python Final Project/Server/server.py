import socket
import threading
from card import Card
from constants_config import BUFFER_SIZE


class Server:
    def __init__(self, host, port):
        """
        Initializes a Server object with the specified host and port.

        Args:
        - host (str): The IP address or hostname to bind the server socket to.
        - port (int): The port number to bind the server socket to.
        """
        self.__host = host
        self.__port = port
        self.__address = (self.__host, self.__port)
        self.__buffer_size = BUFFER_SIZE
        self.__server_socket = None

    def start(self):
        """
        Starts the server and listens for incoming client connections.
        """
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.bind(self.__address)
        self.__server_socket.listen(5)

        print("Server is listening for connections...")

        while True:
            try:
                client_socket, client_address = self.__server_socket.accept()
                print(f"New connection from {client_address}")
                client_thread = threading.Thread(target=self.handle_client_request,
                                                 args=(client_socket, client_address))
                client_thread.start()
            except (socket.error, ConnectionError):
                print("An error occurred while accepting a client connection.")
                continue

    def handle_client_request(self, client_socket, client_address):
        """
        Handles client requests and sends appropriate responses.

        Args:
        - client_socket (socket.socket): The socket object for the connected client.
        - client_address (tuple): The address of the connected client.
        """
        while True:
            try:
                message = client_socket.recv(self.__buffer_size)
                request = message.decode('utf-8')
                response = ""
                card = Card()
            except (socket.error, ConnectionError):
                print(f"An error occurred with client {client_address}.")
                break

            # Process the client's request and perform the appropriate function call
            if request == "create_card":
                response = str(card.create_card())
            elif request.startswith("check_card_status"):
                card_id = request.split(" ")[1]
                card_data = card.check_card_status(card_id)
                response = card_data if isinstance(card_data, str) \
                    else f"Card ID: {card_data[0]}, Wallet: {card_data[1]}, Contract: {card_data[2]}"
            elif request.startswith("pay_for_ride"):
                card_id = request.split(" ")[1]
                destination_region = request.split(" ")[2]
                response = card.pay_for_ride(card_id, destination_region)
            elif request.startswith("fill_wallet"):
                card_id = request.split(" ")[1]
                amount = request.split(" ")[2]
                response = card.fill_wallet(card_id, amount)
            elif request.startswith("change_contract"):
                card_id = request.split(" ")[1]
                new_contract = request.split(" ")[2]
                response = card.change_contract(card_id, new_contract)

            # Send the response back to the client
            try:
                client_socket.send(response.encode('utf-8'))
            except (socket.error, ConnectionError):
                print(f"An error occurred while sending a response to client {client_address}.")
                break

        client_socket.close()
