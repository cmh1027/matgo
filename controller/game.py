import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "model"))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "view"))
import field
import player
import random
from PyQt4.QtGui import *
from PyQt4 import QtTest
import GUI_game as GameGUI
soundPath = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "view\sound")

class Game:
    def __init__(self, window):
        self.window = window
        self.player1 = player.Player(window, isEnemy=False)
        self.player2 = player.Player(window, isEnemy=True)
        self.myturn = True
        self.field = field.Field(window)
        self.endgame = False

    def ready(self):
        for _ in range(2):
            QtTest.QTest.qWait(500)
            self.field.put(self.field.deckpop(count=4), False)
            QtTest.QTest.qWait(500)
            self.player1.gethand(self.field.deckpop(count=5))
            QtTest.QTest.qWait(500)
            self.player2.gethand(self.field.deckpop(count=5))
        QtTest.QTest.qWait(500)
        QSound(os.path.join(soundPath, "start.wav")).play()
        self.field.arrange()
        self.player1.arrange()
        self.player2.arrange()
        QtTest.QTest.qWait(2000)
    
    def start(self):
        # check chongtong.
        fourcardcheck = (self.player1.haveFourCards(), self.player2.haveFourCards())
        if fourcardcheck[0] or fourcardcheck[1]:
            self.endgame = True
            GameGUI.chongtong(fourcardcheck[0], fourcardcheck[1])
        # begin
        self.turn(self.myturn)

    def turn(self, myturn):
        if myturn:
            slot = GameGUI.attachEventHand(self.player1, self.field)
            self.select(self.player1, slot)
        else: # computer
            self.logic(self.player2, random.randrange(len(self.player2.hand)))

    def select(self, player, slot):
        selected = player.at(slot)
        bomb = False
        threeCards = player.haveThreeCards(selected)
        if(threeCards):
            if(self.field.exist(selected)): # Bomb
                bomb = True
                player.addshake()
                self.field.put(player.put(threeCards.pop(0)))
                QtTest.QTest.qWait(200)
                self.field.put(player.put(threeCards.pop(0)))
                QtTest.QTest.qWait(200)
                firstput = self.field.put(player.put(threeCards.pop(0)))
                QtTest.QTest.qWait(400)
                QSound(os.path.join(soundPath, "bomb.wav")).play()
            else: # Shake
                player.addshake()
                QSound(os.path.join(soundPath, "shake.wav")).play()
                GameGUI.shake(player.at(threeCards[0]), player.at(threeCards[1]), player.at(threeCards[2]))
                QtTest.QTest.qWait(1500)
                firstput = self.field.put(player.put(slot))
            QtTest.QTest.qWait(700)
        else:
            if selected.prop == "bomb":
                firstput = {"slot":None, "len":None}
            else:
                firstput = self.field.put(player.put(slot))
                QtTest.QTest.qWait(700)
        secondput = self.field.put(self.field.deckpop())
        QtTest.QTest.qWait(700)
        # self.process(player, firstput, secondput, bomb)

    def process(self, player, firstput, secondput, bomb):
        rob = 0
        getcards = []
        if firstput["slot"] == secondput["slot"]:
            if secondput["pos"] == 2: # Kiss
                rob+=1
                getcards.extend(self.field.pop(firstput["slot"]))
            if secondput["pos"] == 3: # Fuck
                player.addfuck()
                player.addfuckmonth(self.__field.current[firstput["slot"]][0].month)
            else: # Tadack
                rob+=1
                getcards.extend(self.field.pop(firstput["slot"]))
        else:
            if firstput["pos"] == 4:
                if bomb:
                    rob+=1 # Bomb
                    getcards.extend(self.field.pop(firstput["slot"]))
                else:
                    rob+=1 # Get fuck
                    if self.__field.current[firstput["slot"]][0].month in player.fuckmonth: # Jafuck
                        rob += 1
                        getcards.extend(self.field.pop(firstput["slot"]))
            else if firstput["pos"] == 3:
                select = self.chooseCard(player, self.__field.current[firstput["slot"]][0:2])
                getcards.extend(self.field.pop(firstput["slot"], [select, 2]))
            else if firstput["pos"] == 2:
                getcards.extend(self.field.pop(firstput["slot"]))
            
            if secondput["pos"] == 4: # Get fuck
                rob+=1
                if self.__field.current[secondput["slot"]][0].month in player.fuckmonth: # Jafuck
                    rob += 1
                getcards.extend(self.field.pop(secondput["slot"]))
                
            else if secondput["pos"] == 3:
                select = self.chooseCard(player, self.__field.current[secondput["slot"]][0:2])
                getcards.extend(self.field.pop(secondput["slot"], [select, 2]))
            else if secondput["pos"] == 2:
                getcards.extend(self.field.pop(firstput["slot"]))
        player.getCard(getcards)
        QtTest.QTest.qWait(700)
        if player.isEnemy:
            getcards.extend(self.player1.rob(rob))
        else:
            getcards.extend(self.player2.rob(rob))
        player.getCard(getcards)
        QtTest.QTest.qWait(1000)
        if(bomb):
            player.gethandbombs()
        self.myturn = not self.myturn
        self.turn(self.myturn)

    def gameresult(self, mult, winner):
        pass
    
    def chooseCard(self, player, cards):
        if player.isEnemy:
            return random.randrange(2)
        else:
            GameGUI.chooseCard(self.window, cards)

def init(window):
    for components in window.findChildren(QPushButton): # remove Start / Exit Buttons
        components.setParent(None)
    controller = Game(window)
    controller.ready()
    controller.start()