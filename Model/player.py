from card import *

class Player():
    def __init__(self, isEnemy=None):
        self._hand = []
        self._gwang = []
        self._animal = []
        self._dan = []
        self._pee = []
        self._score = 0
        self._score_go = 0 # Check if the player gets scores
        self._shakecount = 0
        self._fuckcount = 0
        self._gocount = 0
        self._isEnemy = isEnemy
        self._fuckcountmonth = []
        return self

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
    def singlepee(self):
        return list(filter(lambda c:c.special==None, self._pee))
    @property
    def doublepee(self):
        return list(filter(lambda c:c.special=="double", self._pee))    
    @property
    def shakecount(self):
        return self._shakecount
    @property
    def score(self):
        return self._score
    @property
    def score_go(self):
        return self._score_go
    @property
    def fuckcount(self):
        return self._fuckcount
    @property
    def gocount(self):
        return self._gocount
    @property
    def money(self):
        return self._money
    @property
    def isEnemy(self):
        return self._isEnemy
    @property
    def fuckmonth(self):
        return self._fuckcountmonth
    
    def addshake(self):
        self._shakecount+=1
        self.update()
    
    def addfuck(self):
        self._fuckcount+=1
        self.update()

    def addgo(self):
        self._gocount+=1
        self.update()
        self._score_go = self._score


    def addfuckmonth(self, month):
        self._fuckcountmonth.append(month)

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
        self.gethand([Card("bomb", 13), Card("bomb", 13)])

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
        li = []
        while count > 0:
            if count == 1:
                if len(self.singlepee) == 0:
                    if len(self.doublepee) > 0:
                        li.append(self.doublepee.pop())
                        self._pee.remove(self.doublepee.pop())
                        break
                    else:
                        break
                else:
                    li.append(self.singlepee.pop())
                    self.pee.remove(self.singlepee.pop())
                    break
            else:
                if len(self.doublepee) > 0:
                    li.append(self.doublepee.pop())
                    self._pee.remove(self.doublepee.pop())
                    count -= 2
                else:
                    if len(self.singlepee) > 2:
                        li.append(self.singlepee.pop())
                        self.pee.remove(self.singlepee.pop())
                        li.append(self.singlepee.pop())
                        self.pee.remove(self.singlepee.pop())
                        count -= 2
                    elif len(self.singlepee) == 1:
                        li.append(self.singlepee.pop())
                        self.pee.remove(self.singlepee.pop())
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
        score += self._gocount
        if self._gocount >= 3:
            score *= 2**((self._gocount-2)*(self._gocount-1)/2)
        self._score = int(score)