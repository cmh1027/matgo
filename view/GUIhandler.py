from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "controller"))
import game
class Image(QLabel):
    def __init__(self, window, image, x, y):
        super().__init__(window)
        image_file = QPixmap(os.path.join(os.getcwd(), "view\img_matgo\\"+image))
        self.setPixmap(image_file)
        self.resize(image_file.size().width(), image_file.size().height())
        self.move(x, y)
class MainMenuButton(QPushButton):
    def __init__(self, string):
        super().__init__(string)
        self.setFixedHeight(50)
        self.setFont(QFont("Times", 15, QFont.Bold))
        self.setStyleSheet("background-color: white")
        self.show()

def mainScreen(window):
    for components in window.findChildren(QWidget):
        components.deleteLater()
    window.setStyleSheet("background-color: yellow")
    menus = QVBoxLayout()
    menus.setContentsMargins(250, 20, 250, 60)
    title = QLabel("MATGO")
    title.setFont(QFont("Times", 35, QFont.Bold))
    title.setStyleSheet("color: blue")
    title.setFixedHeight(110)
    title.setFixedWidth(200)
    menus.addWidget(title)
    singleButton = MainMenuButton("vs Computer")
    menus.addWidget(singleButton)
    singleButton.clicked.connect(lambda state, win=window: singleGameScreen(win))
    multiButton = MainMenuButton("vs Player")
    menus.addWidget(multiButton)
    configButton = MainMenuButton("설정")
    menus.addWidget(configButton)
    exitButton = MainMenuButton("나가기")
    menus.addWidget(exitButton)
    exitButton.clicked.connect(lambda state: sys.exit(0))
    window.setLayout(menus)


def singleGameScreen(window):
    QWidget().setLayout(window.layout())
    for components in window.findChildren(QWidget):
        components.deleteLater()
    Image(window, "Field.png", 0, 0).show()
    Image(window, "gony.png", 376, 369).show()
    Image(window, "monkfish.png", 376, 1).show()
    startButton = QPushButton("시작", window)
    startButton.move(80, 210)
    startButton.setFont(QFont("Times", 15, QFont.Bold))
    startButton.setStyleSheet("background-color: white;color: red")
    startButton.clicked.connect(lambda state, win=window: game.init(win))
    startButton.show()
    exitButton = QPushButton("나가기", window)
    exitButton.move(230, 210)
    exitButton.setFont(QFont("Times", 15, QFont.Bold))
    exitButton.setStyleSheet("background-color: white;color: red")
    exitButton.clicked.connect(lambda state, win=window: mainScreen(win))
    exitButton.show()