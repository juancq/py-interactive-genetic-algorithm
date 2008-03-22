import wx
from iga.gacommon import gaParams

class LeftPanel(wx.Panel):
    def __init__(self, parent, size = None, color = "LIGHT BLUE", style = None):
#wx.Panel.__init__(self, parent, -1, size=size, style = wx.RAISED_BORDER | wx.DOUBLE_BORDER)
        wx.Panel.__init__(self, parent, -1, size=size, style = wx.DOUBLE_BORDER)

        self.SetBackgroundColour('WHITE')
        self.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL,wx.FONTWEIGHT_BOLD))
        self.gaWindow = parent.GetParent()

        yaml = gaParams.getYaml()
        f = open('config/guiconfig.yml', 'r')
        widgets = yaml.load(f)
        widgets = widgets['widgets']
        f.close()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add((10, 14))

        # Population size label
        self.sizer.Add(wx.StaticText(self, -1, 'Population Size:'), 0, wx.ALIGN_CENTER)
        # Population size slider
        self.populationSlider = wx.Slider(self, -1, size=(100, 40), style= wx.SL_LABELS | wx.SL_AUTOTICKS)
        max = int(widgets['population']['max'])
        min = int(widgets['population']['min'])
        self.populationSlider.SetRange(min, max)
        self.populationSlider.SetValue(gaParams.getVar('population_size'))

        self.sizer.Add(self.populationSlider, 0, wx.ALIGN_CENTER)
        self.Bind(wx.EVT_SCROLL, self.onPopulationChange, self.populationSlider)

        xoRate, mutRate = gaParams.getGARates()
        # XO Rate Slider
        self.xoRateSlider = wx.Slider(self, -1, size = (100, 40), style = wx.SL_LABELS | wx.SL_AUTOTICKS)
        max = int(widgets['crossover']['max'])
        min = int(widgets['crossover']['min'])
        self.xoRateSlider.SetRange(min, max)
        self.xoRateSlider.SetValue(xoRate * max)

        # Add xo slider to sizer
        self.sizer.Add((10, 10))
        self.sizer.Add(wx.StaticText(self, -1, 'Crossover Rate:'), 0, wx.ALIGN_CENTER)
        self.sizer.Add(self.xoRateSlider, 0, wx.ALIGN_CENTER)

        self.Bind(wx.EVT_SCROLL, self.onCrossoverChange, self.xoRateSlider)

        # Mutation Rate
        self.mutBox = wx.TextCtrl(self, -1, size = (50, -1))
        self.mutBox.SetValue("%.3f" % mutRate)

        tempSizer = wx.BoxSizer(wx.HORIZONTAL)
        tempSizer.Add(wx.StaticText(self, -1, 'Mutation:'), 0, wx.ALIGN_CENTER_VERTICAL)
        tempSizer.Add(self.mutBox, 0)
        self.sizer.Add((10, 10))
        self.sizer.Add(tempSizer, 0, wx.ALIGN_CENTER)

        max = int(widgets['mutation']['max'])
        min = int(widgets['mutation']['min'])

        self.Bind(wx.EVT_TEXT, self.onMutationChange, self.mutBox)

        self.sizer.Add((10, 10))

        # Step size spinner control
        self.stepSize = wx.SpinCtrl(self, wx.ID_ANY, size = (50,23))
        self.stepSize.SetRange(1, 300)
        step = gaParams.getVar('stepSize') or 1
        self.stepSize.SetValue(step)

        self.Bind(wx.EVT_SPINCTRL, self.onSpin, self.stepSize)

        # Add spinner with text label to sizer
        tempSizer = wx.BoxSizer(wx.HORIZONTAL)
        tempSizer.Add(wx.StaticText(self, -1, 'Step Size:'), 0, wx.ALIGN_CENTER_VERTICAL)
        tempSizer.Add(self.stepSize)
        self.sizer.Add(tempSizer, 0, wx.ALIGN_CENTER)

        # edit mask button
        self.sizer.AddSpacer((10, 10))
        self.maskB = wx.Button(self, -1, 'Edit Mask')
        self.Bind(wx.EVT_BUTTON, self.onEditMask, self.maskB)
        self.sizer.Add(self.maskB, 0, wx.ALIGN_CENTER) 
        if not gaParams.getAppVars():
            self.maskB.Enable(False)

        # 8px spaces for widgets in same group
        # 10px for widgets not in the same group

        # -----------------------------------
        # peer stuff
        self.sizer.Add((10, 10))
        self.sizer.Add(wx.StaticLine(self), 0, wx.EXPAND)
        self.sizer.Add((10, 10))

        peers = {}
        peer_list = gaParams.getVar('peers')
        online = wx.Bitmap('gui/online.png')
        offline = wx.Bitmap('gui/offline.png')
        delete = wx.Bitmap('gui/delete.png')
        self.online, self.offline, self.delete = online, offline, delete

        # my status
        tmp_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.my_status = wx.StaticBitmap(self)
        self.my_status.SetBitmap(online)
        tmp_sizer.Add(self.my_status)
        tmp_sizer.Add(wx.StaticText(self, -1, 'Collaborate'))
        self.sizer.Add(tmp_sizer)

        # add peer button
        self.sizer.Add((10, 10))
        newButton = wx.Button(self, -1, 'Add Peer...')
        newButton.Bind(wx.EVT_BUTTON, self.onAddPeer, newButton)
        self.sizer.Add(newButton)
        self.sizer.Add((10, 10))

        self.names = {}
        # add list of peers
        all_peers_sizer = wx.BoxSizer(wx.VERTICAL)
        for peer in peer_list:
            id = wx.NewId()

            peer_sizer = wx.BoxSizer(wx.HORIZONTAL)
            peer_status = wx.StaticBitmap(self)
            peer_status.SetBitmap(offline)
            peer_name = wx.StaticText(self, -1, peer)
            peer_name.Bind(wx.EVT_LEFT_DOWN, self.onEditPeer, peer_name)
            peer_sizer.Add(peer_status)
            peer_sizer.Add(peer_name)

            peer_delete = wx.BitmapButton(self, id = id, bitmap = delete, 
                                                style = wx.ALIGN_RIGHT)
            self.Bind(wx.EVT_BUTTON, self.onDeletePeer, peer_delete)

            peer_sizer.Add(wx.StaticText(self, -1, '  '), 1)
            peer_sizer.Add(peer_delete)

            all_peers_sizer.Add(peer_sizer, 0, wx.EXPAND)
            peers[id] = {'name': peer,
                         'sizer': peer_sizer, 'status': peer_status}
            self.names[peer] = id
                
        self.sizer.Add(all_peers_sizer)
        self.peer_sizer = all_peers_sizer

        self.peers = peers
        self.status_bitmap = {}
        self.status_bitmap['online'] = online
        self.status_bitmap['offline'] = offline

        # Disconnect button
        self.sizer.AddSpacer((10, 10))
        self.disconnect = wx.Button(self, -1, 'Disconnect')
        self.Bind(wx.EVT_BUTTON, self.onDisconnect, self.disconnect)
        self.sizer.Add(self.disconnect, 0, wx.ALIGN_CENTER) 

        # refresh button
        self.sizer.AddSpacer((10, 10))
        self.refresh = wx.Button(self, wx.ID_REFRESH, '')
        self.Bind(wx.EVT_BUTTON, self.onRefresh, self.refresh)
        self.sizer.Add(self.refresh, 0, wx.ALIGN_CENTER) 

        # back button
        self.sizer.AddSpacer((10, 10))
        self.back = wx.Button(self, wx.ID_BACKWARD, '')
        self.back.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.onBack, self.back)
        self.sizer.Add(self.back, 0, wx.ALIGN_CENTER) 


        self.sizer.AddSpacer((10, 10))
        self.sizer.Add(wx.StaticLine(self), 0, wx.EXPAND)
        self.sizer.AddSpacer((10, 10))

        # Add submit button
        self.sizer.AddSpacer((10, 10))
        self.submit = wx.Button(self, -1, 'Step %d Gen' % step, size = (130,-1))
        self.submit.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.onSubmit, self.submit)
        self.sizer.Add(self.submit, 0, wx.ALIGN_CENTER)

        # final sizer and fitting stuff
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        self.sizer.Layout()
        self.sizer.Fit(self)
        self.sizer.SetSizeHints(self)
        self.Layout()

        # Keeps the textbox from having the default focus, which was annoying
        self.SetFocus()

        self.timestamp = 0.
        self.gen = 0

