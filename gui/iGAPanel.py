import wx
from iga.gacommon import gaParams

#---------------------------------------#
class iGAPanel(wx.Panel):
    def __init__(self, parent = None, id = wx.NewId(), size = None):
        '''
        GUI window for the GA.
        '''
        wx.Panel.__init__(self, parent, wx.ID_ANY, size = size)

        import leftPanel
        if gaParams.getVar('gui'):
            import rightPanel as _rightPanel
        else:
            import newrightPanel as _rightPanel

        # window splitter
        self.split = wx.SplitterWindow(self, -1, style = wx.SP_3D)
        self.rightPanel = _rightPanel.RightPanel(self.split,
                size = (100, 100), style = wx.RAISED_BORDER | wx.DOUBLE_BORDER)
        self.leftPanel = leftPanel.LeftPanel(self.split,
                size = (100, 100), style = wx.RAISED_BORDER | wx.DOUBLE_BORDER)
        self.split.SplitVertically(self.leftPanel, self.rightPanel, sashPosition=150)

        self.rightPanel.left = self.leftPanel
        self.leftPanel.right = self.rightPanel
        self.leftPanel.onDisconnect(None)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.split, 1, wx.EXPAND)

        self.SetSizer(sizer)

        self.Layout()
        self.Show(True)
                

#-------------------------------------------#
    def setPopSize(self, popSize):
        gaParams.setPopSize(popSize)
        self.rightPanel.setPopSize(popSize)

#-------------------------------------------#
    def setStepSize(self, stepSize):
        gaParams.setStepSize(stepSize)
        self.rightPanel.submit.SetLabel('Step %d Gen' % stepSize)

#-------------------------------------------#
    def setGeneration(self, gen):
        self.rightPanel.setGeneration(gen)

#-------------------------------------------#
    def onRun(self, event):
        '''
        Runs the GA.
        '''
        panels_to_display = gaParams.onRun(self.rightPanel.displayPanel)
        self.rightPanel.onRun()
        self.leftPanel.onRun()
        self.rightPanel.display(panels_to_display)


#-------------------------------------------#
    def peerStatus(self, status):
        self.leftPanel.peerStatus(status)

#-------------------------------------------#
    def onStop(self):
        self.leftPanel.onStop()

#-------------------------------------------#
