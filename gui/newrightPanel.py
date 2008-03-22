import wx, random
import coga_panel as coga
from iga.gacommon import gaParams

class RightPanel(wx.ScrolledWindow):
    def __init__(self, parent, params = None, size = None, color = "LIGHT BLUE", style = None):
        wx.ScrolledWindow.__init__(self, parent, -1, size=size, style = wx.DOUBLE_BORDER)

        self.parent = parent.GetParent()

        self.SetScrollbars(20,20,50,50)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.startButton = wx.Button(self, -1, 'Start')
        self.Bind(wx.EVT_BUTTON, self.onStart, self.startButton)
        self.sizer.Add(self.startButton)

        self.genLabel = wx.StaticText(self, -1, 'Generation 0')
        self.genLabel.Hide()
        self.sizer.Add(self.genLabel)
        self.sizer.Add((10, 10))

        # panels that display individuals from peers
        self.cogaPanel = coga.CollaboratePanel(self, name = "top")

        middleSpace = (50,10)

        # add top coga panel
        middleSizer = wx.BoxSizer(wx.HORIZONTAL)

        import display_panel
        self.displayPanel = display_panel.DisplayPanel(self)
        self.displayPanel.Hide()
        middleSizer.Add(self.displayPanel, 0, wx.EXPAND)

        middleSizer.AddSpacer(middleSpace)
        middleSizer.Add(self.cogaPanel, 0)#, wx.EXPAND) -- windows fix

        self.sizer.Add(middleSizer)

        self.SetSizer(self.sizer)
        self.Layout()

        self.generation = 1
        self.online = True


#-------------------------------------------#
    def connect(self, online):
        if online:
            self.online = True
            self.fillCoGAPanels()
        else:
            self.online = False
            self.cogaPanel.clear()

#-------------------------------------------#
    def getDisplay(self):
        return self.displayPanel

#-------------------------------------------#
    def onBack(self, e):
        panels_to_display, gen = gaParams.back(self.displayPanel)
        self.display(panels_to_display)

        self.genLabel.SetLabel('Generation %d' % gen)
        self.generation = gen

        return gen

#-------------------------------------------#
    def onSubmit(self, e):
        '''
        Take user selection and pass it to the GA for 
        fitness evaluation.
        '''
        feedback = None
        # get user input
        inject_genomes = self.cogaPanel.getPeerGenomes()
        if inject_genomes['best']:
            print 'inject_genomes ', inject_genomes
            feedback = None

            self.cogaPanel.clearFeedback()
            panels_to_display = gaParams.step(feedback, self.displayPanel, inject_genomes)
            self.display(panels_to_display)

            self.generation += gaParams.getVar('stepSize')
            self.genLabel.SetLabel('Generation %d' % self.generation)

        elif not inject_genomes['best']:
            feedback = self.displayPanel.getUserInput()
            if feedback:
                print 'inject_genomes ', inject_genomes

                self.cogaPanel.clearFeedback()
                panels_to_display = gaParams.step(feedback, self.displayPanel, inject_genomes)
                self.display(panels_to_display)

                self.generation += gaParams.getVar('stepSize')
                self.genLabel.SetLabel('Generation %d' % self.generation)

    
#-------------------------------------------#
    def onRun(self):
        self.startButton.Hide()
        self.currentGen = 0
        self.genLabel.SetLabel('Generation 1')
        self.genLabel.Show()
        self.displayPanel.Show()

#-------------------------------------------#
    def setGeneration(self, gen):
        self.genLabel.SetLabel('Generation %d' % gen)
        self.generation = gen

#-------------------------------------------#
    def fit(self):
        self.parent.Layout()

#-------------------------------------------#
    def display(self, panels_to_display):
        '''
        Takes a list of panels to display to be evaluated.
        '''
        displayPanel = self.displayPanel
        displayPanel.clear()

        expandFlag = bool(gaParams.getVar('expand'))
        displayPanel.addPanels(panels_to_display, expand=expandFlag)
        displayPanel.fit()

        self.fillCoGAPanels()

        self.Layout()

#-------------------------------------------#
    def fillCoGAPanels(self):
        '''
        Request genomes from peers to be displayed on collaboration
        panels.
        '''
        if self.online:
            subset_size = gaParams.getVar('population')['subset']['size']
            peer_list = gaParams.peer_list
            if peer_list:
                # for every peer, ping it, if alive then
                # get pickled genomes and draw them in the coga panels
                to_draw = []
                must = []
                status = {}
                for peer in peer_list:
                    status[peer.getName()] = 'offline'

                    if peer.online():
                        genome_objs = peer.getGenomes()
                        if genome_objs:
                            must.append(genome_objs[0])
                            to_draw.extend(genome_objs[1:])
                            status[peer.getName()] = 'online'

                self.parent.peerStatus(status)

                if to_draw:
                    self.cogaPanel.drawGenomes(must+random.sample(to_draw, subset_size-(len(must))))

#-------------------------------------------#
    def onStart(self, event):
        self.parent.onRun(event)

#-------------------------------------------#
