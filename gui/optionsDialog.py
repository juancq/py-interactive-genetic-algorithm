
import wx

class OptionsDialog(wx.Dialog):

    def __init__(self, parent, params = None, id = wx.ID_ANY, title = 'GA Preferences'):
        '''
        Dialog which contains overall options, such as GA configuration, and display preferences.
        '''

        wx.Dialog.__init__(self, parent, id = id, title = title)

        self.gaWindow = parent
        self.gaParams = params

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(sizer)

        sizer.Add((10, 10))

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.sizer, 1, wx.EXPAND)

        tempSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Positioning type
        self.positioning = wx.RadioBox(self, wx.ID_ANY, 'Positioning Scheme', choices = ['Absolute', 'Relative', 'Grid'])
        self.positioning.SetStringSelection(self.gaParams.getVar('positioning').capitalize())
        self.sizer.Add(self.positioning, 0, wx.ALIGN_BOTTOM)

        # Color space selection
        self.colorSpace = wx.RadioBox(self, wx.ID_ANY, 'Color Space', choices = ['16', '4096', 'All Colors'])
        _colorSpace = self.gaParams.getVar('colorSpace')
        if _colorSpace == 16:
            self.colorSpace.SetSelection(0)
        elif _colorSpace == 4096:
            self.colorSpace.SetSelection(1)
        else:
            self.colorSpace.SetSelection(2)

        self.sizer.Add(self.colorSpace, 0, wx.ALIGN_BOTTOM)

        self.selectionType = wx.RadioBox(self, wx.ID_ANY, 'Selection Type', choices = ['Roulette', 'Tournament'])
        self.selectionType.SetStringSelection(self.gaParams.getVar('selectionType').capitalize())
        self.sizer.Add(self.selectionType, 0, wx.ALIGN_BOTTOM)


        displaySizer = wx.BoxSizer(wx.HORIZONTAL)
        
        displaySizer.Add(wx.StaticText(self, -1, 'Individuals to Display:'), 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER)
        self.displayNum = wx.Slider(self, -1, size = (100, 40), style = wx.SL_LABELS | wx.SL_AUTOTICKS)
        self.displayNum.SetRange(2, 20)
        self.displayNum.SetValue(self.gaParams.getVar('displayNum'))
        displaySizer.Add(self.displayNum, 0)

        self.sizer.Add(displaySizer, 0)

        self.okButton = wx.Button(self, wx.ID_OK, '')
        self.cancelButton = wx.Button(self, wx.ID_CANCEL, '')

        self.Bind(wx.EVT_BUTTON, self.onOK, self.okButton)
        self.Bind(wx.EVT_BUTTON, self.onCancel, self.cancelButton)

        tempSizer.Add((10, 10), 10)
        tempSizer.Add(self.okButton, 0) 
        tempSizer.Add((1,1), 1)
        tempSizer.Add(self.cancelButton, 0)
        tempSizer.Add((2,2), 1)

        self.sizer.Add((10,10), 2, wx.EXPAND)
        self.sizer.Add(tempSizer, 0, wx.EXPAND)
        self.sizer.Add((10,10), 0)


        self.currentValues = {}
        self.currentValues['positioning'] = self.positioning.GetSelection()
        self.currentValues['colorSpace'] = self.colorSpace.GetSelection()
        self.currentValues['selectionType'] = self.selectionType.GetSelection()
        self.currentValues['displayNum'] = self.displayNum.GetValue()

#-------------------------------------------#
    def Show(self):
        wx.Dialog.Show(self)

#-------------------------------------------#
    def Hide(self):
        wx.Dialog.Hide(self)

#-------------------------------------------#
    def onOK(self, event):

        # Adjust rank list on main window if number of inviduals displayed was changed
        if not (self.currentValues['displayNum'] == self.displayNum.GetValue()):
            self.gaWindow.adjustRankList(self.displayNum.GetValue())

        # Save current options
        self.currentValues['positioning'] = self.positioning.GetSelection()
        self.currentValues['colorSpace'] = self.colorSpace.GetSelection()
        self.currentValues['displayNum'] = self.displayNum.GetValue()
        self.currentValues['selectionType'] = self.selectionType.GetSelection()

        self.gaParams.setOptionAttributes(self.currentValues)

        self.Hide()

#-------------------------------------------#
    def onCancel(self, event):
        # Discard current changes
        # Retrieve values from when the dialog was opened
        self.positioning.SetSelection(self.currentValues['positioning'])
        self.colorSpace.SetSelection(self.currentValues['colorSpace'])
        self.selectionType.SetSelection(self.currentValues['selectionType'])
        self.displayNum.SetValue(self.currentValues['displayNum'])

        self.Hide()

#-------------------------------------------#
