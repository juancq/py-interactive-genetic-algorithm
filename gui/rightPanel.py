import wx, random
import collaborate_panel as coga
from iga.gacommon import gaParams
from pickle import loads

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
        tCogaPanel = coga.CollaboratePanel(self, name = "top", orientation = wx.HORIZONTAL)
        lCogaPanel = coga.CollaboratePanel(self, name = "left")
        rCogaPanel = coga.CollaboratePanel(self, name = "right")
        bCogaPanel = coga.CollaboratePanel(self, name = "bottom", orientation = wx.HORIZONTAL)
        self.coga_panel = [tCogaPanel, bCogaPanel, lCogaPanel, rCogaPanel]

        extraSp = (20,20)
        # add top coga panel
        self.sizer.Add(tCogaPanel, 0, wx.EXPAND)

        middleSizer = wx.BoxSizer(wx.HORIZONTAL)

        middleSizer.Add(lCogaPanel, 0, wx.EXPAND)

        import display_panel
        self.displayPanel = display_panel.DisplayPanel(self)
        self.displayPanel.Hide()
        middleSizer.Add(self.displayPanel, 0, wx.EXPAND)

        middleSizer.Add(rCogaPanel, 0, wx.EXPAND)

        self.sizer.Add(middleSizer)
        self.sizer.Add(bCogaPanel, 0, wx.EXPAND)

        self.SetSizer(self.sizer)

        self.Layout()

        self.generation = 1
        self.tCogaPanel = tCogaPanel
        self.lCogaPanel = lCogaPanel
        self.rCogaPanel = rCogaPanel
        self.bCogaPanel = bCogaPanel


#-------------------------------------------#
    def onSubmit(self, e):
        '''
        Take user selection and pass it to the GA for 
        fitness evaluation.
        '''
        # get user input
        feedback = self.displayPanel.getUserInput()
        if feedback:
            # check collaborative panels to see if any genomes need to be added
            # to gene pool
            inject_genomes = []
            for cpanel in self.coga_panel:
                inject_genomes.extend(cpanel.getPeerGenomes())
            print 'inject_genomes ', inject_genomes

            panels_to_display = gaParams.step(feedback, self.displayPanel, inject_genomes)
            self.display(panels_to_display)

            self.generation += gaParams.getVar('stepSize')
            self.genLabel.SetLabel('Generation %d' % self.generation)
    
#-------------------------------------------#
    def onRun(self):
        self.startButton.Hide()
        self.currentGen = 0
        self.genLabel.SetLabel('Generation 1')
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
        peer_list = gaParams.peer_list
        peer_num = min(4, len(peer_list))
        panel_counter = 0
        row_size = gaParams.getVar('rowSize')
        peer_genome = []
        # for every peer, ping it, if alive then
        # get pickled genomes and draw them in the coga panels

        status = []
        for peer in peer_list:
            if peer.online():
                genome = peer.proxy.getGenomes()
                genome_objs = loads(genome)
                peer_genome.append(genome_objs)
                to_display = row_size
                if self.coga_panel[panel_counter].orientation == wx.HORIZONTAL:
                    to_display += 2
                self.coga_panel[panel_counter].drawGenomes(genome_objs[:to_display])
                panel_counter += 1
                status.append([peer.getName(), 'online'])
            else:
                status.append([peer.getName(), 'offline'])

        self.parent.peerStatus(status)

        if peer_genome:
            # fill the rest of the empty coga panels with
            # remaining genomes, if any
            leftover = []
            for genome in peer_genome:
                leftover.extend(genome[row_size:])
            random.shuffle(leftover)

            for panel in self.coga_panel[panel_counter:]:
                to_display = row_size
                if panel.orientation == wx.HORIZONTAL:
                    to_display += 2
                panel.drawGenomes(leftover[:to_display])
                del(leftover[:to_display])


        #for i in xrange(peer_num):
        #    if peer_list[i].online():
        #        genome = peer_list[i].proxy.getGenomes()
        #        genome_objs = loads(genome)
        #        peer_genome.append(genome_objs)
        #        panels = gaParams.draw(self.coga_panel[panel_counter], genome_objs[:row_size])
        #        self.coga_panel[panel_counter].addPanels(panels)
        #        panel_counter += 1

        self.peer_genome = peer_genome

#-------------------------------------------#
    def onStart(self, event):
        self.parent.onRun(event)

#-------------------------------------------#
