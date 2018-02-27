import GUI_game as GameGUI
from card import *
class Player:
    def __init__(self, window, isEnemy=None):
        self.window = window
        self.__hand = [];
        self.__gwang = [];
        self.__animal = [];
        self.__dan = [];
        self.__pee = [];
        self.__score = 0
        self.__shake = 0;
        self.__fuck = 0;
        self.__go = 0;
        self.__isEnemy = isEnemy
        self.__fuckmonth = []

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
    def addfuck(self):
        self.__fuck+=1
    def addgo(self):
        self.__go+=1
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
        li = []
        for i in range(len(self.__hand)):
            if card.month == self.__hand[i]:
                li.append(i)
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

    def doubleCount(self):
        return len(list(filter(lambda c : c.special == "double" or c.special == "dual", self.__pee)))

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
        selected = self.__hand.pop(slot)
        self.arrange()
        return selected
    
    def at(self, slot):
        return self.__hand[slot]

    def arrange(self):
        self.__hand.sort(key=lambda card:card.month)
        for slot in range(len(self.__hand)):
            GameGUI.tohand(self.__hand[slot], slot, self, True)
    
    def getCard(self, cards):
        if type(cards) is list:
            while cards != []
                self.getCard(cards.pop())
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
        pass