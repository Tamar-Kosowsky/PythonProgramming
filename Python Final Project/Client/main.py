import sys
from PyQt5.QtWidgets import QApplication
from gui import ClientGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)

    client_gui = ClientGUI()
    client_gui.show()
    sys.exit(app.exec_())
