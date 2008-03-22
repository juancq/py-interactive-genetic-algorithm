import wx
from iga.gacommon import gaParams

class CollaboratePanel(wx.Panel):

    def __init__(self, parent, color="GRAY", name = "", orientation = wx.VERTICAL):
        wx.Panel.__init__(self, parent = parent)

        self.SetBackgroundColour('WHITE')
        self.defFont = self.GetFont()

        self.name = name
        self.orientation = orientation

        self.sizer = wx.BoxSizer(orientation)

        self.SetSizer(self.sizer)

        self.best = None
        self.parent = parent
        self.child_panels = []
        self.feedback_option = ['Add to Genome', 'Best']
        self.bestIndex = self.feedback_option.index('Best')
        self.user_feedback = set()

#------------------------------------------#
    def clear(self):
        self.clearFeedback()
        self.sizer.Clear(True)
        self.Layout()
        self.Refresh()
        self.child_panels = []

#------------------------------------------#
    def onFeedback(self, event_object, panel):
        f_option = self.feedback_option
        label = event_object.GetLabel()

        feedback = self.user_feedback
        value = self.child_panels.index(panel)


        # if unselecting individual
        if label == f_option[0] and value in feedback:
            feedback.remove(value)
            panel.unselectAll()
            if value == self.best:
                self.best = None

        # if adding to genome 
        elif label == f_option[0] and value not in feedback:
            feedback.add(value)

        # if panel selected as best (and add to genome not pressed yet), 
        # then highlight add to genome  button as well
        elif label == f_option[1] and value not in feedback:
            feedback.add(value)
            if self.best is not None:
                self.child_panels[self.best].unselect(self.bestIndex)
            self.best = value
            panel.select(0)

        # if pressing best and add to genome has already been pressed
        elif label == f_option[1] and value in feedback:
            if self.best == value:
                self.best = None
            elif self.best is None:
                self.best = value

        else:
            panel.unselectAll()
            feedback.remove(value)
            if value == self.best:
                self.best = None

#------------------------------------------#
    def clearFeedback(self):
        '''
        Clear all user selections made to
        individuals from other peers.
        '''
        self.user_feedback.clear()
        for panel in self.child_panels:
            panel.unselectAll()
        self.best = None

#------------------------------------------#
    def getPeerGenomes(self):
        genomes = [self.genomes[i] for i in self.user_feedback]
        if self.best is None:
            return {'genomes': genomes, 'best': None}
        else:
            return {'genomes': genomes, 'best': self.genomes[self.best]}


#------------------------------------------#
    def drawGenomes(self, genomes):
        panels = gaParams.draw(self, genomes)
        self.addPanels(panels)
        self.genomes = genomes

#------------------------------------------#
    def addPanels(self, panels, expand = True):
        self.clear()
        self.child_panels = panels
        rowSize = 3

        space = (5, 5)

        if gaParams.params.has_key('rowSize'):
            rowSize = gaParams.params['rowSize'] 

        if expand:
            def addtorow(row, panel):
                row.Add(panel, 1, wx.EXPAND)
        else:
            def addtorow(row, panel):
                row.Add(panel, 1)

        self.sizer.AddSpacer(space)
        self.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL,wx.FONTWEIGHT_BOLD))
        self.sizer.Add(wx.StaticText(self, -1, 'Peer Genomes'), 0, wx.EXPAND|wx.ALIGN_CENTER)
        self.SetFont(self.defFont)

        for i in xrange(0, len(panels), rowSize):
            row = wx.BoxSizer(wx.HORIZONTAL)
            row.AddSpacer(space)
            num_cols = min(rowSize, len(panels)-i)

            for j in xrange(num_cols):
                addtorow(row, panels[i+j])

            row.AddSpacer(space)
            addtorow(self.sizer, row)

        self.sizer.AddSpacer(space)

        self.Layout()

#        if expand:
#            for panel in panels:
#                self.sizer.Add(panel, 1, wx.EXPAND)
#        else:
#            self.sizer.AddMany(panels)
#            for panel in panels:
#                self.sizer.Add(panel, 1)


#------------------------------------------#
