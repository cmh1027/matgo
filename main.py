import sys
import os
from PyQt4.QtGui import *
sys.path.append(os.path.join(os.path.dirname(__file__), "view"))
from GUI_screen import Window

if __name__ == "__main__":
    app = QApplication([])
    mainWindow = Window()
    mainWindow.mainScreen()
    app.exec_()