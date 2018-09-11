from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "controller"))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "model"))
from gamecontroller import Gamecontroller
from card import Card
class Image(QLabel):
    def __init__(self, window, image, x, y, width, height):
        super().__init__(window)
        self.setPixmap(image)
        self.resize(width, height)
        self.move(x, y)
        self.show()

class Profile(QLabel):
    def __init__(self, window, enemy):
        super().__init__(window)
        if enemy:
            self.move(376, 95)
            self.resize(95, 39)
        else:
            self.move(375, 324)
            self.resize(95, 45)
        self.setStyleSheet("background-color: orange")
        self.setFont(QFont("Times", 10))
        self.setAlignment(Qt.AlignCenter)
        self.show()
    def setInfo(self, nickname, money=None):
        if money:
            self.setText("{}\n{}원".format(nickname, money))
        else:
            self.setText("{}\n".format(nickname))

class MainMenuButton(QPushButton):
    def __init__(self, string):
        super().__init__(string)
        self.setFixedHeight(50)
        self.setFixedWidth(150)
        self.setFont(QFont("Times", 15, QFont.Bold))
        self.setStyleSheet("background-color: white")
        self.show()

class Sidebar(QLabel):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.setStyleSheet("background-color: white;")
        self.move(676, 0)
        self.resize(200, 459)
        self.show()
        self.chatarea = QPlainTextEdit(self)
        self.chatarea.move(0, 0)
        self.chatarea.resize(201, 334)
        self.chatarea.setDisabled(True)
        self.chatarea.show()
        self.chatinput = QLineEdit(self)
        self.chatinput.move(0, 334)
        self.chatinput.resize(170, 26)
        self.chatinput.show()
        self.sendbutton = QPushButton("전송", self)
        self.sendbutton.move(170, 334)
        self.sendbutton.resize(30, 26)
        self.sendbutton.show()
        self.quitbutton = QPushButton("나가기", self)
        self.quitbutton.move(10, 374)
        self.quitbutton.resize(50, 26)
        self.quitbutton.clicked.connect(self.quit)
        self.quitbutton.show()
    
    @pyqtSlot()
    def quit(self):
        try:
            self.window.game.controller.terminate()
            self.window.game.controller.wait()
        except:
            pass
        self.window.mainScreen()

class Gamefield(QLabel):
    def __init__(self, window):
        super().__init__(window)
        self.move(0, 0)
        self.resize(676, 459)
        self.show()

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(676, 459)
        self.setWindowTitle("MATGO")
        self.setWindowIcon(QIcon('icon.ico'))
        self.show()
        try:
            with open('settings.json') as data_file:    
                self.config = json.load(data_file)
                self.config["nickname"] = self.config["nickname"][:8]
                for key, value in self.config["image"].items():
                    path = value.replace('/', '\\')
                    if not os.path.exists(os.path.join(os.getcwd(), path)):
                        raise FileNotFoundError(os.path.join(os.getcwd(), path) + " is not found")
                    self.config["image"][key] = QPixmap(os.path.join(os.getcwd(), path))
                for key, value in self.config["sound"].items():
                    path = value.replace('/', '\\')
                    if not os.path.exists(os.path.join(os.getcwd(), path)):
                        raise FileNotFoundError(os.path.join(os.getcwd(), path) + " is not found")
                    self.config["sound"][key] = QSound(os.path.join(os.getcwd(), path))
        except KeyError as error:
            print("****** Some configuration is missing! Check settings.json ******")
            print("Error message :", error)
            sys.exit(0)
        except FileNotFoundError as error:
            print("****** Some file is not found! Check settings.json ******")
            print("Error message :", error)
            sys.exit(0)
        except TypeError as error:
            print("****** Some configuration is invalid! Check settings.json ******")
            print("Error message :", error)
            sys.exit(0)
        
    def closeEvent(self, event):
        event.accept()
        self.deleteLater()
        sys.exit(0)

    def mainScreen(self):
        if self.layout():
            QWidget().setLayout(self.layout())
        self.setFixedWidth(676)
        self.setFixedHeight(459)
        for components in self.findChildren(QWidget):
            components.deleteLater()
        self.setStyleSheet("background-color: yellow")
        menus = QVBoxLayout()
        menus.setContentsMargins(200, 20, 200, 40)
        title = QLabel("MATGO")
        title.setFont(QFont("Times", 35, QFont.Bold))
        title.setStyleSheet("color: blue")
        title.setFixedHeight(110)
        title.setFixedWidth(200)
        menus.addWidget(title, 0, Qt.AlignCenter)
        singleButton = MainMenuButton("vs Computer")
        menus.addWidget(singleButton, 0, Qt.AlignCenter)
        singleButton.clicked.connect(self.singleGameEnter)
        multiButton = MainMenuButton("vs Player")
        menus.addWidget(multiButton, 0, Qt.AlignCenter)
        configButton = MainMenuButton("설정")
        menus.addWidget(configButton, 0, Qt.AlignCenter)
        exitButton = MainMenuButton("나가기")
        menus.addWidget(exitButton, 0, Qt.AlignCenter)
        exitButton.clicked.connect(lambda state: sys.exit(0))
        self.setLayout(menus)
        
    def singleGameEnter(self):
        if self.layout():
            QWidget().setLayout(self.layout())
        self.setFixedWidth(876)
        self.setFixedHeight(459)
        self.gamefield = Gamefield(self)
        self.sidebar = Sidebar(self)
        Image(self.gamefield, self.config["image"]["field_image"], 0, 0, 676, 459)
        Image(self.gamefield, self.config["image"]["my_profile"], 375, 369, 95, 95)
        Image(self.gamefield, self.config["image"]["computer_profile"], 376, 0, 95, 95)
        Profile(self.gamefield, True).setInfo("Computer")
        Profile(self.gamefield, False).setInfo(self.config["nickname"])
        self.singleGameScreen()

    def singleGameScreen(self, winner=None):
        def exit():
            del self.gamefield
            del self.sidebar
            del self.game
            self.mainScreen()
        for component in self.gamefield.findChildren(QWidget):
            if type(component).__name__ != 'Image' and type(component).__name__ != 'Profile':
                component.deleteLater()
        startButton = QPushButton("시작", self.gamefield)
        startButton.move(80, 210)
        startButton.setFont(QFont("Times", 15, QFont.Bold))
        startButton.setStyleSheet("background-color: white;color: red")
        if winner==None:
            startButton.clicked.connect(self.init)
        else:
            startButton.clicked.connect(lambda state, winner=winner: self.init(winner))
        startButton.show()
        exitButton = QPushButton("나가기", self.gamefield)
        exitButton.move(230, 210)
        exitButton.setFont(QFont("Times", 15, QFont.Bold))
        exitButton.setStyleSheet("background-color: white;color: red")
        exitButton.clicked.connect(exit)
        exitButton.show()
    
    def init(self, winner=None):
        self.game = Gamecontroller(self, winner)