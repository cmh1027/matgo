from card import *
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
        deck.append(Card(window, "gwang", 1))
        deck.append(Card(window, "gwang", 3))
        deck.append(Card(window, "gwang", 8))
        deck.append(Card(window, "gwang", 11))
        deck.append(Card(window, "gwang", 12, "bee"))
        # dan
        deck.append(Card(window, "dan", 4, "cho"))
        deck.append(Card(window, "dan", 5, "cho"))
        deck.append(Card(window, "dan", 7, "cho"))
        deck.append(Card(window, "dan", 6, "blue"))
        deck.append(Card(window, "dan", 9, "blue"))
        deck.append(Card(window, "dan", 10, "blue"))
        deck.append(Card(window, "dan", 1, "red"))
        deck.append(Card(window, "dan", 2, "red"))
        deck.append(Card(window, "dan", 3, "red"))
        deck.append(Card(window, "dan", 12))
        # animal
        deck.append(Card(window, "animal", 2, "godori"))
        deck.append(Card(window, "animal", 4, "godori"))
        deck.append(Card(window, "animal", 8, "godori"))
        deck.append(Card(window, "animal", 5))
        deck.append(Card(window, "animal", 6))
        deck.append(Card(window, "animal", 7))
        deck.append(Card(window, "animal", 10))
        deck.append(Card(window, "animal", 12))
        # pee
        deck.append(Card(window, "pee", 11, "double"))
        deck.append(Card(window, "pee", 12, "double"))
        for month in range(1, 12):
            deck.append(Card(window, "pee", month, None, 1))
            deck.append(Card(window, "pee", month, None, 2))
        # dual
        deck.append(Card(window, "dual", 9))
        random.shuffle(deck)
        return deck

class Field(Deck):
    def __init__(self, window):
        super().__init__(window)
        self._field = [[], [], [], [], [], [], [], [], [], [], [], []]
    
    @property
    def current(self):
        return self._field
    
    def exist(self, card):
        for slot in self._field:
            if len(slot) > 0:
                if slot[0].month == card.month:
                    return True
        return False

    def pop(self, slot, pos=None):
        if type(pos) is int:
            return self._field[slot].pop(pos)
        elif type(pos) is list:
            li = []
            while pos != []:
                li.append(self._field[slot].pop(max(pos)))
                pos.remove(max(pos))
            return li
        else:
            li = []
            li.extend(self._field[slot])
            self._field[slot].clear()
            return li

    def put(self, card, arrange=True): # arrange is false only when initially cards are distributed
        if type(card) is list:
            for c in card:
                self.put(c, arrange)
        else:
            if arrange:
                for p in range(12):
                    for c in self._field[p]:
                        if c.month == card.month:
                            self._field[p].append(card)
                            return {"slot":p, "pos":len(self._field[p])} 
                            # Position of put card and the number of cards in it
                for p in range(12):
                    if len(self._field[p])==0:
                        self._field[p].append(card)
                        return {"slot":p, "pos":len(self._field[p])}
            else:
                for p in range(12):
                    if len(self._field[p]) == 0:
                        self._field[p].append(card)
                        return {"slot":p, "pos":len(self._field[p])}

    def arrange(self): # Add chongtong case later on
        for i in range(11, 0, -1):
            for p in range(i):
                if len(self._field[p])!=0 and len(self._field[i])!=0:
                    if self._field[p][0].month == self._field[i][0].month:
                        for _ in range(len(self._field[i])):
                            card = self._field[i].pop()
                            self._field[p].append(card)
                        break