import os
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtTest
from playercontroller import Player
from fieldcontroller import Field
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "view"))
import GUI_game as GameGUI
from game import Game
from card import Card

class Gamecontroller(QObject):
    answer = pyqtSignal(int)
    def __init__(self, window, winner):
        super().__init__()
        self.window = window
        self.gamefield = window.gamefield
        for components in window.gamefield.findChildren(QPushButton): # remove Start / Exit Buttons
            components.setParent(None)
        self.cardlabels = {}
        self.status = {}
        self.answer.connect(self.respond)
        self.start(winner)

    def start(self, winner, draw=0, push=0):
        for key, card in self.cardlabels.items():
            card.setParent(None)
        self.cardlabels = {}
        for key, label in self.status.items():
            label.setParent(None)
        self.status = {}
        self.controller = Game(panmoney=1000, winner=winner, draw=draw, push=push)
        self.controller.attacheventhand.connect(self.attacheventhand)
        self.controller.playsound.connect(self.playsound)
        self.controller.addstatus.connect(self.addstatus)
        self.controller.updatestatus.connect(self.updatestatus)
        self.controller.addcard.connect(self.addcard)
        self.controller.removecard.connect(self.removecard)
        self.controller.flipcard.connect(self.flipcard)
        self.controller.movecard.connect(self.movecard)
        self.controller.raisecard.connect(self.raisecard)
        self.controller.shake.connect(self.shake)
        self.controller.chongtong.connect(self.chongtong)
        self.controller.result.connect(self.result)
        self.controller.endgame.connect(self.endgame)
        self.controller.start()
    
    @pyqtSlot(int)
    def respond(self, answer):
        self.controller.waitforResponse = False
        self.controller.answer = answer

    @pyqtSlot(list, Field)
    def attacheventhand(self, hand, field):
        GameGUI.attachEventHand(self, hand, field)

    @pyqtSlot(str)
    def playsound(self, sound):
        self.window.config["sound"][sound].play()

    @pyqtSlot(bool)
    def addstatus(self, isEnemy):
        self.status[isEnemy] = GameGUI.Status(self.gamefield, isEnemy)

    @pyqtSlot(bool, str, int, int, int, int, int)
    def updatestatus(self, isEnemy, status, gwang, animal, dan, peenum, peesum):
        self.status[isEnemy].status.setText(status)
        self.status[isEnemy].gwanglabel.setText(gwang)
        self.status[isEnemy].animallabel.setText(animal)
        self.status[isEnemy].danlabel.setText(dan)
        self.status[isEnemy].peelabel.setText(peenum, peesum)
    
    @pyqtSlot(Card)
    def addcard(self, card):
        cardLabel = GameGUI.CardLabel(self.gamefield)
        cardLabel.move(350, 200)
        cardLabel.show()
        self.cardlabels[card] = cardLabel

    @pyqtSlot(Card)
    def removecard(self, card):
        self.cardlabels[card].setParent(None)

    @pyqtSlot(Card)
    def flipcard(self, card):
        try:
            self.cardlabels[card].setImage(os.path.join(os.getcwd(), "view\img_matgo\cards\\"+card.imageName))
        except KeyError:
            pass
    @pyqtSlot(Card, int, int)
    def movecard(self, card, x, y):
        try:
            self.cardlabels[card].move(x, y)
        except KeyError:
            pass    
    @pyqtSlot(Card)
    def raisecard(self, card):
        self.cardlabels[card].raise_()

    @pyqtSlot(list, int, int)
    def shake(self, cards, width, height):
        try:
            dialog = GameGUI.ShakeDialog(self.gamefield, cards, width, height)
            QtTest.QTest.qWait(2000)
            dialog.setParent(None)
        except RuntimeError:
            pass
    @pyqtSlot(list, int, int)
    def chongtong(self, cards, width, height):
        try:
            dialog = GameGUI.ChongtongDialog(self.gamefield, cards, width, height)
            QtTest.QTest.qWait(2000)
            dialog.setParent(None)
        except RuntimeError:
            pass
    @pyqtSlot(str, int, int, list, int)
    def result(self, title, width, height, messages, money):
        try:
            dialog = GameGUI.ResultDialog(self.gamefield, title, width, height, messages, money)
            QtTest.QTest.qWait(4500)
            dialog.setParent(None)
        except RuntimeError:
            pass
    @pyqtSlot(dict)
    def endgame(self, result):
        if result["winner"] == None: # draw
            draw = self.controller.draw
            push = self.controller.push
            self.controller.quit()
            del self.controller
            self.start(winner=None, draw=draw, push=push)
        elif result["push"] == True:
            draw = self.controller.draw
            push = self.controller.push
            self.controller.quit()
            del self.controller
            self.start(winner=result["winner"], draw=draw, push=push)
        else:
            self.window.singleGameScreen(result["winner"])
            self.controller.quit()