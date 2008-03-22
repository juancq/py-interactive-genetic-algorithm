import wx
from gui import feedbackpanel

class OpenGLPanel(feedbackpanel.FeedbackPanel):
    def __init__(self, parent, id, data = None, tick = 100, size = (250, 250)):
        feedbackpanel.FeedbackPanel.__init__(self, parent, id, size = size)

        import openglcanvas
        canvas = openglcanvas.IGAGLCanvas(self, data, tick = tick, size = size)

        self.sizer.Add(canvas, 1, wx.EXPAND)
        self.Layout()

#------------------------------------------#
