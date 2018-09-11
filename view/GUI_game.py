from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtTest
import os
class CardLabel(QLabel):
    def __init__(self, window, name=None):
        super().__init__(window)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("color:red;")
        if not name:
            self.setImage(os.path.join(os.getcwd(), "view\img_matgo\cards\\tail.png"))
        else:
            self.setImage(os.path.join(os.getcwd(), "view\img_matgo\cards\\"+name))
        
    def setImage(self, image):
        if(os.path.exists(image)):
            card_image = QPixmap(image)
            self.setPixmap(card_image)
            self.resize(card_image.size().width(), card_image.size().height())
        else:
            self.resize(37, 60)
            self.setText("Image\nnot\nfound")

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

    def __init__(self, window, isEnemy): # FIX
        self.status = self.StatusLabel(window, isEnemy)
        self.gwanglabel = self.GwangLabel(window, isEnemy)
        self.animallabel = self.AnimalLabel(window, isEnemy)
        self.danlabel = self.DanLabel(window, isEnemy)
        self.peelabel = self.PeeLabel(window, isEnemy)
    
    def setParent(self, window):
        self.status.setParent(window)
        self.gwanglabel.setParent(window)
        self.animallabel.setParent(window)
        self.danlabel.setParent(window)
        self.peelabel.setParent(window)


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
        titleLabel = QLabel("흔들었습니다", self)
        titleLabel.setFont(QFont("Times", 14, QFont.Bold))
        qv.addWidget(titleLabel, 0, Qt.AlignCenter)
        qh = QHBoxLayout()
        for card in cards:
            label = CardLabel(self, card.imageName)
            qh.addWidget(label)
        qv.addLayout(qh)
        self.setLayout(qv)

class ChongtongDialog(Dialog):
    def __init__(self, window, cards, width, height):
        super().__init__(window, width, height)
        qv = QVBoxLayout()
        titleLabel = QLabel("총통!", self)
        titleLabel.setFont(QFont("Times", 14, QFont.Bold))
        qv.addWidget(titleLabel, 0, Qt.AlignCenter)
        if len(cards) == 4:
            qh = QHBoxLayout()    
            for card in cards:
                label = CardLabel(self, card.imageName)
                qh.addWidget(label)
            qv.addLayout(qh)
        else:
            qh = QHBoxLayout()    
            for card in cards[0:4]:
                label = CardLabel(self, card.imageName)
                qh.addWidget(label)
            qv.addLayout(qh)
            qh = QHBoxLayout()    
            for card in cards[4:8]:
                label = CardLabel(self, card.imageName)
                qh.addWidget(label)
            qv.addLayout(qh)
        self.setLayout(qv)

class ResultDialog(Dialog):
    def __init__(self, window, title, width, height, messages=None, money=None):
        super().__init__(window, width, height)
        qv = QVBoxLayout()
        titleLabel = QLabel(title, window)
        titleLabel.setFont(QFont("Times", 24, QFont.Bold))
        qv.addWidget(titleLabel, 0, Qt.AlignCenter)
        if messages:
            messageLabel = QLabel('\n'.join(messages), window)
            messageLabel.setFont(QFont("Times", 14))
        else:
            messageLabel = QLabel('무승부', window)
            messageLabel.setFont(QFont("Times", 14))
        qv.addWidget(messageLabel, 0, Qt.AlignCenter)            
        if money:
            moneyLabel = QLabel(str(money)+"원", window)
            moneyLabel.setFont(QFont("Times", 24, QFont.Bold))
        else:
            moneyLabel = QLabel("재시작합니다", window)
            moneyLabel.setFont(QFont("Times", 24, QFont.Bold))
        qv.addWidget(moneyLabel, 0, Qt.AlignCenter)            
        self.setLayout(qv)

