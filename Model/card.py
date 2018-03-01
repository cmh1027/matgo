import random
import os
from PyQt4.QtGui import *
imagePath = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "view\img_matgo\cards")
soundPath = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "view")
from GUI_game import CardLabel

class Card(CardLabel): 
    prop = ("gwang", "animal", "dan", "pee", "dual", "bomb")
    special = (None, "bee", "red", "blue", "cho", "godori", "double")
    month = (1,2,3,4,5,6,7,8,9,10,11,12,13) # 13 is for bomb

    def __init__(self, prop, month = 13, special = None, number = 0):
        super().__init__()
        self.__prop = prop
        self.__special = special
        self.__month = month
        self.__number = number # for 2 pees
        self.__fliped = False
    def __str__(self):
        return self.__prop + "/" + str(self.__month)
    
    def propchange(self, prop): # for dual
        if prop == "animal":
            self.__prop = "animal"
        else:
            self.__prop = "pee"
            self.__special = "double"
    @property
    def fliped(self):
        return self.__fliped
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
        if self.__prop == "bomb":
            return "bomb.png"
        if self.__special:
            return str(self.__month) + "_" + self.__special + ".png"
        else:
            if self.__number:
                return str(self.__month) + "_" + self.__prop + str(self.__number) + ".png"
            else:
                return str(self.__month) + "_" + self.__prop + ".png"
    
    def flip(self):
        self.setPixmap(QPixmap(os.path.join(os.getcwd(), "view\img_matgo\cards\\"+self.imageName)))
        self.__fliped = True