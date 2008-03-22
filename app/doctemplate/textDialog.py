import wx

class TextDialog(wx.Dialog):

    def __init__(self, parent, title, box_size):

        wx.Dialog.__init__(self, parent, wx.NewId(), title)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        w, l = box_size[-2], box_size[-1]
        self.text_box = wx.TextCtrl(self, -1, size = (w, l), style = wx.TE_MULTILINE)

        sizer = self.CreateStdDialogButtonSizer(wx.HORIZONTAL)
        sizer.AddButton(wx.Button(self, wx.ID_CANCEL, ''))
        sizer.Realize()

        self.sizer.Add(self.text_box)
        self.sizer.AddSpacer((10,10))
        self.sizer.Add(sizer)

        self.SetSizer(self.sizer)
        self.Fit()

    def GetValue(self):
        return self.text_box.GetValue()