#-------------------------------------------#
    def onPopulationChange(self, event):
        '''
        Population slider event handler.
        '''
        popSize = self.populationSlider.GetValue()
        gaParams.setVar('population_size', popSize)

        #self.gaWindow.setPopSize(popSize)

#-------------------------------------------#
    def onStop(self):
        self.populationSlider.Enable(True)

#-------------------------------------------#
    def onRun(self):
        self.populationSlider.Enable(False)
        self.submit.Enable(True)

#-------------------------------------------#
    def onCrossoverChange(self, event):
        xoRate = self.xoRateSlider.GetValue()
        gaParams.setVar('crossover_prob', xoRate/100.0)

#-------------------------------------------#
    def onMutationChange(self, event):
        rate_str = self.mutBox.GetValue().strip()
        if rate_str and not rate_str=='.':
            rate = float(rate_str)
        else:
            rate = 0.0
        gaParams.setVar('mutation_prob', rate)

#-------------------------------------------#
    def onSpin(self, event):
        spin = self.stepSize.GetValue()
        gaParams.setVar('stepSize', spin)
        self.submit.SetLabel('Step %d Gen' % spin)

#-------------------------------------------#
    def peerStatus(self, status):
        '''
        Update the status icon of peer list.
        '''
        for peer in self.peers.itervalues():
            tmp = status[peer['name']]
            peer['status'].SetBitmap(self.status_bitmap[tmp])

