import wx
from iga.gacommon import gaParams

class CollaboratePanel(wx.Panel):

    def __init__(self, parent, color="GRAY", name = "", orientation = wx.VERTICAL):
        wx.Panel.__init__(self, parent = parent)

        self.name = name
        self.orientation = orientation

        rows = 3
        cols = 2
        if orientation == wx.FlexGridSizer:
            self.sizer = wx.FlexGridSizer(rows, cols, 1, 1)
        else:
            self.sizer = wx.BoxSizer(orientation)

        self.SetSizer(self.sizer)

        self.limit = rows * cols
        self.best = None
        self.worst = None
        self.parent = parent
        self.child_panels = []
        self.feedback_option = ['Add to Genome', 'Unselect']
        self.user_feedback = set()

#------------------------------------------#
    def clear(self):
        self.sizer.DeleteWindows()
        self.Layout()

#------------------------------------------#
    def onFeedback(self, event_object, panel):
        f_option = self.feedback_option
        label = event_object.GetLabel()

        # if wanting genome
        if label == f_option[0]:
            self.user_feedback.add(self.child_panels.index(panel))
        else:
            panel.unselectAll()
            self.user_feedback.remove(self.child_panels.index(panel))


#------------------------------------------#
    def clearFeedback(self):
        '''
        Clear all user selections made to
        individuals from other peers.
        '''
        self.user_feedback.clear()
        for panel in self.child_panels:
            panel.unselectAll()

#------------------------------------------#
    def getPeerGenomes(self):
        genomes = [self.genomes[i] for i in self.user_feedback]
        self.clearFeedback()

        return genomes


#------------------------------------------#
    def drawGenomes(self, genomes):
        panels = gaParams.draw(self, genomes)
        self.addPanels(panels)
        self.genomes = genomes

#------------------------------------------#
    def addPanels(self, panels, expand = True):
        self.clear()

        self.child_panels = panels
        self.sizer.AddMany(panels)
        self.Layout()

#        if expand:
#            for panel in panels:
#                self.sizer.Add(panel, 1, wx.EXPAND)
#        else:
#            self.sizer.AddMany(panels)
#            for panel in panels:
#                self.sizer.Add(panel, 1)


#------------------------------------------#