class ResultDialog(Dialog):
    def __init__(self, window, title, width, height, messages=None, money=None):
        super().__init__(window, width, height)
        qv = QVBoxLayout()
        titleLabel = QLabel(title, window)
        titleLabel.setFont(QFont("Times", 24, QFont.Bold))
        qv.addWidget(titleLabel, 0, Qt.AlignCenter)
        if messages:
            messageLabel = QLabel('\n'.join(messages), window)
            messageLabel.setFont(QFont("Times", 14))
        else:
            messageLabel = QLabel('무승부', window)
            messageLabel.setFont(QFont("Times", 14))
        qv.addWidget(messageLabel, 0, Qt.AlignCenter)            
        if money:
            moneyLabel = QLabel(str(money)+"원", window)
            moneyLabel.setFont(QFont("Times", 24, QFont.Bold))
        else:
            moneyLabel = QLabel("재시작합니다", window)
            moneyLabel.setFont(QFont("Times", 24, QFont.Bold))
        qv.addWidget(moneyLabel, 0, Qt.AlignCenter)            
        self.setLayout(qv)

class FieldGUI:
    def __init__(self, parent):
        self.parent = parent
    def tofield(self, card, slot, pos, arrange=False):
        if not card.fliped:
            card.flip()
            self.parent.flipcard.emit(card)
        self.parent.movecard.emit(card, 10+slot//2*55+5*pos+20*(slot%2), 150+85*(slot%2)+5*pos)
        if pos==0:
            if not arrange:
                self.parent.playsound.emit("whoop")
        else:
            if not arrange:
                self.parent.playsound.emit("whip")

    def clear(self):
        print('싹쓸')
        self.parent.playsound.emit("clear")
        QtTest.QTest.qWait(1500)

def attachEventHand(controller, hand, field):
    def select(number):
        for i in range(len(hand)):
            controller.cardlabels[hand[i]].mousePressEvent = None
            for label in controller.cardlabels[hand[i]].findChildren(QWidget):
                label.setParent(None)
        controller.answer.emit(number)
    for i in range(len(hand)):
        controller.cardlabels[hand[i]].mousePressEvent = lambda state, number=i:select(number)
        if field.exist(hand[i]):
            exist = QLabel("↖", controller.cardlabels[hand[i]])
            exist.show()

class PlayerGUI:
    def __init__(self, parent, player, field):
        self.parent = parent
        self.player = player
        self.field = field

    def tohand(self, card, slot, arrange=False):
        if self.player.isEnemy:
            self.parent.movecard.emit(card, 476+(slot%5)*40, 5+68*(slot//5))
        else:
            card.flip()
            self.parent.flipcard.emit(card)
            self.parent.movecard.emit(card, 476+(slot%5)*40, 326+68*(slot//5))
        if not arrange:
            self.parent.playsound.emit("whoop")

    def toplayer(self, cards):
        if type(cards) is list:
            for card in cards:
                if card.prop == "gwang":
                    self.togwang(card)
                elif card.prop == "animal":
                    self.toanimal(card)
                elif card.prop == "dan":
                    self.todan(card)
                else:
                    self.topee(card)
            if len(cards) != 0:
                self.parent.playsound.emit("whoop")
        else:
            if cards.prop == "gwang":
                self.togwang(cards)
            elif cards.prop == "animal":
                self.toanimal(cards)
            elif cards.prop == "dan":
                self.todan(cards)
            else:
                self.topee(cards)
            self.parent.playsound.emit("whoop") 
        
            
    def togwang(self, card):
        self.parent.raisecard.emit(card)
        if self.player.isEnemy:
            self.parent.movecard.emit(card, 2+(len(self.player.gwang)-1)*7, 3)
        else:
            self.parent.movecard.emit(card, 2+(len(self.player.gwang)-1)*7, 395)

    def toanimal(self, card):
        self.parent.raisecard.emit(card)
        if self.player.isEnemy:
            self.parent.movecard.emit(card, 115+(len(self.player.animal)-1)*7, 3)
        else:
            self.parent.movecard.emit(card, 119+(len(self.player.animal)-1)*7, 395)

    def todan(self, card):
        self.parent.raisecard.emit(card)
        if self.player.isEnemy:
            self.parent.movecard.emit(card, 237+(len(self.player.dan)-1)*7, 3)          
        else:
            self.parent.movecard.emit(card, 241+(len(self.player.dan)-1)*7, 395)

    def topee(self, card):
        self.parent.raisecard.emit(card)
        if self.player.isEnemy:
            self.parent.movecard.emit(card, 2+(len(self.player.pee)-1)*7, 72)
        else:
            self.parent.movecard.emit(card, 2+(len(self.player.pee)-1)*7, 325)

    def selectdual(self):
        answer = input("Treat as pee? : ")
        if answer == "no":
            return "animal"
        else:
            return "pee"     

    def whattoget(self, cards):
        num = input("Choose a card to get : ")
        if num == 0:
            return 0
        else:
            return 1

    def askgo(self):
        answer = input("Go? : ")
        if answer == "yes":
            return True
        else:
            return False

    def chongtong(self, cards1, cards2):
        if not(cards1 and cards2):
            if cards1:
                self.parent.chongtong.emit(cards1, 230, 140)
            else:
                self.parent.chongtong.emit(cards2, 230, 140)
        else:
            cards1.extend(cards2)
            self.parent.chongtong.emit(cards1, 230, 280)
        QtTest.QTest.qWait(2000)
        

    def shake(self, cards):
        self.parent.playsound.emit("shake")
        self.parent.shake.emit(cards, 200, 140)
        QtTest.QTest.qWait(2000)

    def bomb(self, cards):
        self.field.put(self.player.put(cards.pop(0)))
        QtTest.QTest.qWait(400)
        self.field.put(self.player.put(cards.pop(0)))
        QtTest.QTest.qWait(400)
        firstput = self.field.put(self.player.put(cards.pop(0)))
        QtTest.QTest.qWait(400)
        self.parent.playsound.emit("bomb")
        QtTest.QTest.qWait(500)
        return firstput


    def threefuck(self):
        print('쓰리뻑')
        self.parent.playsound.emit("threefuck")
        QtTest.QTest.qWait(1500)

    def allgodori(self):
        print('고도리')
        self.parent.playsound.emit("godori")
        QtTest.QTest.qWait(1500)
        

    def allreddan(self):
        print('홍단')
        self.parent.playsound.emit("reddan")
        QtTest.QTest.qWait(1500)
        

    def allbluedan(self):
        print('청단')
        self.parent.playsound.emit("bluedan")
        QtTest.QTest.qWait(1500)
        
    def allchodan(self):
        print('초단')
        self.parent.playsound.emit("chodan")
        QtTest.QTest.qWait(1500)
    

    def allgwang(self, count, bee=False):
        if not bee:
            print('{}광'.format(count))
        else:
            print("비삼광")
        self.parent.playsound.emit("gwang{}".format(count))
        QtTest.QTest.qWait(1500)
            

    def go(self, count):
        print("{}고".format(count))
        self.parent.playsound.emit("go{}".format(count))
        QtTest.QTest.qWait(1500)

    def stop(self):
        print("스톱")
        self.parent.playsound.emit("stop")
        QtTest.QTest.qWait(1500)   

    def kiss(self):
        print("쪽")
        self.parent.playsound.emit("kiss")
        QtTest.QTest.qWait(1500)
        

    def fuck(self):
        print("뻑")
        self.parent.playsound.emit("fuck")
        QtTest.QTest.qWait(1500)
        

    def getfuck(self):
        print("뻑 얻음")
        self.parent.playsound.emit("getfuck")
        QtTest.QTest.qWait(1500)
        

    def jafuck(self):
        print("자뻑")
        self.parent.playsound.emit("getfuck")
        QtTest.QTest.qWait(1500)

    def tadack(self):
        print("따닥")
        self.parent.playsound.emit("tadack")
        QtTest.QTest.qWait(1500)

    def result(self, info):
        if info["winner"] == None:
            self.parent.playsound.emit("lose")
            self.parent.result.emit("나가리", 260, 140, None, None)
        elif info["winner"]:
            self.parent.playsound.emit("win")
            self.parent.result.emit("승리", 260, 240+10*len(info["messages"]), info["messages"], info["money"])
        else:
            self.parent.playsound.emit("lose")
            self.parent.result.emit("패배", 260, 240+10*len(info["messages"]), info["messages"], info["money"])
        QtTest.QTest.qWait(4500)
    
    def askpush(self):
        answer = input("Push? : ")
        if answer == "yes":
            return True
        else:
            return False