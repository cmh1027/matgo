from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os
soundPath = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "view\sound")

def tohand(card, slot, player, arrange=False):
    card.flip()
    if player.isEnemy:
        card.move(476+(slot%5)*40, 5+68*(slot//5))
    else:
        card.move(476+(slot%5)*40, 326+68*(slot//5))
    if not arrange:
        QSound(os.path.join(soundPath, "whoop.wav")).play()

def tofield(card, slot, pos, arrange=False):
    card.flip()
    card.move(10+slot//2*55+5*pos+20*(slot%2), 150+85*(slot%2)+5*pos)
    if pos==0:
        if not arrange:
            QSound(os.path.join(soundPath, "whoop.wav")).play()
    else:
        if not arrange:
            QSound(os.path.join(soundPath, "whip.wav")).play()

def toplayer(cards, player):
    if card.special == "gwang":
        togwang(card, player)
    elif card.special == "animal":
        toanimal(card, player)
    elif card.special == "dan":
        todan(card, player)
    else:
        topee(card, player)
    QSound(os.path.join(soundPath, "whoop.wav")).play()
 
def togwang(card, player):
    if player.isEnemy:
        card.move(5+(len(player.gwang)-1)*7, 3)
    else:
        card.move(5+(len(player.gwang)-1)*7, 395)


def toanimal(card, player):
    if player.isEnemy:
        card.move(115+(len(player.animal)-1)*7, 3)
    else:
        card.move(115+(len(player.animal)-1)*7, 395)

def todan(card, player):
    if player.isEnemy:
        card.move(237+(len(player.dan)-1)*7, 3)           
    else:
        card.move(237+(len(player.dan)-1)*7, 395)

def topee(card, player):
    if player.isEnemy:
        card.move(5+(len(player.pee)-1)*7, 75)
    else:
        card.move(5+(len(player.pee)-1)*7, 323)

def attachEventHand(game, player, field):
    def select(slot):
        removeEventHand(player)
        game.select(player, slot)
    for i in range(len(player.hand)):
        player.hand[i].mousePressEvent = lambda state, slot=i: select(slot)

def removeEventHand(player):
    for i in range(len(player.hand)):
        player.hand[i].mousePressEvent = None


def chongtong(cards):
    pass

def shake(cards):
    pass

def chooseCard(window, cards):
    pass