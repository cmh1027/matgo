import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "model"))
from player import Player as Playermodel
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "view"))
from GUI_game import PlayerGUI
from PyQt4.QtTest import QTest
class Player(Playermodel, PlayerGUI): # Model - View connector
    def __init__(self, parent, isEnemy, field):
        self.parent = parent
        parent.addstatus.emit(isEnemy)
        player = Playermodel.__init__(self, isEnemy=isEnemy)
        PlayerGUI.__init__(self, parent, player, field)
        self.update()

    def gethand(self, cards, arrange=False):
        if type(cards) is list:
            for card in cards:
                self.gethand(card, arrange)
        else:
            Playermodel.gethand(self, cards)
            PlayerGUI.tohand(self, cards, len(self._hand)-1, arrange)
    
    def arrange(self):
        Playermodel.arrange(self)
        for slot in range(len(self._hand)):
            PlayerGUI.tohand(self, self._hand[slot], slot, True)
    
    def getCard(self, cards):
        Playermodel.getCard(self, cards)
        PlayerGUI.toplayer(self, cards)
        self.update()
    
    def rob(self, count):
        def arrangepee():
            li = []
            li.extend(self._pee)
            self._pee.clear()
            for card in li:
                self._pee.append(card)
                PlayerGUI.topee(self, card)
        cards = Playermodel.rob(self, count)
        arrangepee()
        self.update()
        return cards
    
    def update(self):
        Playermodel.update(self)
        if self._gocount == 0:
            status = '\n뻑 : {}번\n점수 : {}점\n흔들기 : {}번\n\n'.format(self._fuckcount, self._score, self._shakecount)
        else:
            status = '\n뻑 : {}번\n점수 : {}점\n흔들기 : {}번\n현재 {}고\n'.format(self._fuckcount, self._score, self._shakecount, self._gocount)
        gwang = len(self._gwang)
        animal = len(self._animal)
        dan = len(self._dan)
        peenum = len(self._pee)
        peesum = len(list(filter(lambda c:c.special==None, self._pee))) + 2*len(list(filter(lambda c:c.special=="double", self._pee)))
        self.parent.updatestatus.emit(self.isEnemy, status, gwang, animal, dan, peenum, peesum)

    def addgo(self):
        Playermodel.addgo(self)
        PlayerGUI.go(self, self._gocount)
    
    def stop(self):
        PlayerGUI.stop(self)

    def gethandbombs(self):
        Playermodel.gethandbombs(self)
        for card in self._hand[-2:]:
            self.parent.addcard.emit(card)
        self.arrange()