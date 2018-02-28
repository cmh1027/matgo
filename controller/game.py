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
import GUI_screen as ScreenGUI
soundPath = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "view\sound")



class Game:
    def __init__(self, window):
        self.window = window
        self.player1 = player.Player(window, isEnemy=False)
        self.player2 = player.Player(window, isEnemy=True)
        self.myturn = True
        self.field = field.Field(window)
    
    def replay(self):
        self.player1 = player.Player(window, isEnemy=False)
        self.player2 = player.Player(window, isEnemy=True)
        self.myturn = True
        self.field = field.Field(window)
        self.ready()
        self.start()

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
            GameGUI.chongtong(self.window, fourcardcheck[0], fourcardcheck[1])
            if fourcardcheck[0] and not fourcardcheck[1]:
                self.gameresult(winner=self.player1, "chongtong")
            elif not fourcardcheck[0] and fourcardcheck[1]:
                self.gameresult(winner=self.player2, "chongtong")
            else:
                self.gameresult(winner=None)
            return
        # begin
        while True:
            end = self.turn(self.myturn)
            self.myturn = not self.myturn
            if end == True:
                break

    def turn(self, myturn):
        if myturn:
            slot = GameGUI.attachEventHand(self.player1, self.field)
            return self.select(self.player1, slot)
        else: # computer
            return self.select(self.player2, random.randrange(len(self.player2.hand)))

    def select(self, player, slot):
        selected = player.at(slot)
        bomb = False
        threeCards = player.haveThreeCards(selected)
        if(threeCards):
            player.addshake()
            if(self.field.exist(selected)): # Bomb
                bomb = True
                firstput = GameGUI.bomb(self.window, self.field, player, threeCards)
            else: # Shake
                GameGUI.shake(self.window, threeCards)
                firstput = self.field.put(player.put(slot))
            QtTest.QTest.qWait(700)
        else:
            if selected.prop == "bomb":
                firstput = {"slot":None, "pos":None}
            else:
                firstput = self.field.put(player.put(slot))
                QtTest.QTest.qWait(700)
        secondput = self.field.put(self.field.deckpop())
        QtTest.QTest.qWait(700)
        return self.process(player, firstput, secondput, bomb)

    def process(self, player, firstput, secondput, bomb):
        rob = 0
        getcards = []
        if firstput["slot"] == secondput["slot"]:
            if secondput["pos"] == 2: # Kiss
                rob+=1
                getcards.extend(self.field.pop(firstput["slot"]))
                GameGUI.kiss(self.window, player)
            elif secondput["pos"] == 3: # Fuck
                player.addfuck()
                player.addfuckmonth(self.field.current[firstput["slot"]][0].month)
                GameGUI.fuck(self.window, player)
                if player.fuck==3:
                    GameGUI.threefuck(self.window, player)
                    return self.gameresult(winner=player, "threefuck")
            elif secondput["pos"] == 4: # Tadack
                rob+=1
                getcards.extend(self.field.pop(firstput["slot"]))
                GameGUI.tadack(self.window, player)
        else:
            if firstput["pos"] == 4:
                if bomb:
                    rob+=1 # Bomb
                    getcards.extend(self.field.pop(firstput["slot"]))
                else:
                    rob+=1 # Get fuck
                    if self.field.current[firstput["slot"]][0].month in player.fuckmonth: # Jafuck
                        rob += 1
                        GameGUI.jafuck(self.window, player)
                    else:
                        GameGUI.getfuck(self.window, player)
                    getcards.extend(self.field.pop(firstput["slot"]))
            elif firstput["pos"] == 3:
                select = self.whattoget(player, self.field.current[firstput["slot"]][0:2])
                getcards.extend(self.field.pop(firstput["slot"], [select, 2]))
            elif firstput["pos"] == 2:
                getcards.extend(self.field.pop(firstput["slot"]))
            if secondput["pos"] == 4: # Get fuck
                rob+=1
                if self.field.current[secondput["slot"]][0].month in player.fuckmonth: # Jafuck
                    rob += 1
                    GameGUI.jafuck(self.window, player)
                else:
                    GameGUI.getfuck(self.window, player)
                getcards.extend(self.field.pop(secondput["slot"]))
            elif secondput["pos"] == 3:
                select = self.whattoget(player, self.field.current[secondput["slot"]][0:2])
                getcards.extend(self.field.pop(secondput["slot"], [select, 2]))
            elif secondput["pos"] == 2:
                getcards.extend(self.field.pop(secondput["slot"]))
        if player.isEnemy:
            getcards.extend(self.player1.rob(rob))
        else:
            getcards.extend(self.player2.rob(rob))
        if list(filter(lambda c:c.prop=="dual", getcards)) != []:
            dual = list(filter(lambda c:c.prop=="dual", getcards))[0]
            select = self.selectdual(player)
            if select == "animal":
                dual.propchange("animal")
            else:
                dual.propchange("pee")
        player.getCard(getcards)
        if list(filter(lambda c:c.prop=="gwang", getcards)) != []:
            if len(player.gwang)>=3:
                GameGUI.gwang(self.window, player, len(player.gwang))
        if list(filter(lambda c:c.special=="godori", getcards)) != []:
            if player.haveAllGodori():
                GameGUI.godori(self.window, player)
        if list(filter(lambda c:c.special=="red", getcards)) != []:
            if player.haveAllRed():
                GameGUI.reddan(self.window, player)
        if list(filter(lambda c:c.special=="blue", getcards)) != []:
            if player.haveAllBlue():
                GameGUI.bluedan(self.window, player)
        if list(filter(lambda c:c.special=="cho", getcards)) != []:
            if player.haveAllCho():
                GameGUI.chodan(self.window, player)
        QtTest.QTest.qWait(1000)
        if(bomb):
            player.gethandbombs()  
        if player.score_go < player.score and 7<=player.score:
            if len(player.hand) == 0:
                return self.gameresult(winner=player)
            else:
                go = self.askgo(player)
                if not go:
                    return self.gameresult(winner=player)
                else:
                    player.addgo()
                    QtTest.QTest.qWait(1000)
        if(len(self.player1.hand)==0 and len(self.player2.hand)==0):
            return self.gameresult(winner=None)

    def gameresult(self, winner=None, special=None):
        if not winner:
            print("무승부")
        elif winner.isEnemy:
            print("패배")
        else:
            print("승리")
        return True
    
    def askgo(self, player):
        if player.isEnemy:
            return random.randrange(2)
        else:
            # return GameGUI.askgo(self.window, player)
            return False

    def whattoget(self, player, cards):
        if player.isEnemy:
            return random.randrange(2)
        else:
            # return GameGUI.whattoget(self.window, cards)
            return 0

    def selectdual(self, player):
        if player.isEnemy:
            return ["aniaml", "pee"][random.randrange(2)]
        else:
            # return GameGUI.selectdual(self.window)
            return "pee"

def init(window):
    for components in window.findChildren(QPushButton): # remove Start / Exit Buttons
        components.setParent(None)
    controller = Game(window)
    controller.ready()
    controller.start()
    ScreenGUI.singleGameScreen(window)