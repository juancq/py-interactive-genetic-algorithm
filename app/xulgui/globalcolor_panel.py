import wx
import wx.lib.stattext

class IndividualPanel(wx.Panel):

    def __init__(self, parent, id, widget_style, grid, ui_data, size = None):
        wx.Panel.__init__(self, parent = parent, size = (300,200), style = wx.SIMPLE_BORDER)

        self.parent = parent
        self.id = id

        gridSize = [10,2]
        
        widgets = {}
        widgets['label'] = wx.lib.stattext.GenStaticText
        widgets['slider'] = wx.Slider
        widgets['button'] = wx.Button
        widgets['textbox'] = wx.TextCtrl
        widgets['combobox'] = wx.Choice
        self.widgets = widgets

        #self.SetBackgroundColour(tuple(widget_style[0]))
        self.SetBackgroundColour(widget_style[0])

        sizer = wx.GridSizer(gridSize[0], gridSize[1], 2, 2)

        wIndex = 1
        for j in xrange(gridSize[0]):
            for k in xrange(gridSize[1]):
                if grid[j*gridSize[1] + k] > 0:
                    _widget = self.addWidget(ui_data[grid[j*gridSize[1]+k]])
                    # set bg color
                    _widget.SetBackgroundColour(widget_style[wIndex])
                    #_widget.SetForegroundColour(widget_style[0])
                    sizer.Add(_widget, 1, border = 5, flag=wx.EXPAND)

                else:
                    sizer.Add((20,5))


        sizer.Layout()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.bestLabel = wx.lib.stattext.GenStaticText(self, -1, "Best:")
        self.worstLabel = wx.lib.stattext.GenStaticText(self, -1, "Worst:")

        self.bestLabel.SetFont(wx.Font(11, wx.NORMAL, wx.NORMAL, wx.BOLD))
        self.worstLabel.SetFont(wx.Font(11, wx.NORMAL, wx.NORMAL, wx.BOLD))
        self.bestLabel.Hide()
        self.worstLabel.Hide()

        self.sizer.Add(self.bestLabel, 0, wx.EXPAND)
        self.sizer.Add(self.worstLabel, 0, wx.EXPAND)
        self.sizer.Add(sizer)

        self.Layout()


        #self.sizer.Fit(self);
        #self.sizer.SetSizeHints(self)
        self.SetSizer(self.sizer)


        self.Bind(wx.EVT_LEFT_DOWN, self.bestSelect, self)
        self.Bind(wx.EVT_RIGHT_DOWN, self.worstSelect, self)

        #self.Bind(wx.EVT_LEFT_DCLICK, self.parent.onBestSelect, self)
        #self.Bind(wx.EVT_RIGHT_DCLICK, self.parent.onWorstSelect, self)


#------------------------------------------#
    def getID(self):
        return self.id

#------------------------------------------#
    def unSelect(self):
        self.bestLabel.Hide()
        self.worstLabel.Hide()

#------------------------------------------#
    def bestSelect(self, event):
        self.bestLabel.Show()
        self.worstLabel.Hide()
        self.Layout()
        self.parent.onBestSelect(self.id)

#------------------------------------------#
    def worstSelect(self, event):
        self.bestLabel.Hide()
        self.worstLabel.Show()
        self.Layout()
        self.parent.onWorstSelect(self.id)


#------------------------------------------#
    def addWidget(self, widget):
        _widget = None
        if widget['name'] == 'label':
            _widget = self.widgets['label'](self, -1, widget['value'])

        elif widget['name'] == 'textbox':
            _widget = self.widgets['textbox'](self, -1, widget['value'])

        elif widget['name'] == 'button':
            _widget = self.widgets['button'](self, -1, widget['value'])

        elif widget['name'] == 'slider':
            _widget = self.widgets['slider'](self, -1, size = widget['size'])

        elif widget['name'] == 'combobox':
            _widget = self.widgets['combobox'](self, -1, size = widget['size'], choices = eval(widget['value']))

        return _widget

#------------------------------------------#
