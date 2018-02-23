class Player:
    def __init__(self, user):
        self.__hand = [];
        self.__gwang = [];
        self.__animal = [];
        self.__dan = [];
        self.__pee = [];
        self.__shake = 0;
        self.__fuck = 0;
        self.__go = 0;
        self.__user = user

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
    
    def hasThreeCards(self, card):
        return len(list(filter(lambda c : c.month == card.month, self.__hand))) == 3
    
    def hasAllGodori(self):
        return len(list(filter(lambda c : c.special == "godori")), self.__animal) == 3
    
    def hasAllCho(self):
        return len(list(filter(lambda c : c.special == "cho")), self.__dan) == 3
    
    def hasAllRed(self):
        return len(list(filter(lambda c : c.special == "red")), self.__dan) == 3
    
    def hasAllBlue(self):
        return len(list(filter(lambda c : c.special == "blue")), self.__dan) == 3

    def hasBee(self):
        return len(list(filter(lambda c : c.special == "bee", self.__gwang)))

    def doubleCount(self):
        return len(list(filter(lambda c : c.special == "double" or c.special == "dual", self.__pee)))

    def haveCard(self, card):
        return card in self.__hand or card in self.__gwang or card in self.__animal or card in self.__dan or card in self.__pee

    def getHand(self, cards):
        if cards is list:
            for card in cards:
                self.getHand(card)
        else:
            self.__hand.append(cards)
            self.__hand.sort(key=lambda card:card.month)
    
    def getCard(self, cards, dual=None):
        if cards is list:
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