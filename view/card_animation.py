from PyQt4.QtGui import *
import os

def tofield(card, slot, pos):
    card.flip()
    card.move(10+slot//2*55+5*pos+20*(slot%2), 150+85*(slot%2)+5*pos)
def tohand(card, slot, isEnemy):
    card.flip()
    if isEnemy:
        card.move(476+(slot%5)*40, 5+68*(slot//5))
    else:
        card.move(476+(slot%5)*40, 326+68*(slot//5))
def togwang(card, slot, isEnemy):
    pass

def toanimal(card, slot, isEnemy):
    pass

def todan(card, slot, isEnemy):
    pass

def topee(card, slot, isEnemy):
    pass