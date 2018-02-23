import sys
import os
import wx
sys.path.append(os.path.join(os.path.dirname(__file__), "view"))
import GUIhandler

if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None, -1, 'MATGO', size = (676, 459))
    frame.Show()
    GUIhandler.main(frame)
    app.MainLoop()