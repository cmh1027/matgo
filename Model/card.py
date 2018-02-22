import random
class Card: 
    prop = ("gwang", "animal", "dan", "pee", "dual", "bomb")
    special = (None, "bee", "red", "blue", "cho", "godori", "double")
    month = (1,2,3,4,5,6,7,8,9,10,11,12)

    def __init__(self, prop, special, month, isfront, number=0):
        self.__prop = prop
        self.__special = special
        self.__month = month
        self.__isfront = isfront
        self.__number = number # for 2 pees
    def __str__(self):
        return self.__prop + "/" + str(self.__month)

    def flip(self):
        self.__isfront = not self.__isfront
    
    @property
    def prop(self):
        return self.__prop
    @property
    def special(self):
        return self.__special
    @property
    def month(self):
        return self.__month
    @property
    def isfront(self):
        return self.__isfront
    @property
    def imageName(self):
        if(self.__special):
            return str(self.__month) + "_" + self.__special + ".png"
        else:
            if(self.number):
                return str(self.__month) + "_" + self.__prop + str(self.__number) + ".png"
            else:
                return str(self.__month) + "_" + self.__prop + str(self.__number) + ".png"

    @staticmethod
    def fresh_deck():
        deck = []
        # gwang
        deck.append(Card("gwang", None, 1, False))
        deck.append(Card("gwang", None, 3, False))
        deck.append(Card("gwang", None, 8, False))
        deck.append(Card("gwang", None, 11, False))
        deck.append(Card("gwang", "bee", 12, False))
        # dan
        deck.append(Card("dan", "cho", 4, False))
        deck.append(Card("dan", "cho", 5, False))
        deck.append(Card("dan", "cho", 7, False))
        deck.append(Card("dan", "blue", 6, False))
        deck.append(Card("dan", "blue", 9, False))
        deck.append(Card("dan", "blue", 10, False))
        deck.append(Card("dan", "red", 1, False))
        deck.append(Card("dan", "red", 2, False))
        deck.append(Card("dan", "red", 3, False))
        deck.append(Card("dan", None, 12, False))
        # animal
        deck.append(Card("animal", "godori", 2, False))
        deck.append(Card("animal", "godori", 4, False))
        deck.append(Card("animal", "godori", 8, False))
        deck.append(Card("animal", None, 5, False))
        deck.append(Card("animal", None, 6, False))
        deck.append(Card("animal", None, 7, False))
        deck.append(Card("animal", None, 10, False))
        deck.append(Card("animal", None, 12, False))
        # pee
        deck.append(Card("pee", "double", 11, False))
        deck.append(Card("pee", "double", 12, False))
        for month in range(1, 12):
            deck.append(Card("pee", None, month, False, 1))
            deck.append(Card("pee", None, month, False, 2))
        # dual
        deck.append(Card("dual", None, 9, False))      

        random.shuffle(deck)
        return deck