#-------------------------------------------#
    def onEditMask(self, event):
        '''
        Edit the mask.
        '''
        import maskDialog
        dialog = maskDialog.MaskDialog(self)
        if dialog.ShowModal() == wx.ID_OK:
            list = dialog.list
            vars = {}
            for i in xrange(list.GetCount()):
                if list.IsChecked(i):
                    vars[str(list.GetString(i)).strip()] = True
                else:
                    vars[str(list.GetString(i)).strip()] = False
            gaParams.updateMask(vars)
                    
        dialog.Destroy()


#-------------------------------------------#
    def onSubmit(self, e):
        '''
        Take user selection and pass it to the GA for 
        fitness evaluation.
        '''
        self.right.onSubmit(e)
        if self.gen is 0:
            self.back.Enable(True)
            self.gen += self.stepSize.GetValue()

#-------------------------------------------#
    def onBack(self, event):
        '''
        Make the GA go back to a previous state.
        '''
        self.gen = self.right.onBack(event)
        if self.gen is 0:
            self.back.Enable(False)

#-------------------------------------------#
    def onDisconnect(self, event):
        '''
        When we want to run a session without peer
        collaboration.
        '''
        #button = event.GetEventObject()
        button = self.disconnect
        if button.GetLabel() == 'Disconnect':
            for peer in self.peers.itervalues():
                peer['status'].SetBitmap(self.status_bitmap['offline'])
            self.right.connect(False)
            button.SetLabel('Connect')
            self.my_status.SetBitmap(self.offline)
        else:
            self.right.connect(True)
            button.SetLabel('Disconnect')
            self.my_status.SetBitmap(self.online)

#-------------------------------------------#
    def onDeletePeer(self, event):
        button = event.GetEventObject()
        id = button.GetId()
        self.peers[id]['sizer'].DeleteWindows()

        name = self.peers[id]['name']
        gaParams.delPeer(name)

        del self.names[name]
        del self.peers[id]

        self.Layout()
        self.Refresh()

#-------------------------------------------#
    def peerEntry(self, peer):
        '''
            Create a new peer entry.
        '''
        id = wx.NewId()
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        peer_status = wx.StaticBitmap(self)
        peer_status.SetBitmap(self.offline)
        peer_name = wx.StaticText(self, -1, peer)
        sizer.Add(peer_status)
        sizer.Add(peer_name)

        peer_delete = wx.BitmapButton(self, id, bitmap = self.delete, 
                                            style = wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_BUTTON, self.onDeletePeer, peer_delete)

        sizer.Add(wx.StaticText(self, -1, '  '), 1)
        sizer.Add(peer_delete)

        self.peer_sizer.Add(sizer, 0, wx.EXPAND)
        self.peers[id] = {'name': peer, 'widget': sizer, 'status': peer_status}
        self.names[peer] = id

        gaParams.addPeer(peer)
        self.Layout()
        self.Refresh()
        self.onRefresh(None)

#-------------------------------------------#
    def onAddPeer(self, event):
        '''
        Handle addition of peer event.
        Ask for IP address, add it to list if not duplicate.
        '''
        dialog = wx.TextEntryDialog(self, 'Enter IP address of new peer:', 'Add New Peer')
        if dialog.ShowModal() == wx.ID_OK:
            newPeer = str(dialog.GetValue().strip())
            if not self.peers.has_key(newPeer):
                self.peerEntry(newPeer)

        dialog.Destroy()

#-------------------------------------------#
    def onEditPeer(self, event):
        '''
        Edit an existing peer IP.
        '''
        peer_obj = event.GetEventObject()
        def_value = peer_obj.GetLabel()
        dialog = wx.TextEntryDialog(self, 'Edit Peer IP Address', 'Edit Peer', def_value)
        if dialog.ShowModal() == wx.ID_OK:
            newPeer = str(dialog.GetValue().strip())
            if not self.names.has_key(newPeer):
                peer_obj.SetLabel(newPeer)
                gaParams.addPeer(newPeer)
                gaParams.delPeer(def_value)

                id = self.names.pop(def_value)
                self.names[newPeer] = id
                self.peers[id]['name'] = newPeer

#-------------------------------------------#
    def onRefresh(self, event):
        self.right.fillCoGAPanels()

#-------------------------------------------#
