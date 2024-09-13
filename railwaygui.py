import math
import socket
import sys
import threading
from os.path import curdir
from time import sleep

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot

from graphing import find_shortest

HOST = "127.0.0.1"
PORT = 5555
MAX_BYTE = 1024

LINE_LEFT = 50
LINE_RIGHT = 711

LINE_1_Y = 29
LINE_2_Y = 180
LINE_3_Y = 280
LINE_4_Y = 427

LINE_1_DOWN = 69
LINE_3_DOWN = 284

LINE_WIDTH = 661
LINE_HEIGHT = 40
BETWEEN_LINES = 92
HALFOF_BETWWEN_LINES = 42
TRAIN_WIDTH = 40
TRAIN_HEIGHT = 40

X_1 = 80
X_2 = 180
X_3 = 525
X_4 = 635

TRAIN_X = 671 #50+661-40
#TRAIN_X = 661
TRAIN_Y = 376

class rotates:
    def __init__(self, rotateName, x_position, y_position):
        self.rotateName = rotateName
        self.x_position = x_position
        self.y_position = y_position

class client(QtCore.QObject):
    message_received = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.client_socket = None

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(MAX_BYTE).decode('utf-8')
                if message:
                    self.message_received.emit(message)
                    print(message)
                else:
                    print("EMPTY MESSAGE")
            except Exception as e:
                print(f"\nBağlantı koptu: {e}")
                break


    def start_client(self, host, port):
        while True:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((host, port))
                print("CONNECTED SUCCESSFULLY!")
                receive_thread = threading.Thread(target=self.receive_messages)
                receive_thread.start()
                break
            except Exception as e:
                print(f"Bağlantı hatası: {e}. Yeniden deniyorum...")
                sleep(5)


