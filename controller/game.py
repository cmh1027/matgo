import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "model"))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "view"))
import field
import player
import time
import GUIhandler as gui
from PyQt4.QtGui import *
from PyQt4 import QtTest
import PyQt4.QtCore as QtCore
soundPath = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "view\sound")

class Game:
    def __init__(self, window):
        self.player1 = player.Player(isEnemy=False)
        self.player2 = player.Player(isEnemy=True)
        self.field = field.Field(window)
        self.endgame = False
        self.whoop = QSound(os.path.join(soundPath, "whoop.wav"))
        self.whip = QSound(os.path.join(soundPath, "whip.wav"))
        self.start = QSound(os.path.join(soundPath, "start.wav"))
    def ready(self):
        QtTest.QTest.qWait(300)
        for _ in range(2):
            self.whoop.play()
            self.field.putcard(self.field.deckpop(count=4), False)
            QtTest.QTest.qWait(500)
            self.whoop.play()
            self.player1.gethand(self.field.deckpop(count=5))
            QtTest.QTest.qWait(300)
            self.whoop.play()
            self.player2.gethand(self.field.deckpop(count=5))
            QtTest.QTest.qWait(500)
        self.field.arrange()
        self.player1.arrange()
        self.player2.arrange()
        self.start.play()
        QtTest.QTest.qWait(300)
    def start(self):
        pass

def init(window):
    for components in window.findChildren(QPushButton): # remove Start / Exit Buttons
        components.setParent(None)
    controller = Game(window)
    controller.ready()