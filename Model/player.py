from card import *

class Player():
    def __init__(self, window, isEnemy=None):
        self.window = window
        self._hand = []
        self._gwang = []
        self._animal = []
        self._dan = []
        self._pee = []
        self._score = 0
        self._score_go = 0 # Check if the player gets scores
        self._shake = 0
        self._fuck = 0
        self._go = 0
        self._isEnemy = isEnemy
        self._fuckmonth = []

    @property
    def hand(self):
        return self._hand
    @property
    def gwang(self):
        return self._gwang
    @property
    def animal(self):
        return self._animal
    @property
    def dan(self):
        return self._dan
    @property
    def pee(self):
        return self._pee
    @property
    def shake(self):
        return self._shake
    @property
    def score(self):
        return self._score
    @property
    def score_go(self):
        return self._score_go
    @property
    def fuck(self):
        return self._fuck
    @property
    def go(self):
        return self._go
    @property
    def money(self):
        return self._money
    @property
    def isEnemy(self):
        return self._isEnemy
    @property
    def fuckmonth(self):
        return self._fuckmonth
    
    def addshake(self):
        self._shake+=1
        self.update()
    
    def addfuck(self):
        self._fuck+=1
        self.update()

    def addgo(self):
        self._go+=1
        self.update()
        self._score_go = self._score

    def addfuckmonth(self, month):
        self._fuckmonth.append(month)

    def isChongtong(self):
        for i in range(1, 13):
            li = list(filter(lambda c : c.month == i, self._hand))
            if len(li) == 4:
                return li
        return False
    
    def haveFourCards(self):
        for month in range(1, 13):
            li = list(filter(lambda c : c.month == month, self._hand))
            if len(li) == 4:
                return li
        return False

    def haveThreeCards(self, card):
        li = list(filter(lambda c : c.month == card.month, self._hand))
        if len(li) == 3:
            return li
        else:
            return False

    def haveAllGodori(self):
        li = list(filter(lambda c : c.special == "godori", self._animal))
        if len(li) == 3:
            return li
        else:
            return False
    
    def haveAllCho(self):
        li = list(filter(lambda c : c.special == "cho", self._dan))
        if len(li) == 3:
            return li
        else:
            return False
    
    def haveAllRed(self):
        li = list(filter(lambda c : c.special == "red", self._dan))
        if len(li) == 3:
            return li
        else:
            return False
    
    def haveAllBlue(self):
        li = list(filter(lambda c : c.special == "blue", self._dan))
        if len(li) == 3:
            return li
        else:
            return False

    def haveBee(self):
        return len(list(filter(lambda c : c.special == "bee", self._gwang)))

    def haveCard(self, card):
        return card in self._hand or card in self._gwang or card in self._animal or card in self._dan or card in self._pee

    def gethand(self, cards):
        if type(cards) is list:
            for card in cards:
                self.gethand(card)
        else:
            self._hand.append(cards)

    def gethandbombs(self):
        self.gethand([Card(self.window, "bomb"), Card(self.window, "bomb")])

    def put(self, slot):
        if type(slot) is int: # slot is a number
            selected = self._hand.pop(slot)
            self.arrange()
            return selected
        else: # slot is a card object
            self._hand.remove(slot)
            self.arrange()
            return slot
            
    
    def at(self, slot):
        return self._hand[slot]

    def arrange(self):
        self._hand.sort(key=lambda card:card.month)


    def getCard(self, cards):
        if type(cards) is list:
            while cards != []:
                self.getCard(cards.pop())
            self.update()
        else:
            if cards.prop == "gwang":
                self._gwang.append(cards)
            elif cards.prop == "animal":
                self._animal.append(cards)
            elif cards.prop == "dan":
                self._dan.append(cards)
            else:
                self._pee.append(cards)
    
    def rob(self, count):
        def one():
            return list(filter(lambda c:c.special==None, self._pee))
        def double():
            return list(filter(lambda c:c.special=="double", self._pee))
        li = []
        while count > 0:
            if count == 1:
                if len(one()) == 0:
                    if len(double()) > 0:
                        li.append(double().pop())
                        self._pee.remove(double().pop())
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
                    self._pee.remove(double().pop())
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
        self.update()
        return li

    def update(self):
        score = 0
        if len(self._gwang) == 3:
            if list(filter(lambda c:c.special=="bee", self._gwang)) != []:
                score += 2
            else:
                score += 3
        elif len(self._gwang) == 4:
            score += 4
        elif len(self._gwang) == 5:
            score += 15
        if self.haveAllGodori():
            score += 5
        if len(self._animal) >= 5:
            score += len(self._animal) - 4
        if self.haveAllRed():
            score += 3
        if self.haveAllBlue():
            score += 3
        if self.haveAllCho():
            score += 3
        if len(self._dan) >= 5:
            score += len(self._dan) - 4
        pee = list(filter(lambda c:c.special==None, self._pee))
        double = list(filter(lambda c:c.special=="double", self._pee))
        if len(pee) + 2*len(double) >= 10:
            score += len(pee) + 2*len(double) - 9
        score += self._go
        if self._go >= 3:
            score *= 2**((self._go-2)*(self._go-1)/2)
        self._score = int(score)