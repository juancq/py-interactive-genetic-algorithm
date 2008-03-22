import wx
import wx.lib.stattext
from gui import feedbackpanel

class IndividualPanel(feedbackpanel.FeedbackPanel):

    def __init__(self, parent, id, widget_style, grid, ui_data, size = None):
        #feedbackpanel.FeedbackPanel.__init__(self, parent, id, size = (300, 200))
        feedbackpanel.FeedbackPanel.__init__(self, parent, id)

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
                    wIndex += 1
                    sizer.Add(_widget, 1, border = 5, flag=wx.EXPAND)

                else:
                    sizer.Add((20, 5))


        sizer.Layout()
        self.sizer.Add(sizer)
        self.Layout()

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
            _widget = self.widgets['combobox'](self, -1, size = widget['size'], 
                    choices = eval(widget['value']))

        return _widget

#------------------------------------------#
