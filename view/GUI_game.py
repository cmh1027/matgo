from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtTest
import os
import time
import copy
soundPath = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "view\sound")
class CardLabel(QLabel):
    def __init__(self, window, name=None):
        super().__init__(window)
        if not name:
            card_image = QPixmap(os.path.join(os.getcwd(), "view\img_matgo\cards\\tail.png"))
        else:
            card_image = QPixmap(os.path.join(os.getcwd(), "view\img_matgo\cards\\"+name))
        self.setPixmap(card_image)
        self.resize(card_image.size().width(), card_image.size().height())
        self.move(350, 200)
        self.show()

class Status:
    class StatusLabel(QLabel):
        def __init__(self, window, isEnemy):
            super().__init__(window)
            self.setStyleSheet("background-color: white;color: black; padding-left: 2px;")
            if isEnemy:
                self.move(399, 139)
            else:
                self.move(399, 232)
            self.resize(72, 88)
            self.setFont(QFont("Times", 9))
            self.show()
    
    class CountLabel(QLabel):
        def __init__(self, window):
            super().__init__(window)
            self.setStyleSheet("background-color: white;color: black;")
            self.setFont(QFont("Times", 9))
        def setText(self, num):
            if num == 0:
                self.hide()
                return
            else:
                self.show()
                self.raise_()
            super().setText(str(num))
            if num < 10:
                self.resize(7, 11)
            else:
                self.resize(13, 11)
    
    class GwangLabel(CountLabel):
        def __init__(self, window, isEnemy):
            self.isEnemy = isEnemy
            super().__init__(window)
        def setText(self, num):
            if type(num) is str:
                num = int(num)
            super().setText(num)
            if self.isEnemy:
                self.move(33+7*num, 54)
            else:
                self.move(33+7*num, 444)

    class AnimalLabel(CountLabel):
        def __init__(self, window, isEnemy):
            self.isEnemy = isEnemy
            super().__init__(window)
        def setText(self, num):
            if type(num) is str:
                num = int(num)
            super().setText(num)
            if self.isEnemy:
                self.move(146+7*num, 54)
            else:
                self.move(150+7*num, 444)

    class DanLabel(CountLabel):
        def __init__(self, window, isEnemy):
            self.isEnemy = isEnemy
            super().__init__(window)
        def setText(self, num):
            if type(num) is str:
                num = int(num)
            super().setText(num)
            if self.isEnemy:
                self.move(268+7*num, 54)
            else:
                self.move(272+7*num, 444)

    class PeeLabel(CountLabel):
        def __init__(self, window, isEnemy):
            self.isEnemy = isEnemy
            super().__init__(window)
        def setText(self, num, sum):
            if type(num) is str:
                num = int(num)
            super().setText(sum)
            if self.isEnemy:
                self.move(33+7*num, 122)
            else:
                self.move(33+7*num, 375)

    def __init__(self, window, isEnemy):
        self._status = self.StatusLabel(window, isEnemy)
        self._gwanglabel = self.GwangLabel(window, isEnemy)
        self._animallabel = self.AnimalLabel(window, isEnemy)
        self._danlabel = self.DanLabel(window, isEnemy)
        self._peelabel = self.PeeLabel(window, isEnemy)


