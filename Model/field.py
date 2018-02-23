from card import *
class Deck:
    def __init__(self):
        self._deck = Card.fresh_deck()

    def Deckpop(self):
        if self._deck != []:
            return self._deck.pop()
        else:
            return None

    @property
    def Decktop(self):
        if self._deck != []:
            return self._deck[-1]
        else:
            return None

    @property
    def Deck(self):
        return self._deck

class Field(Deck):
    def __init__(self):
        super().__init__()
        self.__field = [[], [], [], [], [], [], [], [], [], [], [], []]
    
    @property
    def current(self):
        return self.__field
    
    def putCard(self, card, arrange=True): # arrange is false only when initially cards are distributed 
        if arrange:
            for p in range(12):
                for c in self.__field[p]:
                    if c.month == card.month:
                        self.__field[p].append(card)
                        return (p, len(self.__field[p])) # (pos, count of overlapped cards)
            for p in self.__field:
                if len(p)==0:
                    p.append(card)
                    return (p, len(self.__field[p])) # (pos, 1)
        else:
            for p in self.__field:
                if len(p) == 0:
                    p.append(card)
                    return
    
    def arrange(self):
        for i in range(7, -1, -1):
            for k in range(i):
                if len(self.__field[k])!=0:
                    if self.__field[k][0].month == self.__field[i][0].month:
                        self.__field[k].append(self.__field[i].pop())
                        break