class MainWindows(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindows, self).__init__()
        self.rotateList = {}
        self.buildRotates()
        self.client = client()
        self.client.message_received.connect(self.message_decode)
        self.startServer()
        self.enemyAnimation = QtCore.QParallelAnimationGroup()  # Initialize enemyAnimation
        self.buildMainWidget()
        self.current_station = "L11M"

    def message_decode(self, station):
        try:
            paths = find_shortest(self.current_station, station)  # Use the current station
            for i, station in enumerate(paths):
                self.doAnimation(station, self.current_station)
                print(f"Current station: {self.current_station}")
                print(f"Next station: {station}")
                if i > 0:
                    self.current_station = paths[i]  # Update the current station
                # Wait for the current animation to finish before starting the next one
                while self.enemyAnimation.state() == QtCore.QAbstractAnimation.Running:
                    QtCore.QCoreApplication.processEvents()
                current_station = station
        except Exception as e:
            print(f"Error in message_decode: {e}")



    def buildRotates(self):
        self.rotateList["L11M"] = rotates("L11M", 80, 50)
        self.rotateList["L12M"] = rotates("L12M", 180, 50)
        self.rotateList["L13M"] = rotates("L13M", 80, 140)
        self.rotateList["L14M"] = rotates("L14M", 180, 140)
        self.rotateList["L15M"] = rotates("L15M", 525, 50)
        self.rotateList["L16M"] = rotates("L16M", 635, 50)
        self.rotateList["L17M"] = rotates("L17M", 525, 140)
        self.rotateList["L18M"] = rotates("L18M", 635, 140)
        self.rotateList["L19M"] = rotates("L19M", 80, 300)
        self.rotateList["L20M"] = rotates("L20M", 180, 300)
        self.rotateList["L21M"] = rotates("L21M", 80, 400)
        self.rotateList["L22M"] = rotates("L22M", 180, 400)
        self.rotateList["L23M"] = rotates("L23M", 525, 300)
        self.rotateList["L24M"] = rotates("L24M", 635, 300)
        self.rotateList["L25M"] = rotates("L25M", 525, 400)
        self.rotateList["L26M"] = rotates("L26M", 635, 400)


    def startServer(self):
        server_thread = threading.Thread(target=self.runServer)
        server_thread.daemon = True
        server_thread.start()

    def runServer(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen(5)
        print("Server started, waiting for connections...")
        while True:
            client_socket, addr = server.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(MAX_BYTE).decode('utf-8')
                if message:
                    self.client.message_received.emit(message)
                else:
                    break
            except Exception as e:
                print(f"Client connection error: {e}")
                break
        client_socket.close()

    def path_lender(self, go):
        try:
            paths = find_shortest("L11M", go)
            current_station = "L11M"
            for i, station in enumerate(paths):
                if i > 1:
                    current_station = paths[i]
                self.doAnimation(station, current_station)
                # Wait for the current animation to finish before starting the next one
                while self.enemyAnimation.state() == QtCore.QAbstractAnimation.Running:
                    QtCore.QCoreApplication.processEvents()
        except Exception as e:
            print(f"Error in path_lender: {e}")

    @pyqtSlot(str, str)
    def doAnimation(self, target, current_station):
        current_x = self.btn_tren14.x()
        current_y = self.btn_tren14.y()
        self.btn_tren14.raise_()
        if self.enemyAnimation and self.enemyAnimation.state() == QtCore.QAbstractAnimation.Running:
            self.enemyAnimation.stop()
        self.enemyAnimation.clear()
        if target in self.rotateList:
            if target == "L19M" and current_station == "L16M":
                # Special case for L19M: instantly move the train to L19M
                self.btn_tren14.move(self.rotateList["L19M"].x_position, self.rotateList["L19M"].y_position)
            elif target == "L18M" and current_station == "L21M":
                # Special case for L19M: instantly move the train to L19M
                self.btn_tren14.move(self.rotateList["L18M"].x_position, self.rotateList["L18M"].y_position)
            else:
                try:
                    animation = QtCore.QPropertyAnimation(self.btn_tren14, b'pos')
                    duration = int((math.sqrt((self.rotateList[target].x_position - current_x) ** 2 +
                                          (self.rotateList[target].y_position - current_y) ** 2)) * 5)
                    animation.setDuration(duration)
                    animation.setStartValue(QtCore.QPoint(current_x, current_y))
                    animation.setEndValue(
                        QtCore.QPoint(self.rotateList[target].x_position, self.rotateList[target].y_position))
                    self.enemyAnimation.addAnimation(animation)
                    self.enemyAnimation.start()
                except Exception as e:
                    print(f"Error: {e}")
        current_station = target



    @pyqtSlot()
    def stopAnimation(self):
        self.activateWindow()
        self.enemyAnimation.pause()


#--------------------------------------------------Design--------------------------------------------------------
    def buildMainWidget(self):
        self.resize(800, 610)
        self.centralwidget = QtWidgets.QWidget(self)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setMinimumSize(QtCore.QSize(0, 500))
        self.widget.setMaximumSize(QtCore.QSize(16777215, 500))
        self.widget.setStyleSheet("background-color: rgb(0, 0, 0);")

        self.line = QtWidgets.QFrame(self.widget)
        self.line.setGeometry(QtCore.QRect(50, 53, 661, 20))
        self.line.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.btn_tren14 = QtWidgets.QPushButton(self.widget)
        self.btn_tren14.setGeometry(QtCore.QRect(40, 40, 60, 40))
        self.btn_tren14.setStyleSheet("background-color: rgb(85, 255, 127);")
        self.btn_tren14.setText("14")
        self.btn_tren14.raise_()

        self.line_2 = QtWidgets.QFrame(self.widget)
        self.line_2.setGeometry(QtCore.QRect(50, 160, 661, 20))
        self.line_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.createScissors()
        self.createStops()
        self.verticalLayout.addWidget(self.widget)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)

        self.line3 = QtWidgets.QFrame(self.widget)
        self.line3.setGeometry(QtCore.QRect(50, 300, 661, 20))
        self.line3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.line3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line3.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.line4 = QtWidgets.QFrame(self.widget)
        self.line4.setGeometry(QtCore.QRect(50, 407, 661, 20))
        self.line4.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.line4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line4.setFrameShadow(QtWidgets.QFrame.Sunken)


    def createStops(self):
        self.L11M = QtWidgets.QPushButton(self.widget)
        self.L11M.setGeometry(QtCore.QRect(80, 70, 50, 40))
        self.L11M.setStyleSheet("background-color: rgb(0, 71, 171);")
        self.L11M.setText("L11M")
        self.L11M.raise_()

        self.L12M = QtWidgets.QPushButton(self.widget)
        self.L12M.setGeometry(QtCore.QRect(180, 70, 50, 40))
        self.L12M.setStyleSheet("background-color: rgb(0, 71, 171);")
        self.L12M.setText("L12M")
        self.L12M.raise_()

        self.L13M = QtWidgets.QPushButton(self.widget)
        self.L13M.setGeometry(QtCore.QRect(80, 120, 50, 40))
        self.L13M.setStyleSheet("background-color: rgb(0, 71, 171);")
        self.L13M.setText("L13M")
        self.L13M.raise_()

        self.L14M = QtWidgets.QPushButton(self.widget)
        self.L14M.setGeometry(QtCore.QRect(180, 120, 50, 40))
        self.L14M.setStyleSheet("background-color: rgb(0, 71, 171);")
        self.L14M.setText("L14M")
        self.L14M.raise_()

        self.L15M = QtWidgets.QPushButton(self.widget)
        self.L15M.setGeometry(QtCore.QRect(525, 70, 50, 40))
        self.L15M.setStyleSheet("background-color: rgb(0, 71, 171);")
        self.L15M.setText("L15M")
        self.L15M.raise_()

        self.L16M = QtWidgets.QPushButton(self.widget)
        self.L16M.setGeometry(QtCore.QRect(635, 70, 50, 40))
        self.L16M.setStyleSheet("background-color: rgb(0, 71, 171);")
        self.L16M.setText("L16M")
        self.L16M.raise_()

        self.L17M = QtWidgets.QPushButton(self.widget)
        self.L17M.setGeometry(QtCore.QRect(525, 120, 50, 40))
        self.L17M.setStyleSheet("background-color: rgb(0, 71, 171);")
        self.L17M.setText("L17M")
        self.L17M.raise_()

        self.L18M = QtWidgets.QPushButton(self.widget)
        self.L18M.setGeometry(QtCore.QRect(635, 120, 50, 40))
        self.L18M.setStyleSheet("background-color: rgb(0, 71, 171);")
        self.L18M.setText("L18M")
        self.L18M.raise_()

        self.L19M = QtWidgets.QPushButton(self.widget)
        self.L19M.setGeometry(QtCore.QRect(80, 320, 50, 40))
        self.L19M.setStyleSheet("background-color: rgb(0, 71, 171);")
        self.L19M.setText("L19M")
        self.L19M.raise_()

        self.L20M = QtWidgets.QPushButton(self.widget)
        self.L20M.setGeometry(QtCore.QRect(180, 320, 50, 40))
        self.L20M.setStyleSheet("background-color: rgb(0, 71, 171);")
        self.L20M.setText("L20M")
        self.L20M.raise_()

        self.L21M = QtWidgets.QPushButton(self.widget)
        self.L21M.setGeometry(QtCore.QRect(80, 370, 50, 40))
        self.L21M.setStyleSheet("background-color: rgb(0, 71, 171);")
        self.L21M.setText("L21M")
        self.L21M.raise_()

        self.L22M = QtWidgets.QPushButton(self.widget)
        self.L22M.setGeometry(QtCore.QRect(180, 370, 50, 40))
        self.L22M.setStyleSheet("background-color: rgb(0, 71, 171);")
        self.L22M.setText("L22M")
        self.L22M.raise_()

        self.L23M = QtWidgets.QPushButton(self.widget)
        self.L23M.setGeometry(QtCore.QRect(525, 320, 50, 40))
        self.L23M.setStyleSheet("background-color: rgb(0, 71, 171);")
        self.L23M.setText("L23M")
        self.L23M.raise_()

        self.L24M = QtWidgets.QPushButton(self.widget)
        self.L24M.setGeometry(QtCore.QRect(635, 320, 50, 40))
        self.L24M.setStyleSheet("background-color: rgb(0, 71, 171);")
        self.L24M.setText("L24M")
        self.L24M.raise_()

        self.L25M = QtWidgets.QPushButton(self.widget)
        self.L25M.setGeometry(QtCore.QRect(525, 370, 50, 40))
        self.L25M.setStyleSheet("background-color: rgb(0, 71, 171);")
        self.L25M.setText("L25M")
        self.L25M.raise_()

        self.L26M = QtWidgets.QPushButton(self.widget)
        self.L26M.setGeometry(QtCore.QRect(635, 370, 50, 40))
        self.L26M.setStyleSheet("background-color: rgb(0, 71, 171);")
        self.L26M.setText("L26M")
        self.L26M.raise_()


    def createScissors(self):
        self.graphicsView = QtWidgets.QGraphicsView(self.widget)
        self.graphicsView.setGeometry(QtCore.QRect(50,70,661,90))

        self.graphicsView2 = QtWidgets.QGraphicsView(self.widget)
        self.graphicsView2.setGeometry(QtCore.QRect(50, 300, 661, 120))

        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.scene.setSceneRect(0,0,650,75)

        self.scene2 = QtWidgets.QGraphicsScene()
        self.graphicsView2.setScene(self.scene)
        self.scene2.setSceneRect(0, 300, 650, 275)

        self.line1to2 = QtWidgets.QGraphicsLineItem(50, 0, 150, 80) #bas x,y, bitis x,y
        self.line2to1 = QtWidgets.QGraphicsLineItem(150, 0, 50, 80)
        self.line3to4 = QtWidgets.QGraphicsLineItem(50, 300, 150, 480)  # bas x,y, bitis x,y
        self.line4to3 = QtWidgets.QGraphicsLineItem(150, 300, 50, 580)

        self.stop = QtWidgets.QGraphicsRectItem(0,0,60,60) #x,y,boyutlar

        self.line1to2_1 = QtWidgets.QGraphicsLineItem(500, 0, 600, 80)
        self.line2to1_1 = QtWidgets.QGraphicsLineItem(600, 0, 500, 80)
        self.line3to4_1 = QtWidgets.QGraphicsLineItem(500, 500, 600, 580)
        self.line4to3_1 = QtWidgets.QGraphicsLineItem(600, 300, 500, 580)

        self.stop.setPos(300,8)
        self.stop.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))

        self.pen = QtGui.QPen(QtGui.QColor(255,255,255),10) #renk,kalınlık

        self.line1to2.setPen(self.pen)
        self.line2to1.setPen(self.pen)
        self.line1to2_1.setPen(self.pen)
        self.line2to1_1.setPen(self.pen)
        self.line3to4.setPen(self.pen)
        self.line4to3.setPen(self.pen)
        self.line3to4_1.setPen(self.pen)
        self.line4to3_1.setPen(self.pen)

        self.scene.addItem(self.line1to2)
        self.scene.addItem(self.line2to1)
        self.scene.addItem(self.line1to2_1)
        self.scene.addItem(self.line2to1_1)
        self.scene2.addItem(self.line3to4)
        self.scene2.addItem(self.line4to3)
        self.scene2.addItem(self.line3to4_1)
        self.scene2.addItem(self.line4to3_1)
        self.scene.addItem(self.stop)
        self.scene2.addItem(self.stop)

        self.btn_tren14.raise_()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    windows = MainWindows()
    windows.show()
    sys.exit(app.exec_())
