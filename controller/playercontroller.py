import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "model"))
from player import Player as Playermodel
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "view"))
from GUI_game import Status, PlayerGUI

class Player(Playermodel, Status, PlayerGUI): # Model - View connector
    def __init__(self, window, isEnemy, field):
        self.window = window
        Status.__init__(self, window, isEnemy=isEnemy)
        player = Playermodel.__init__(self, isEnemy=isEnemy)
        PlayerGUI.__init__(self, window, player, field)
        self.update()
    

    def gethand(self, cards):
        if type(cards) is list:
            for card in cards:
                self.gethand(card)
        else:
            Playermodel.gethand(self, cards)
            PlayerGUI.tohand(self, cards, len(self._hand)-1)
    
    def arrange(self):
        Playermodel.arrange(self)
        for slot in range(len(self._hand)):
            PlayerGUI.tohand(self, self._hand[slot], slot, True)
    
    def getCard(self, cards):
        if type(cards) is list:
            while cards != []:
                self.getCard(cards.pop())
            self.update()
        else:
            Playermodel.getCard(self, cards)
            PlayerGUI.toplayer(self, cards)
    
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
            self._status.setText('\n뻑 : {}번\n점수 : {}점\n흔들기 : {}번\n\n'.format(self._fuckcount, self._score, self._shakecount))
        else:
            self._status.setText('\n뻑 : {}번\n점수 : {}점\n흔들기 : {}번\n현재 {}고\n'.format(self._fuckcount, self._score, self._shakecount, self._gocount))
        self._gwanglabel.setText(len(self._gwang))
        self._animallabel.setText(len(self._animal))
        self._danlabel.setText(len(self._dan))
        pee = list(filter(lambda c:c.special==None, self._pee))
        double = list(filter(lambda c:c.special=="double", self._pee))
        self._peelabel.setText(len(self._pee), len(pee) + 2*len(double))

    def addgo(self):
        Playermodel.addgo(self)
        PlayerGUI.go(self, self._gocount)

    def gethandbombs(self):
        Playermodel.gethandbombs(self)
        for card in self._hand[-2:]:
            card.setParent(self.window)
            card.show()
        self.arrange()