import wx

class FeedbackPanel(wx.Panel):

    def __init__(self, parent, id, size = None):
        wx.Panel.__init__(self, parent = parent, size = size, style = wx.SIMPLE_BORDER)

        self.parent = parent
        self.id = id

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.on = 'GREEN'
        self.off = wx.NullColour
        # Feedback buttons, we get the labels from the parent panel
        try:
            feedback_option = self.parent.feedback_option
            feedback_sizer = wx.BoxSizer(wx.HORIZONTAL)
            button_list = []
            self.status = [False] * len(feedback_option)
            i = 0
            for option in feedback_option:
                button = wx.Button(self, -1, option, pos = (i, 0))
                button.SetName(option)
                feedback_sizer.Add(button)
                self.Bind(wx.EVT_BUTTON, self.onFeedback, button)
                button_list.append(button)
                # window fix, if we don't set the widget positions,
                # then windows will stack all widgets on top of each other, hiding the best button
                button_size = button.GetSize()
                i += button_size[0] + 5
            sizer.Add(feedback_sizer)
            self.button_list = button_list

        except:
            print 'no feedback on parent panel'

        sizer.AddSpacer((10,10))

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.sizer)

        self.Layout()
        self.SetSizer(sizer)



#------------------------------------------#
    def unselectAll(self):
        self.status = [False] * len(self.button_list)
        for button in self.button_list:
            button.SetBackgroundColour(self.off)

#------------------------------------------#
    def unselect(self, button_index):
        self.status[button_index] = False
        self.button_list[button_index].SetBackgroundColour(self.off)

#------------------------------------------#
    def select(self, button_index):
        self.status[button_index] = True
        button = self.button_list[button_index]
        button.SetBackgroundColour(self.on)

#------------------------------------------#
    def onFeedback(self, event):
        '''
        Tell parent that I've been selected.
        Let my parent keep track of whose been selected for what.
        '''
        button = event.GetEventObject()
        id = self.button_list.index(button)
        if self.status[id]:
            button.SetBackgroundColour(self.off)
        else:
            button.SetBackgroundColour(self.on)
        self.status[id] = not self.status[id]

        self.parent.onFeedback(button, self)

#------------------------------------------#
