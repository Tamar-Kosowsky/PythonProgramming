from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QInputDialog, QMessageBox
from client import send_request


class ClientGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Client GUI")
        self.layout = QVBoxLayout()

        # Create Card Button
        self.create_card_button = QPushButton("Create Card")
        self.create_card_button.clicked.connect(self.create_card_request)
        self.layout.addWidget(self.create_card_button)

        # Check Card Status Button
        self.check_card_status_button = QPushButton("Check Card Status")
        self.check_card_status_button.clicked.connect(self.check_card_status_request)
        self.layout.addWidget(self.check_card_status_button)

        # Pay for Ride Button
        self.pay_for_ride_button = QPushButton("Pay for Ride")
        self.pay_for_ride_button.clicked.connect(self.pay_for_ride_request)
        self.layout.addWidget(self.pay_for_ride_button)

        # Fill Wallet Button
        self.fill_wallet_button = QPushButton("Fill Wallet")
        self.fill_wallet_button.clicked.connect(self.fill_wallet_request)
        self.layout.addWidget(self.fill_wallet_button)

        # Change Contract Button
        self.change_contract_button = QPushButton("Change Contract")
        self.change_contract_button.clicked.connect(self.change_contract_request)
        self.layout.addWidget(self.change_contract_button)

        self.setLayout(self.layout)

    def show_message_box(self, title, message):
        """
        Displays a message box with the given title and message.
        """
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def closeEvent(self, event):
        """
        Overrides the close event to display a confirmation message box before closing the connection.
        """
        reply = QMessageBox.question(self, 'Close Connection', 'Are you sure you want to close the connection?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def get_user_inputs(self, input_labels):
        """
        Displays input dialogs for each input label and returns a dictionary of user inputs.
        """
        inputs = {}
        for label in input_labels:
            value, ok = QInputDialog.getText(self, label, f"Enter {label}:")
            if ok:
                inputs[label] = value
            else:
                return None
        return inputs

    def create_card_request(self):
        """
        Sends a create_card request and displays the response in a message box.
        """
        request = "create_card"
        response = send_request(request)
        if response.startswith("Error"):
            self.show_message_box("Error", response)
        else:
            self.show_message_box("Create Card", f"Card id: {response} was created successfully")

    def check_card_status_request(self):
        """
        Sends a check_card_status request with the specified card ID and displays the response in a message box.
        """
        params = self.get_user_inputs(["Card ID"])
        if params:
            request = f"check_card_status {params['Card ID']}"
            response = send_request(request)
            if response.startswith("Error"):
                self.show_message_box("Error", response)
            else:
                self.show_message_box("Check Card Status", f"Card status: {response}")

    def pay_for_ride_request(self):
        """
        Sends a pay_for_ride request with the specified card ID and destination region, and displays the response
        in a message box.
        """
        params = self.get_user_inputs(["Card ID", "Destination Region"])
        if params:
            request = f"pay_for_ride {params['Card ID']} {params['Destination Region']}"
            response = send_request(request)
            if response.startswith("Error"):
                self.show_message_box("Error", response)
            else:
                self.show_message_box("Pay for Ride", response)

    def fill_wallet_request(self):
        """
        Sends a fill_wallet request with the specified card ID and amount, and displays the response in a message box.
        """
        params = self.get_user_inputs(["Card ID", "Amount"])
        if params:
            request = f"fill_wallet {params['Card ID']} {params['Amount']}"
            response = send_request(request)
            if response.startswith("Error"):
                self.show_message_box("Error", response)
            else:
                self.show_message_box("Fill Wallet", response)

    def change_contract_request(self):
        """
        Sends a change_contract request with the specified card ID and new contract, and displays the response in a
        message box.
        """
        params = self.get_user_inputs(["Card ID", "New Contract"])
        if params:
            request = f"change_contract {params['Card ID']} {params['New Contract']}"
            response = send_request(request)
            if response.startswith("Error"):
                self.show_message_box("Error", response)
            else:
                self.show_message_box("Change Contract", response)
