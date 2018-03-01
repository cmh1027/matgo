import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "model"))
from field import Field as Fieldmodel
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "view"))
from GUI_game import FieldGUI

class Field(Fieldmodel, FieldGUI): # Model - View connector
    def __init__(self, window):
        Fieldmodel.__init__(self)
        FieldGUI.__init__(self, window)
        for card in self._deck:
            card.setParent(window)
            card.move(350, 200)
            card.show()

    def pop(self, slot, pos=None):
        if type(pos) is list:
            li = Fieldmodel.pop(self, slot, pos)
            for i in range(len(self._field[slot])):
                FieldGUI.tofield(self, self._field[slot][i], slot, i)
            return li
        else:
            return Fieldmodel.pop(self, slot, pos)

    def put(self, card, arrange=True): # arrange is false only when initially cards are distributed
        if type(card) is list:
            for c in card:
                self.put(c, arrange)
        else:
            if arrange:
                result = Fieldmodel.put(self, card, arrange)
                FieldGUI.tofield(self, card, result["slot"], len(self._field[result["slot"]])-1)
                self.arrange(result["slot"])
                return result
            else:
                result = Fieldmodel.put(self, card, arrange)
                FieldGUI.tofield(self, card, result["slot"], len(self._field[result["slot"]])-1)
                return result

    def arrange(self, slot=None):
        if slot:
            for pos in range(len(self._field[slot])):
                self._field[slot][pos].raise_()
        else:
            Fieldmodel.arrange(self)
            for slot in range(len(self._field)):
                for pos in range(len(self._field[slot])):
                    self._field[slot][pos].raise_()
                    FieldGUI.tofield(self, self._field[slot][pos], slot, pos, True)