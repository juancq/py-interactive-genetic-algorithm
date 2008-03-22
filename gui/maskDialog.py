import wx
from iga.gacommon import gaParams

class MaskDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.NewId(), "Edit Mask")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer((10, 10))

        # if mask is defined
        vars = gaParams.getAppVars()
        if vars:
            options = [name for name in vars.iterkeys()]
            list = wx.CheckListBox(self, -1, choices = options)
            self.list = list
            i = 0
            for value in vars.values():
                if value.has_key('mask') and value['mask']:
                    list.Check(i, True)
                i += 1

            sizer.Add(list)
        else:
            sizer.Add(wx.StaticText(self, -1, 'No mask defined.'))

        bSizer = wx.StdDialogButtonSizer() 
        okButton = wx.Button(self, wx.ID_OK, '')
        cancelButton = wx.Button(self, wx.ID_CANCEL, '')
        bSizer.AddButton(okButton)
        bSizer.AddButton(cancelButton)
        bSizer.Realize()

        sizer.AddSpacer((10, 18))
        sizer.Add(bSizer)
        self.SetSizer(sizer)
        self.Fit()
