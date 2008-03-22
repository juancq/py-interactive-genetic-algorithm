import wx
from iga.gacommon import gaParams

class DisplayPanel(wx.ScrolledWindow):

    def __init__(self, parent):

        wx.ScrolledWindow.__init__(self, parent = parent, style=wx.DOUBLE_BORDER, size = (710,850))
        self.SetScrollbars(20,20,50,50)
        self.defFont = self.GetFont()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.SetBackgroundColour('BLACK')
        self.SetForegroundColour('WHITE')

        self.best = None
        self.worst = None
        self.parent = parent
        if gaParams.params['application'].has_key('feedback'):
            self.feedback_option = gaParams.params['application']['feedback'] 
	else:
            self.feedback_option = ['Best']
        self.user_feedback = [-1] * len(self.feedback_option)

        self.width, self.height = self.GetSize()

#------------------------------------------#
    def onFeedback(self, event_object, panel):
        '''
        We keep track of user input by matching
        the push button to its label.
        '''
        feedback = self.user_feedback
        label = event_object.GetLabel()
        f_option = self.feedback_option

        new_feedback = self.child_panels.index(panel)
        feedback_index = f_option.index(label)

        # if feedback giving
        if feedback[feedback_index] != new_feedback:
            # if changing previous selection, then unselect previous button
            if feedback[feedback_index] >= 0:
                self.child_panels[feedback[feedback_index]].unselect(feedback_index)

            self.user_feedback[feedback_index] = new_feedback

        # if pressing the same button, then unselect
        elif feedback[feedback_index] == new_feedback:
            self.user_feedback[feedback_index] = -1

        print event_object.GetLabel()
        print self.child_panels.index(panel)


#------------------------------------------#
    def getUserInput(self):
        print self.user_feedback
        error = ''
        for fb,opt in zip(self.user_feedback, self.feedback_option):
            if fb < 0:
                error += ' %s,' % opt

        if error:
            error = error[:-1]
            msg = 'Please provide feedback for: %s\n' % error
            msgDialog = wx.MessageDialog(self, msg, 'Enter Feedback',
                    style = wx.ICON_ERROR )
            
            msgDialog.ShowModal()
            msgDialog.Destroy()
            return None

        return self.user_feedback


#------------------------------------------#
    def addPanels(self, panels, expand = True):
        panel_num = len(panels)
        self.child_panels = panels
        rowSize = 3

        if gaParams.getVar('gui'):
            space = (5, 5)
        else:
            space = (20, 20)

        if gaParams.params.has_key('rowSize'):
            rowSize = gaParams.params['rowSize'] 

        if expand:
            def addtorow(row, panel):
                row.Add(panel, 0, wx.EXPAND)
        else:
            def addtorow(row, panel):
                row.Add(panel, 0)

        self.sizer.AddSpacer(space)
        self.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL,wx.FONTWEIGHT_BOLD))
        self.sizer.Add(wx.StaticText(self, -1, 'My Genomes'), 0, wx.ALIGN_CENTER|wx.EXPAND)
        self.SetFont(self.defFont)

        best_subset = gaParams.getVar('population')['subset']['size']
        for i in xrange(0, best_subset, rowSize):
            row = wx.BoxSizer(wx.HORIZONTAL)
            row.AddSpacer(space)
            num_cols = min(rowSize, len(panels)-i)

            for j in xrange(num_cols):
                addtorow(row, panels[i+j])

            row.AddSpacer(space)
            addtorow(self.sizer, row)


        self.sizer.AddSpacer((30,50))
        self.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL,wx.FONTWEIGHT_BOLD))
        self.sizer.Add(wx.StaticText(self, -1, 'Rest of Population'), 0, wx.ALIGN_CENTER|wx.EXPAND)
        self.SetFont(self.defFont)

        # add rest of pop
        for i in xrange(best_subset, len(panels), rowSize):
            row = wx.BoxSizer(wx.HORIZONTAL)
            row.AddSpacer(space)
            num_cols = min(rowSize, len(panels)-i)

            for j in xrange(num_cols):
                addtorow(row, panels[i+j])

            row.AddSpacer(space)
            addtorow(self.sizer, row)
        self.sizer.AddSpacer(space)

        self.Scroll(0, 0)
        self.Layout()

#------------------------------------------#
    def addUIPanel(self, panel):
        self.sizer.Add(panel)
        self.Layout()

#------------------------------------------#
    def fit(self):
        self.Layout()
        self.sizer.Fit(self)
        #self.sizer.SetSizeHints(self)
        w, h = self.GetSize()
        self.SetSize((w, self.height))
        self.Layout()

#------------------------------------------#
    def clear(self):
        self.user_feedback = [-1] * len(self.feedback_option)
        #self.sizer.DeleteWindows()
        self.sizer.Clear(True)
        self.Layout()
