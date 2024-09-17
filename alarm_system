import sys
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QComboBox, QPushButton

HOST = "127.0.0.1"
PORT = 5556
MAX_BYTE = 1024

Alarms = ["Fire", "Obstruction", "Alarm Cleared"]

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
        self.setWindowTitle('Alarm System')
        self.setGeometry(200, 200, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.label = QLabel('Select an alarm:')
        layout.addWidget(self.label)

        self.comboBox = QComboBox()
        self.comboBox.addItems(Alarms)
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