class Dialog(QLabel):
    def __init__(self, window, width, height):
        super().__init__(window)
        self.resize(width, height)
        self.move((window.width()-width)//2, (window.height()-height)//2)
        self.setStyleSheet("background-color: #f0feb8;padding-left:5px; padding-right:5px")
        self.show()

class ShakeDialog(Dialog): # 180 120
    def __init__(self, window, cards, width, height):
        super().__init__(window, width, height)
        qv = QVBoxLayout()
        title = QLabel("흔들었습니다", window)
        title.setFont(QFont("Times", 14, QFont.Bold))
        qv.addWidget(title, 0, Qt.AlignCenter)
        qh = QHBoxLayout()
        for card in cards:
            label = CardLabel(window, card.imageName)
            qh.addWidget(label)
        qv.addLayout(qh)
        self.setLayout(qv)

class ChongtongDialog(Dialog): # 180 120
    def __init__(self, window, cards, width, height):
        super().__init__(window, width, height)
        qv = QVBoxLayout()
        title = QLabel("총통!", window)
        title.setFont(QFont("Times", 14, QFont.Bold))
        qv.addWidget(title, 0, Qt.AlignCenter)
        if len(cards) == 4:
            qh = QHBoxLayout()    
            for card in cards:
                label = CardLabel(window, card.imageName)
                qh.addWidget(label)
            qv.addLayout(qh)
        else:
            qh = QHBoxLayout()    
            for card in cards[0:4]:
                label = CardLabel(window, card.imageName)
                qh.addWidget(label)
            qv.addLayout(qh)
            qh = QHBoxLayout()    
            for card in cards[4:8]:
                label = CardLabel(window, card.imageName)
                qh.addWidget(label)
            qv.addLayout(qh)
        self.setLayout(qv)
        
def tohand(card, slot, player, arrange=False):
    if player.isEnemy:
        card.move(476+(slot%5)*40, 5+68*(slot//5))
    else:
        card.flip()
        card.move(476+(slot%5)*40, 326+68*(slot//5))
    if not arrange:
        QSound(os.path.join(soundPath, "whoop.wav")).play()

def tofield(card, slot, pos, arrange=False):
    if not card.fliped:
        card.flip()
    card.move(10+slot//2*55+5*pos+20*(slot%2), 150+85*(slot%2)+5*pos)
    if pos==0:
        if not arrange:
            QSound(os.path.join(soundPath, "whoop.wav")).play()
    else:
        if not arrange:
            QSound(os.path.join(soundPath, "whip.wav")).play()

def toplayer(card, player):
    if card.prop == "gwang":
        togwang(card, player)
    elif card.prop == "animal":
        toanimal(card, player)
    elif card.prop == "dan":
        todan(card, player)
    else:
        topee(card, player)
    QSound(os.path.join(soundPath, "whoop.wav")).play()
 
def togwang(card, player):
    card.raise_()
    if player.isEnemy:
        card.move(2+(len(player.gwang)-1)*7, 3)
    else:
        card.move(2+(len(player.gwang)-1)*7, 395)


def toanimal(card, player):
    card.raise_()
    if player.isEnemy:
        card.move(115+(len(player.animal)-1)*7, 3)
    else:
        card.move(119+(len(player.animal)-1)*7, 395)

def todan(card, player):
    card.raise_()
    if player.isEnemy:
        card.move(237+(len(player.dan)-1)*7, 3)           
    else:
        card.move(241+(len(player.dan)-1)*7, 395)

def topee(card, player):
    card.raise_()
    if player.isEnemy:
        card.move(2+(len(player.pee)-1)*7, 72)
    else:
        card.move(2+(len(player.pee)-1)*7, 325)

def attachEventHand(player, field):
    def select(slot):
        global selected
        selected = slot
        removeEventHand(player)
    for i in range(len(player.hand)):
        player.hand[i].mousePressEvent = lambda state, slot=i: select(slot)
    return 0
    

def removeEventHand(player):
    for i in range(len(player.hand)):
        player.hand[i].mousePressEvent = None


def chongtong(window, cards1, cards2):
    if not(cards1 and cards2):
        dialog = ChongtongDialog(window, cards1, 200, 140)
    else:
        cards1.extend(cards2)
        dialog = ChongtongDialog(window, cards1, 200, 280)
    QtTest.QTest.qWait(2000)
    dialog.setParent(None)

def shake(window, cards):
    QSound(os.path.join(soundPath, "shake.wav")).play()
    dialog = ShakeDialog(window, cards, 200, 140)
    QtTest.QTest.qWait(2000)
    dialog.setParent(None)

def bomb(window, field, player, cards):
    field.put(player.put(cards.pop(0)))
    QtTest.QTest.qWait(400)
    field.put(player.put(cards.pop(0)))
    QtTest.QTest.qWait(400)
    firstput = field.put(player.put(cards.pop(0)))
    QtTest.QTest.qWait(400)
    QSound(os.path.join(soundPath, "bomb.wav")).play()
    QtTest.QTest.qWait(500)
    return firstput

def selectdual(window):
    pass

def whattoget(window, cards):
    pass

def threefuck(window):
    print('쓰리뻑')
    QSound(os.path.join(soundPath, "woohoo.wav")).play()
    QtTest.QTest.qWait(1500)

def godori(window):
    print('고도리')
    QSound(os.path.join(soundPath, "godori.wav")).play()
    QtTest.QTest.qWait(1500)
    

def reddan(window):
    print('홍단')
    QSound(os.path.join(soundPath, "reddan.wav")).play()
    QtTest.QTest.qWait(1500)
    

def bluedan(window):
    print('청단')
    QSound(os.path.join(soundPath, "bluedan.wav")).play()
    QtTest.QTest.qWait(1500)
    
def chodan(window):
    print('초단')
    QSound(os.path.join(soundPath, "chodan.wav")).play()
    QtTest.QTest.qWait(1500)
   

def gwang(window, count):
    print('{}광'.format(count))
    QSound(os.path.join(soundPath, "gwang{}.wav".format(count))).play()
    QtTest.QTest.qWait(1500)
        

def askgo(window):
    pass

def go(window, count):
    print("{}고".format(count))
    QSound(os.path.join(soundPath, "go{}.wav".format(count))).play()
    QtTest.QTest.qWait(1500)    

def kiss(window):
    print("쪽")
    QSound(os.path.join(soundPath, "woohoo.wav")).play()
    QtTest.QTest.qWait(1500)
    

def fuck(window):
    print("뻑")
    QSound(os.path.join(soundPath, "doh.wav")).play()
    QtTest.QTest.qWait(1500)
    

def getfuck(window):
    print("뻑 얻음")
    QSound(os.path.join(soundPath, "woohoo.wav")).play()
    QtTest.QTest.qWait(1500)
    

def jafuck(window):
    print("자뻑")
    QSound(os.path.join(soundPath, "woohoo.wav")).play()
    QtTest.QTest.qWait(1500)
    

def tadack(window):
    print("따닥")
    QSound(os.path.join(soundPath, "woohoo.wav")).play()
    QtTest.QTest.qWait(1500)
    