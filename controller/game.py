import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "model"))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "view"))
import field
import player
from card_animation import *
from PyQt4.QtGui import *
class CardLabel(QLabel):
    def __init__(self, window, card):
        super().__init__(window)
        if card is Card:
            card_image = QPixmap(os.path.join(os.getcwd(), "view\img_matgo\cards\\"+card.imageName))
        else:
            card_image = QPixmap(os.path.join(os.getcwd(), "view\img_matgo\cards\\"+card))
        self.setPixmap(card_image)
        self.resize(card_image.size().width(), card_image.size().height())

class Profile(QLabel):
    def __init__(self, window, image, x, y):
        super().__init__(window)
        profile_image = QPixmap(os.path.join(os.getcwd(), "view\img_matgo\\"+image))
        self.setPixmap(profile_image)
        self.resize(profile_image.size().width(), profile_image.size().height())
        self.move(x, y)

class Game:
    def __init__(self, window):
        self.player1 = player.Player()
        self.player2 = player.Player()
        self.field = field.Field()
        self.card = {"tail" : CardLabel(window, "tail.png"), "bomb" : CardLabel(window, "bomb.png")}
        for card in self.field.Deck:
            self.card[card] = CardLabel(window, card)
        Profile(window, "gony.png", 377, 369).show()
        Profile(window, "monkfish.png", 377, 1).show()
    def ready(self):
        pass
        
    def start(self):
        pass

def init(window):
    for components in window.findChildren(QPushButton): # remove Start / Exit Buttons
        components.deleteLater()
    controller = Game(window)