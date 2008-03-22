import wx
import wx.lib.plot as plot

class IndividualPanel(plot.PlotCanvas):
    def __init__(self, parent, id, data, data_max):
        plot.PlotCanvas.__init__(self, parent = parent)#, size=(400,400))

        self.parent = parent

        self.id = id

        problem_size = data_max
        target = [(0,0), (data_max,data_max)]
        candidate = [(0,0), (data_max, data)]

        target_line = plot.PolyLine(target, legend='Target', colour='green', width=3)
        candidate_line = plot.PolyLine(candidate, legend='Candidate', colour='red', width=3)
        gc = plot.PlotGraphics([target_line, candidate_line], '', '', '')
        self.Draw(gc, xAxis= (0,problem_size), yAxis= (0,problem_size))

        self.SetEnableLegend(True)
        self.SetGridColour('black')

        self.Bind(wx.EVT_LEFT_DOWN, self._bestSelect, self)
        self.Bind(wx.EVT_RIGHT_DOWN, self._worstSelect, self)

        self.Bind(wx.EVT_LEFT_DCLICK, parent.onBestSelect, self)
        self.Bind(wx.EVT_RIGHT_DCLICK, parent.onWorstSelect, self)

#------------------------------------------#
    def OnMouseLeftDown(self,event):
        self.parent.onBestSelect(self.id)

#------------------------------------------#
    def OnMouseRightDown(self,event):
        self.parent.onWorstSelect(self.id)

#------------------------------------------#
    def getID(self):
        return self.id

#------------------------------------------#
    def unSelect(self):
        self.bestLabel.Hide()
        self.worstLabel.Hide()

#------------------------------------------#
    def _bestSelect(self,event):
        print 'best selected ', self.id

#------------------------------------------#
    def _worstSelect(self,event):
        print 'worst selected ', self.id

#------------------------------------------#
    def bestSelect(self):
        print 'best selected ', self.id
        self.bestLabel.Show()
        self.worstLabel.Hide()
        self.Layout()

#------------------------------------------#
    def worstSelect(self):
        print 'worst selected ', self.id
        self.bestLabel.Hide()
        self.worstLabel.Show()
        self.Layout()

