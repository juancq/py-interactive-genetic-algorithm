import wx
import wx.lib.plot as libplot
from gui import feedbackpanel

class PlotPanel(feedbackpanel.FeedbackPanel):
    def __init__(self, parent, id, data, data_max):
        feedbackpanel.FeedbackPanel.__init__(self, parent, id)

        plot = libplot.PlotCanvas(self)
        self.id = id

        problem_size = data_max
        target = [(0,0), (data_max,data_max)]
        candidate = [(0,0), (data_max, data)]

        target_line = libplot.PolyLine(target, legend='Target', colour='green', width=3)
        candidate_line = libplot.PolyLine(candidate, legend='Candidate', colour='red', width=3)
        gc = libplot.PlotGraphics([target_line, candidate_line], '', '', '')

        plot.Draw(gc, xAxis= (0,problem_size), yAxis= (0,problem_size))
        plot.SetEnableLegend(True)
        plot.SetGridColour('black')

        self.sizer.Add(plot, 1, wx.EXPAND)
        self.Layout()

#------------------------------------------#
