import sys
import os
from PyQt4.QtGui import *
sys.path.append(os.path.join(os.path.dirname(__file__), "view"))
import GUI_screen as ScreenGUI
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(676)
        self.setFixedHeight(459)
        self.setWindowTitle("MATGO")
        self.setWindowIcon(QIcon('icon.ico'))
        self.show()
    def closeEvent(self, event):
        event.accept()
        self.deleteLater()
        sys.exit(0)
        
if __name__ == "__main__":
    app = QApplication([])
    mainWindow = Window()
    ScreenGUI.mainScreen(mainWindow)
    app.exec_()