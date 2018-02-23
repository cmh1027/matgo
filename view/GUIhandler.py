import wx
def main(frame):
    panel = wx.Panel(frame, -1, pos=(150, 150), style=wx.TRANSPARENT_WINDOW)
    panel.SetSize((300, 150))
    btn = wx.Button(panel,-1,"vs Computer") 
    btn.SetSize((300, 150))