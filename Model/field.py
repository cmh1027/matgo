from card import *
import card_animation as Animation
class Deck:
    def __init__(self, window):
        self._deck = Deck.fresh_deck(window)

    def deckpop(self, count=None):
        if count:
            res = []
            for _ in range(count):
                if self._deck == []:
                    return res
                res.append(self._deck.pop())
            return res
        else:
            if self._deck != []:
                return self._deck.pop()
            else:
                return None

    @property
    def decktop(self):
        if self._deck != []:
            return self._deck[-1]
        else:
            return None

    @property
    def deck(self):
        return self._deck

    @staticmethod
    def fresh_deck(window):
        deck = []
        # gwang
        deck.append(Card(window, "gwang", None, 1))
        deck.append(Card(window, "gwang", None, 3))
        deck.append(Card(window, "gwang", None, 8))
        deck.append(Card(window, "gwang", None, 11))
        deck.append(Card(window, "gwang", "bee", 12))
        # dan
        deck.append(Card(window, "dan", "cho", 4))
        deck.append(Card(window, "dan", "cho", 5))
        deck.append(Card(window, "dan", "cho", 7))
        deck.append(Card(window, "dan", "blue", 6))
        deck.append(Card(window, "dan", "blue", 9))
        deck.append(Card(window, "dan", "blue", 10))
        deck.append(Card(window, "dan", "red", 1))
        deck.append(Card(window, "dan", "red", 2))
        deck.append(Card(window, "dan", "red", 3))
        deck.append(Card(window, "dan", None, 12))
        # animal
        deck.append(Card(window, "animal", "godori", 2))
        deck.append(Card(window, "animal", "godori", 4))
        deck.append(Card(window, "animal", "godori", 8))
        deck.append(Card(window, "animal", None, 5))
        deck.append(Card(window, "animal", None, 6))
        deck.append(Card(window, "animal", None, 7))
        deck.append(Card(window, "animal", None, 10))
        deck.append(Card(window, "animal", None, 12))
        # pee
        deck.append(Card(window, "pee", "double", 11))
        deck.append(Card(window, "pee", "double", 12))
        for month in range(1, 12):
            deck.append(Card(window, "pee", None, month, 1))
            deck.append(Card(window, "pee", None, month, 2))
        # dual
        deck.append(Card(window, "dual", None, 9))
        random.shuffle(deck)
        return deck

class Field(Deck):
    def __init__(self, window):
        super().__init__(window)
        self.__field = [[], [], [], [], [], [], [], [], [], [], [], []]
    
    @property
    def current(self):
        return self.__field
    
    def putcard(self, card, arrange=True): # arrange is false only when initially cards are distributed
        if type(card) is list:
            for c in card:
                self.putcard(c, arrange)
        else:
            if arrange:
                for p in range(12):
                    for c in self.__field[p]:
                        if c.month == card.month:
                            self.__field[p].append(card)
                            Animation.tofield(card, p, len(self.__field[p])-1)
                            return {"slot":p, "len":len(self.__field[p])-1} 
                            # Position of put card and the number of cards in it
                for p in range(12):
                    if len(self.__field[p])==0:
                        self.__field[p].append(card)
                        Animation.tofield(card, p, len(self.__field[p])-1)
                        return {"slot":p, "len":len(self.__field[p])-1}
            else:
                for p in range(12):
                    if len(self.__field[p]) == 0:
                        self.__field[p].append(card)
                        Animation.tofield(card, p, len(self.__field[p])-1)
                        return {"slot":p, "len":len(self.__field[p])-1}

    def arrange(self): # Add chongtong case later on
        for i in range(11, 0, -1):
            for p in range(i-1):
                if len(self.__field[p])!=0 and len(self.__field[i])!=0:
                    if self.__field[p][0].month == self.__field[i][0].month:
                        for _ in range(len(self.__field[i])):
                            card = self.__field[i].pop()
                            self.__field[p].append(card)
                        break
        for slot in range(len(self.__field)):
            for pos in range(len(self.__field[slot])):
                self.__field[slot][pos].raise_()
                Animation.tofield(self.__field[slot][pos], slot, pos)