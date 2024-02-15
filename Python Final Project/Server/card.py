import sqlite3
from constants_config import PRICES, DESTINATION_REGIONS, FAILURE, SUCCESS, MAX_AMOUNT_LENGTH


class Card:
    def __init__(self):
        """
        Initializes a Card object and establishes a connection to the SQLite database 'cards.db'.
        Creates the 'cards' table if it doesn't exist.
        """
        self.__conn = sqlite3.connect('cards.db')
        self.__cursor = self.__conn.cursor()
        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS cards 
                              (id INTEGER PRIMARY KEY, wallet INTEGER, contract TEXT)''')
        self.__conn.commit()

    def create_card(self, wallet=0, contract=None):
        """
        Creates a new card in the database with the specified wallet amount and contract.

        Args:
        - wallet (int): The initial wallet amount for the new card. Default is 0.
        - contract (str): The contract region for the new card. Default is None.

        Returns:
        - card_id (int): The ID of the newly created card.
        """
        self.__cursor.execute("INSERT INTO cards (wallet, contract) VALUES (?, ?)", (wallet, contract))
        card_id = self.__cursor.lastrowid
        self.__conn.commit()
        return card_id

    def check_card_status(self, card_id):
        """
        Retrieves the card data (ID, wallet amount, and contract) for the specified card ID.

        Args:
        - card_id (int): The ID of the card to check.

        Returns:
        - card_data (tuple): A tuple containing the card ID, wallet amount, and contract.
                            Returns an error message if the card does not exist.
        """
        if not self.card_is_valid(card_id):
            return f"Error: Card {card_id} does not exist."
        else:
            self.__cursor.execute("SELECT id, wallet, contract FROM cards WHERE id = ?", (card_id,))
            card_data = self.__cursor.fetchone()
            return card_data

    def pay_for_ride(self, card_id, destination_region):
        """
        Processes a payment for a ride using the specified card ID and destination region.

        Args:
        - card_id (int): The ID of the card to use for payment.
        - destination_region (str): The destination region for the ride.

        Returns:
        - response (str): A success message if the payment is successful, or an error message otherwise.
        """
        if not self.card_is_valid(card_id):
            return f"Error: Card {card_id} does not exist."
        else:
            self.__cursor.execute("SELECT contract, wallet FROM cards WHERE id = ?", (card_id,))
            result = self.__cursor.fetchone()
            contract, wallet = result
            if contract and destination_region.lower() == contract.lower():
                return SUCCESS
            elif destination_region.lower() in DESTINATION_REGIONS:
                ride_cost = PRICES[destination_region.lower()]
                new_wallet = wallet - ride_cost
                if new_wallet >= 0:
                    self.__cursor.execute("UPDATE cards SET wallet = ? WHERE id = ?", (new_wallet, card_id))
                    self.__conn.commit()
                    return SUCCESS
            return FAILURE

    def fill_wallet(self, card_id, amount):
        """
        Increases the wallet amount of the specified card by the specified amount.

        Args:
        - card_id (int): The ID of the card to fill its wallet.
        - amount (str): The amount to add to the wallet.

        Returns:
        - response (str): A success message if the wallet is successfully filled, or an error message otherwise.
        """
        if not self.card_is_valid(card_id):
            return f"Error: Card {card_id} does not exist!"
        if not amount.isdigit():
            return FAILURE
        amount = int(amount)
        if amount <= 0 or len(str(amount)) > MAX_AMOUNT_LENGTH:
            return FAILURE
        else:
            self.__cursor.execute("UPDATE cards SET wallet = wallet + ? WHERE id = ?", (amount, card_id))
            self.__conn.commit()
            return SUCCESS

    def change_contract(self, card_id, new_contract):
        """
        Changes the contract region of the specified card to the new contract.

        Args:
        - card_id (int): The ID of the card to change its contract.
        - new_contract (str): The new contract region.

        Returns:
        - response (str): A success message if the contract is successfully changed, or an error message otherwise.
        """
        if not self.card_is_valid(card_id):
            return f"Error: Card {card_id} does not exist."
        self.__cursor.execute("SELECT contract FROM cards WHERE id = ?", (card_id,))

        current_contract = self.__cursor.fetchone()[0]
        new_contract = new_contract.lower()
        if new_contract in DESTINATION_REGIONS and current_contract != new_contract:
            self.__cursor.execute("UPDATE cards SET contract = ? WHERE id = ?", (new_contract, card_id))
            self.__conn.commit()
            return SUCCESS
        else:
            return FAILURE

    def card_is_valid(self, card_id):
        """
        Checks if a card with the specified ID exists in the database.

        Args:
        - card_id (int): The ID of the card to check.

        Returns:
        - validity (bool): True if the card exists, False otherwise.
        """
        self.__cursor.execute("SELECT id, wallet, contract FROM cards WHERE id = ?", (card_id,))
        result = self.__cursor.fetchone()
        return bool(result)
