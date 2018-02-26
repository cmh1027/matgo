import card_animation as Animation
class Player:
    def __init__(self, isEnemy=None):
        self.__hand = [];
        self.__gwang = [];
        self.__animal = [];
        self.__dan = [];
        self.__pee = [];
        self.__shake = 0;
        self.__fuck = 0;
        self.__go = 0;
        self.__isEnemy = isEnemy
    
    def getCard(self, card):
        self.__hand.append(card)
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
    def fuck(self):
        return self.__fuck
    @property
    def go(self):
        return self.__go
    @property
    def money(self):
        return self.__money
    
    def add_shake(self):
        self.__shake+=1
    def add_fuck(self):
        self.__fuck+=1
    def add_go(self):
        self.__go+=1
    
    def isChongtong(self):
        for i in range(1, 13):
            li = list(filter(lambda c : c.month == i, self.__hand))
            if len(li) == 4:
                return li
        return False

    def haveThreeCards(self, card):
        li = list(filter(lambda c : c.month == card.month, self.__hand))
        if len(li) >= 3:
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

    def gethand(self, cards):
        if type(cards) is list:
            for card in cards:
                self.gethand(card)
        else:
            self.__hand.append(cards)
            Animation.tohand(cards, len(self.__hand)-1, self.__isEnemy)

    def arrange(self):
        self.__hand.sort(key=lambda card:card.month)
        for slot in range(len(self.__hand)):
            Animation.tohand(self.__hand[slot], slot, self.__isEnemy)
    
    def getCard(self, cards, dual=None):
        if type(cards) is list:
            for card in cards:
                self.getCard(card)
        else:
            if cards.prop == "gwang":
                self.__gwang.append(cards)
            elif cards.prop == "animal":
                self.__animal.append(cards)
            elif cards.prop == "dan":
                self.__dan.append(cards)
            elif cards.prop == "pee":
                self.__pee.append(cards)
            else: # dual
                if dual=="animal" :
                    self.__animal.append(cards)
                elif dual=="pee":
                    self.__pee.append(cards)
                else:
                    self.__pee.append(cards)
                    print("Warning : dual flag is not set")