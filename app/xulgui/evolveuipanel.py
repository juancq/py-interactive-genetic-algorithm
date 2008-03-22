import wx
import wx.lib.stattext
from gui import feedbackpanel

class IndividualPanel(feedbackpanel.FeedbackPanel):
    font_list = None

    def __init__(self, parent, id, style, grid, ui_data, size = None):
        feedbackpanel.FeedbackPanel.__init__(self, parent, id)

        if IndividualPanel.font_list is None:
            faces = wx.FontEnumerator.GetFacenames()
            IndividualPanel.faces = faces

        gridSize = [10,2]
        
        widgets = {}
        widgets['label'] = wx.lib.stattext.GenStaticText
        widgets['slider'] = wx.Slider
        widgets['button'] = wx.Button
        widgets['textbox'] = wx.TextCtrl
        widgets['combobox'] = wx.Choice
        self.widgets = widgets

        bgcolor = (style['window_red'], style['window_green'], 
                        style['window_blue'])
        widget_color = (style['widget_red'], style['widget_green'], 
                        style['widget_blue'])

        self.SetBackgroundColour(bgcolor)
        #self.SetForegroundColour(bgcolor)
        #self.SetForegroundColour(tuple(widget_style[0]))

        font = wx.Font(11, wx.NORMAL, wx.NORMAL, wx.NORMAL)
        font.SetFaceName(IndividualPanel.faces[int(style['font_face'])])
        self.SetFont(font)
        vgap = style['vgap']
        hgap = style['hgap']
        sizer = wx.GridSizer(gridSize[0], gridSize[1], vgap, hgap)

        for j in xrange(gridSize[0]):
            for k in xrange(gridSize[1]):
                if grid[j*gridSize[1] + k] > 0:
                    _widget = self.addWidget(ui_data[grid[j*gridSize[1]+k]])
                    # set bg color
                    _widget.SetBackgroundColour(widget_color)
                    sizer.Add(_widget, 1, border = 0, flag=wx.EXPAND)

                else:
                    sizer.Add((20, 4))


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
