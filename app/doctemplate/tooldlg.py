import wx

class InsertDialog(wx.Dialog):

    def __init__(self, parent, shape_size):
        wx.Dialog.__init__(self, parent, wx.NewId(), 'Insert...')

        self.shape_size = shape_size
        # Setting up Toolbar
        self.toolbar1 = wx.ToolBar(self, id=-1, style=wx.TB_HORIZONTAL | wx.NO_BORDER |
                                        wx.TB_FLAT | wx.TB_TEXT)
        INSERT_IMG = wx.NewId()
        INSERT_COLOR = wx.NewId()
        INSERT_TEXT = wx.NewId()
        self.toolbar1.AddSimpleTool(INSERT_IMG,
              wx.Image('app/doctemplate/insert_img.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(),
              'Insert Image', '')
        self.toolbar1.AddSimpleTool(INSERT_TEXT,
              wx.Image('app/doctemplate/insert_text.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(),
              'Insert Text', '')
        #self.toolbar1.AddSeparator()
        self.toolbar1.AddSimpleTool(INSERT_COLOR,
              wx.Image('app/doctemplate/insert_color.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(),
              'Insert Color', '')
        self.toolbar1.Realize()
        self.toolbar1.Bind(wx.EVT_TOOL, self.OnInsertImg, id=INSERT_IMG)
        self.toolbar1.Bind(wx.EVT_TOOL, self.OnInsertText, id=INSERT_TEXT)
        self.toolbar1.Bind(wx.EVT_TOOL, self.OnInsertColor, id=INSERT_COLOR)

        self.Fit()

        self.image = None
        self.text = None
        self.color = None

#-------------------------------------------#
    def OnInsertImg(self, event):
        # Ask the user to load an image
        dirname = ''
        dlg = wx.FileDialog(self, "Insert Image", dirname, "", 'All files (*)|*|PNG (*png)|*png|BMP (*bmp)|*bmp|JPEG (*jpg)|*jpg', wx.OPEN)

        ret_value = wx.ID_CANCEL
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.image = path
            ret_value = wx.ID_OK
        dlg.Destroy()
        self.EndModal(ret_value)

#-------------------------------------------#
    def OnInsertText(self, event):
        from textDialog import TextDialog
        dlg = TextDialog(self, 'Insert Text', self.shape_size)

        ret_value = wx.ID_CANCEL
        if dlg.ShowModal() == wx.ID_OK:
            text = dlg.GetValue()
            self.text = text
            ret_value = wx.ID_OK
        dlg.Destroy()
        self.EndModal(ret_value)

#-------------------------------------------#
    def OnInsertColor(self, event):
        colorDialog = wx.ColourDialog(self)

        ret_value = wx.ID_CANCEL
        if colorDialog.ShowModal() == wx.ID_OK:
            data = colorDialog.GetColourData()
            # color tuple
            colorScheme = data.GetColour().Get()
            ret_value = wx.ID_OK
            self.color = colorScheme

        colorDialog.Destroy()
        self.EndModal(ret_value)

#-------------------------------------------#
