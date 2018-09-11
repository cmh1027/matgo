import random
import os
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtTest
from playercontroller import Player
from fieldcontroller import Field
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "model"))
from card import Card

class Game(QThread):
    playsound = pyqtSignal(str)
    addstatus = pyqtSignal(bool)
    updatestatus = pyqtSignal(bool, str, int, int, int, int, int)
    addcard = pyqtSignal(Card)
    removecard = pyqtSignal(Card)
    flipcard = pyqtSignal(Card)
    raisecard = pyqtSignal(Card)
    movecard = pyqtSignal(Card, int, int) # x, y
    setparent = pyqtSignal(QWidget)
    shake = pyqtSignal(list, int, int)
    chongtong = pyqtSignal(list, int, int)
    result = pyqtSignal(str, int, int, list, int)
    endgame = pyqtSignal(dict) # winner
    attacheventhand = pyqtSignal(list, Field)

    def __init__(self, panmoney=None, winner=None, draw=0, push=0):
        super().__init__()
        self.waitforResponse = False
        self.answer = None
        if panmoney:
            self.__panmoney = panmoney
        else:
            self.__panmoney = 1000
        if winner == None:
            self.__myturn = random.randrange(2)
        elif winner:
            self.__myturn = True
        else:
            self.__myturn = False
        self.__draw = draw
        self.__push = push

    @property
    def draw(self):
        return self.__draw
    @property
    def push(self):
        return self.__push
    
    def run(self):
        self.begin()

    def begin(self):
        self.__field = Field(self)
        self.__me = Player(self, False, self.__field)
        self.__enemy = Player(self, True, self.__field)
        for _ in range(2):
            self.playsound.emit("whoop")
            self.__field.put(self.__field.deckpop(count=4), False)
            QtTest.QTest.qWait(500)
            self.playsound.emit("whoop")
            self.__me.gethand(self.__field.deckpop(count=5), True)
            QtTest.QTest.qWait(500)
            self.playsound.emit("whoop")
            self.__enemy.gethand(self.__field.deckpop(count=5), True)
            QtTest.QTest.qWait(500)
        self.playsound.emit("start")
        self.__field.arrange()
        self.__me.arrange()
        self.__enemy.arrange()
        QtTest.QTest.qWait(2000)
        # check chongtong.
        fourcardcheck = (self.__me.haveFourCards(), self.__enemy.haveFourCards())
        if fourcardcheck[0] or fourcardcheck[1]:
            self.__me.chongtong(fourcardcheck[0], fourcardcheck[1])
            if fourcardcheck[0] and not fourcardcheck[1]:
                self.gameresult(winner=self.__me, special="chongtong")
                push = self.askpush(True)
                if push:
                    self.endgame.emit({"push":True, "winner":True})
                else:
                    self.endgame.emit({"push":False, "winner":True})
            elif not fourcardcheck[0] and fourcardcheck[1]:
                self.gameresult(winner=self.__enemy, special="chongtong")
                push = self.askpush(False)
                if push:
                    self.endgame.emit({"push":True, "winner":False})
                else:
                    self.endgame.emit({"push":False, "winner":False})
            else:
                self.gameresult(winner=None)
                self.endgame.emit({"push":False, "winner":None})
        else:
            # begin
            while True:
                end = self.turn(self.__myturn)
                self.__myturn = not self.__myturn
                if end != None: # Game ends
                    break
            if end!="draw":
                push = self.askpush(end)
                if push:
                    self.endgame.emit({"push":True, "winner":end})
                else:
                    self.endgame.emit({"push":False, "winner":end})
            else:
                self.endgame.emit({"push":False, "winner":None})

    def turn(self, myturn):
        if myturn:
            self.waitforResponse = True
            self.attacheventhand.emit(self.__me.hand, self.__field)
            while self.waitforResponse:
                QtTest.QTest.qWait(100)
            return self.select(self.__me, self.answer)
        else: # computer
            return self.select(self.__enemy, random.randrange(len(self.__enemy.hand)))

    def select(self, player, slot):
        selected = player.at(slot)
        bomb = False
        threeCards = player.haveThreeCards(selected)
        if threeCards:
            player.addshake()
            if self.__field.exist(selected): # Bomb
                bomb = True
                firstput = player.bomb(threeCards)
            else: # Shake
                player.shake(threeCards)
                firstput = self.__field.put(player.put(slot))
            QtTest.QTest.qWait(700)
        else:
            if selected.prop == "bomb":
                self.removecard.emit(player.put(slot))
                firstput = {"slot":None, "pos":None}
            else:
                firstput = self.__field.put(player.put(slot))
                if firstput["pos"] == 4:
                    QtTest.QTest.qWait(500)
                    if self.__field.current[firstput["slot"]][0].month in player.fuckmonth:
                        player.jafuck()
                    else:
                        player.getfuck()
                QtTest.QTest.qWait(700)
        secondput = self.__field.put(self.__field.deckpop())
        if secondput["pos"] == 4 and firstput["slot"] != secondput["slot"]:
            QtTest.QTest.qWait(300)
            if self.__field.current[secondput["slot"]][0].month in player.fuckmonth:
                player.jafuck()
            else:
                player.getfuck()
        QtTest.QTest.qWait(700)
        return self.process(player, firstput, secondput, bomb)

    def process(self, player, firstput, secondput, bomb):
        rob = 0
        getcards = []
        if firstput["slot"] == secondput["slot"]:
            if secondput["pos"] == 2: # Kiss
                rob+=1
                getcards.extend(self.__field.pop(firstput["slot"]))
                player.kiss()
            elif secondput["pos"] == 3: # Fuck
                player.addfuck()
                player.addfuckmonth(self.__field.current[firstput["slot"]][0].month)
                player.fuck()
                if player.fuck==3:
                    player.threefuck()
                    return self.gameresult(winner=player, special="threefuck")
            elif secondput["pos"] == 4: # Tadack
                rob+=1
                getcards.extend(self.__field.pop(firstput["slot"]))
                player.tadack()
        else:
            if firstput["pos"] == 4:
                if bomb:
                    rob+=1 # Bomb
                    getcards.extend(self.__field.pop(firstput["slot"]))
                else:
                    rob+=1 # Get fuck
                    if self.__field.current[firstput["slot"]][0].month in player.fuckmonth: # Jafuck
                        rob += 1
                    getcards.extend(self.__field.pop(firstput["slot"]))
            elif firstput["pos"] == 3:
                select = self.whattoget(player, self.__field.current[firstput["slot"]][0:2])
                getcards.extend(self.__field.pop(firstput["slot"], [select, 2]))
            elif firstput["pos"] == 2:
                getcards.extend(self.__field.pop(firstput["slot"]))
            if secondput["pos"] == 4: # Get fuck
                rob+=1
                if self.__field.current[secondput["slot"]][0].month in player.fuckmonth: # Jafuck
                    rob += 1
                getcards.extend(self.__field.pop(secondput["slot"]))
            elif secondput["pos"] == 3:
                select = self.whattoget(player, self.__field.current[secondput["slot"]][0:2])
                getcards.extend(self.__field.pop(secondput["slot"], [select, 2]))
            elif secondput["pos"] == 2:
                getcards.extend(self.__field.pop(secondput["slot"]))
        if player.isEnemy: 
            getcards.extend(self.__me.rob(rob))
        else:
            getcards.extend(self.__enemy.rob(rob))
        if list(filter(lambda c:c.prop=="dual", getcards)) != []: 
            dual = list(filter(lambda c:c.prop=="dual", getcards))[0]
            select = self.selectdual(player)
            if select == "animal":
                dual.propchange("animal")
            else:
                dual.propchange("pee")
        player.getCard(getcards)
        QtTest.QTest.qWait(500)
        if self.__field.isclear() and (len(self.__me.hand) != 0 or len(self.__enemy.hand) != 0):
            self.__field.clear()
        if list(filter(lambda c:c.prop=="gwang", getcards)) != []:
            if len(player.gwang)==3:
                if list(filter(lambda c:c.special=="bee", player.gwang)) == 0:
                    player.allgwang(len(player.gwang))
                else:
                    player.allgwang(len(player.gwang), True)
            elif len(player.gwang)>=4:
                player.allgwang(len(player.gwang))
        if list(filter(lambda c:c.special=="godori", getcards)) != []:
            if player.haveAllGodori():
                player.allgodori()
        if list(filter(lambda c:c.special=="red", getcards)) != []:
            if player.haveAllRed():
                player.allreddan()
        if list(filter(lambda c:c.special=="blue", getcards)) != []:
            if player.haveAllBlue():
                player.allbluedan()
        if list(filter(lambda c:c.special=="cho", getcards)) != []:
            if player.haveAllCho():
                player.allchodan()
        QtTest.QTest.qWait(500)
        if(bomb):
            player.gethandbombs()
        if player.score_go < player.score and 7<=player.score:
            if len(player.hand) == 0:
                return self.gameresult(winner=player)
            else:
                go = self.askgo(player)
                if not go:
                    player.stop()
                    return self.gameresult(winner=player)
                else:
                    player.addgo()
                    QtTest.QTest.qWait(1000)
        if(len(self.__me.hand)==0 and len(self.__enemy.hand)==0):
            return self.gameresult(winner=None)


    def gameresult(self, winner=None, special=None):
        def enemy(player):
            if player.isEnemy:
                return self.__me
            else:
                return self.__enemy
        if winner == None:
            self.__me.result({"winner":None})
            return "draw"
        else:
            messages = []
            money = self.__panmoney
            if special == "chongtong":
                messages.append("총통 x4")
                money *= 4
                self.__me.result({"winner":not winner.isEnemy, "messages":messages, "money":money})
            elif special == "threefuck":
                messages.append("쓰리뻑 x4")
                money *= 4
                self.__me.result({"winner":not winner.isEnemy, "messages":messages, "money":money})
            else:
                if self.__draw > 0:
                    messages.append("나가리 {}번 x{}".format(self.__draw, 2**(self.__draw)))
                    money *= 2**self.__draw
                if self.__push > 0:
                    messages.append("{}번 밀음 x{}".format(self.__push, 2**(self.__draw)))
                    money *= 2**self.__push
                if enemy(winner).gocount > 0:
                    messages.append("역고 x{}".format(2**enemy(winner).gocount))
                    money *= 2**enemy(winner).gocount
                if winner.shakecount > 0:
                    messages.append("흔들기 {}번 x{}".format(winner.shakecount, 2**winner.shakecount))
                    money *= 2**winner.shakecount
                if len(winner.animal) >= 7:
                    messages.append("멍따 x2")
                    money *= 2
                if len(enemy(winner).gwang) <= 2 and len(winner.gwang) >= 3:
                    messages.append("광박 x2")
                    money *= 2
                if len(winner.singlepee) + 2*len(winner.doublepee) >= 10 and \
                len(enemy(winner).singlepee) + 2*len(enemy(winner).singlepee) <= 7:
                    messages.append("피박 x2")
                    money *= 2
                if len(winner.animal) >= 5 and len(enemy(winner).animal) < 5:
                    messages.append("멍박 x2")
                    money *= 2
                if len(winner.dan) >= 5 and len(enemy(winner).dan) < 5:
                    messages.append("띠박 x2")
                    money *= 2
                messages.append("총 {}점".format(winner.score))
                money *= winner.score
                self.__me.result({"winner":not winner.isEnemy, "messages":messages, "money":money})
            return winner == self.__me

    def askgo(self, player):
        if player.isEnemy:
            return 1
        else:
            return player.askgo()

    def whattoget(self, player, cards):
        if player.isEnemy:
            return random.randrange(2)
        else:
            return player.whattoget(cards)

    def selectdual(self, player):
        if player.isEnemy:
            return ["aniaml", "pee"][random.randrange(2)]
        else:
            return player.selectdual()
    
    def askpush(self, win):
        if win == False:
            return False
        else:
            return self.__me.askpush()