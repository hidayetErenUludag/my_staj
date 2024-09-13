import sys
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QComboBox, QPushButton

HOST = "127.0.0.1"
PORT = 5555
MAX_BYTE = 1024

stations = ["L11M", "L12M", "L13M", "L14M", "L15M", "L16M",
            "L17M", "L18M", "L19M", "L20M", "L21M", "L22M",
            "L23M", "L24M", "L25M", "L26M"]

def send_message(data):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        client_socket.send(data.encode())
        client_socket.close()
    except Exception as e:
        print(f"Error: {e}")

class TrainServerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Train Server')
        self.setGeometry(100, 100, 300, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.label = QLabel('Select a station:')
        layout.addWidget(self.label)

        self.comboBox = QComboBox()
        self.comboBox.addItems(stations)
        layout.addWidget(self.comboBox)

        self.button = QPushButton('Send')
        self.button.clicked.connect(self.send_station)
        layout.addWidget(self.button)

        central_widget.setLayout(layout)

    def send_station(self):
        selected_station = self.comboBox.currentText()
        send_message(selected_station)
        self.label.setText(f'Sent: {selected_station}')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = TrainServerGUI()
    gui.show()
    sys.exit(app.exec_())