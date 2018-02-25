import sys
import os
from PyQt4.QtGui import *
sys.path.append(os.path.join(os.path.dirname(__file__), "view"))
import GUIhandler
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(676)
        self.setFixedHeight(459)
        self.setWindowTitle("MATGO")
        self.show()
        
if __name__ == "__main__":
    app = QApplication([])
    mainWindow = Window()
    GUIhandler.mainScreen(mainWindow)
    app.exec_()