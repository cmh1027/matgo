import random
import os
from PyQt4.QtGui import *
imagePath = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "view\img_matgo\cards")

class CardLabel(QLabel):
    def __init__(self, window):
        super().__init__(window)
        card_image = QPixmap(os.path.join(os.getcwd(), "view\img_matgo\cards\\tail.png"))
        self.setPixmap(card_image)
        self.resize(card_image.size().width(), card_image.size().height())
        self.move(350, 200)
        self.show()

class Card(CardLabel): 
    prop = ("gwang", "animal", "dan", "pee", "dual", "bomb")
    special = (None, "bee", "red", "blue", "cho", "godori", "double")
    month = (1,2,3,4,5,6,7,8,9,10,11,12)

    def __init__(self, window, prop, special, month, number = 0):
        super().__init__(window)
        self.__prop = prop
        self.__special = special
        self.__month = month
        self.__number = number # for 2 pees
    def __str__(self):
        return self.__prop + "/" + str(self.__month)

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
    def imageName(self):
        if self.__special:
            return str(self.__month) + "_" + self.__special + ".png"
        else:
            if self.__number:
                return str(self.__month) + "_" + self.__prop + str(self.__number) + ".png"
            else:
                return str(self.__month) + "_" + self.__prop + ".png"
    
    def flip(self):
        self.setPixmap(QPixmap(os.path.join(os.getcwd(), "view\img_matgo\cards\\"+self.imageName)))
