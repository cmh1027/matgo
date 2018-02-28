import GUI_game as GameGUI
from card import *
from PyQt4.QtGui import *
soundPath = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "view")
from GUI_game import Status

class Player(Status):
    def __init__(self, window, isEnemy=None):
        super().__init__(window, isEnemy)
        self.window = window
        self.__hand = []
        self.__gwang = []
        self.__animal = []
        self.__dan = []
        self.__pee = []
        self.__score = 0
        self.__score_go = 0 # Check if the player gets scores
        self.__shake = 0
        self.__fuck = 0
        self.__go = 0
        self.__isEnemy = isEnemy
        self.__fuckmonth = []
        self.update()

    @property
    def hand(self):
        return self.__hand
    @property
    def gwang(self):
        return self.__gwang
    @property
    def animal(self):
        return self.__animal
    @property
    def dan(self):
        return self.__dan
    @property
    def pee(self):
        return self.__pee
    @property
    def shake(self):
        return self.__shake
    @property
    def score(self):
        return self.__score
    @property
    def score_go(self):
        return self.__score_go
    @property
    def fuck(self):
        return self.__fuck
    @property
    def go(self):
        return self.__go
    @property
    def money(self):
        return self.__money
    @property
    def isEnemy(self):
        return self.__isEnemy
    @property
    def fuckmonth(self):
        return self.__fuckmonth
    
    def addshake(self):
        self.__shake+=1
        self.update()
    
    def addfuck(self):
        self.__fuck+=1
        self.update()

    def addgo(self):
        self.__go+=1
        self.update()
        self.__score_go = self.__score

    def addfuckmonth(self, month):
        self.__fuckmonth.append(month)

    def isChongtong(self):
        for i in range(1, 13):
            li = list(filter(lambda c : c.month == i, self.__hand))
            if len(li) == 4:
                return li
        return False
    
    def haveFourCards(self):
        for month in range(1, 13):
            li = list(filter(lambda c : c.month == month, self.__hand))
            if len(li) == 4:
                return li
        return False

    def haveThreeCards(self, card):
        li = list(filter(lambda c : c.month == card.month, self.__hand))
        if len(li) == 3:
            return li
        else:
            return False

    def haveAllGodori(self):
        li = list(filter(lambda c : c.special == "godori", self.__animal))
        if len(li) == 3:
            return li
        else:
            return False
    
    def haveAllCho(self):
        li = list(filter(lambda c : c.special == "cho", self.__dan))
        if len(li) == 3:
            return li
        else:
            return False
    
    def haveAllRed(self):
        li = list(filter(lambda c : c.special == "red", self.__dan))
        if len(li) == 3:
            return li
        else:
            return False
    
    def haveAllBlue(self):
        li = list(filter(lambda c : c.special == "blue", self.__dan))
        if len(li) == 3:
            return li
        else:
            return False

    def haveBee(self):
        return len(list(filter(lambda c : c.special == "bee", self.__gwang)))

    def haveCard(self, card):
        return card in self.__hand or card in self.__gwang or card in self.__animal or card in self.__dan or card in self.__pee

    def gethand(self, cards, recur=False):
        if type(cards) is list:
            for card in cards:
                self.gethand(card)
        else:
            self.__hand.append(cards)
            GameGUI.tohand(cards, len(self.__hand)-1, self)

    def gethandbombs(self):
        self.gethand([Card(self.window, "bomb"), Card(self.window, "bomb")])

    def put(self, slot):
        if type(slot) is int:
            selected = self.__hand.pop(slot)
            self.arrange()
            return selected
        else:
            self.__hand.remove(slot)
            self.arrange()
            return slot
            
    
    def at(self, slot):
        return self.__hand[slot]

    def arrange(self):
        self.__hand.sort(key=lambda card:card.month)
        for slot in range(len(self.__hand)):
            GameGUI.tohand(self.__hand[slot], slot, self, True)

    def getCard(self, cards):
        if type(cards) is list:
            while cards != []:
                self.getCard(cards.pop())
            self.update()
        else:
            if cards.prop == "gwang":
                self.__gwang.append(cards)
            elif cards.prop == "animal":
                self.__animal.append(cards)
            elif cards.prop == "dan":
                self.__dan.append(cards)
            else:
                self.__pee.append(cards)
            GameGUI.toplayer(cards, self)
    
    def rob(self, count):
        def one():
            return list(filter(lambda c:c.special==None, self.__pee))
        def double():
            return list(filter(lambda c:c.special=="double", self.__pee))
        def arrangepee():
            li = []
            li.extend(self.__pee)
            self.__pee.clear()
            for card in li:
                self.__pee.append(card)
                GameGUI.topee(card, self)
        li = []
        while count > 0:
            if count == 1:
                if len(one()) == 0:
                    if len(double()) > 0:
                        li.append(double().pop())
                        self.__pee.remove(double().pop())
                        break
                    else:
                        break
                else:
                    li.append(one().pop())
                    self.pee.remove(one().pop())
                    break
            else:
                if len(double()) > 0:
                    li.append(double().pop())
                    self.__pee.remove(double().pop())
                    count -= 2
                else:
                    if len(one()) > 2:
                        li.append(one().pop())
                        self.pee.remove(one().pop())
                        li.append(one().pop())
                        self.pee.remove(one().pop())
                        count -= 2
                    elif len(one()) == 1:
                        li.append(one().pop())
                        self.pee.remove(one().pop())
                        break
                    else:
                        break
        arrangepee()
        self.update()
        return li

    def update(self):
        score = 0
        if len(self.__gwang) == 3:
            if list(filter(lambda c:c.special=="bee", self.__gwang)) != []:
                score += 2
            else:
                score += 3
        elif len(self.__gwang) == 4:
            score += 4
        elif len(self.__gwang) == 5:
            score += 15
        if self.haveAllGodori():
            score += 5
        if len(self.__animal) >= 5:
            score += len(self.__animal) - 4
        if self.haveAllRed():
            score += 3
        if self.haveAllBlue():
            score += 3
        if self.haveAllCho():
            score += 3
        if len(self.__dan) >= 5:
            score += len(self.__dan) - 4
        pee = list(filter(lambda c:c.special==None, self.__pee))
        double = list(filter(lambda c:c.special=="double", self.__pee))
        if len(pee) + 2*len(double) >= 10:
            score += len(pee) + 2*len(double) - 9
        score += self.__go
        if self.__go >= 3:
            score *= 2**((self.__go-2)*(self.__go-1)/2)
        self.__score = int(score)
        if self.__go == 0:
            self.status.setText('\n뻑 : {}번\n점수 : {}점\n흔들기 : {}번\n\n'.format(self.__fuck, self.__score, self.__shake))
        else:
            self.status.setText('\n뻑 : {}번\n점수 : {}점\n흔들기 : {}번\n현재 {}고\n'.format(self.__fuck, self.__score, self.__shake, self.__go))
        self.gwanglabel.setText(len(self.__gwang))
        self.animallabel.setText(len(self.__animal))
        self.danlabel.setText(len(self.__dan))
        self.peelabel.setText(len(self.__pee), len(pee) + 2*len(double))