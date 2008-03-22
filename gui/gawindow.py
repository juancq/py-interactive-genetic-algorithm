import wx
from iga.gacommon import gaParams
from os import getcwd

#---------------------------------------#
# Menu ids
#---------------------------------------#
ID_RUN = wx.NewId()
ID_STOP = wx.NewId()
ID_EXIT = wx.NewId()
ID_SAVE_GA_STATE = wx.NewId()
ID_OPEN_GA_STATE = wx.NewId()

ID_OPEN_APP = wx.NewId()

#---------------------------------------#


class GAWindow(wx.Frame):
    def __init__(self, parent = None, id = wx.NewId(), title = 'UI Evolver'):
        '''
        GUI window for the GA.
        '''
        wSize = (850, 900)
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, size = wSize, pos = (200,0), 
                        style = wx.DEFAULT_FRAME_STYLE)
        self.CreateStatusBar()

        # tools menu specification
        toolsMenu = wx.Menu()
        toolsMenu.Append(ID_RUN, "&Run GA\tCtrl+R", "Start/restart the GA.")
        toolsMenu.Append(ID_STOP, "&Stop GA\tCtrl+K", "Stop the GA.")
        toolsMenu.AppendSeparator()


        # id, label text, status bar message
        # file menu specification
        fileMenu = wx.Menu()
        fileMenu.Append(ID_OPEN_APP, "Open Application...\tCtrl+O", "Open application file.")
        fileMenu.AppendSeparator()
        fileMenu.Append(ID_EXIT, "E&xit\tCtrl+Q", "Terminate the program.")

        # menubar specification
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(toolsMenu, "&GA")
        self.SetMenuBar(menuBar)

        # event handlers for menu items

        wx.EVT_MENU(self, ID_RUN,  self.onRun )
        wx.EVT_MENU(self, ID_STOP,  self.onStop )
        wx.EVT_MENU(self, ID_EXIT, self.onExit)
        wx.EVT_MENU(self, ID_SAVE_GA_STATE, self.onSaveGAState)
        wx.EVT_MENU(self, ID_OPEN_GA_STATE, self.onOpenGAState)

        wx.EVT_MENU(self, ID_OPEN_APP, self.onOpenApp) 
        wx.EVT_MENU(self, ID_EXIT, self.onExit)
        self.Bind(wx.EVT_CLOSE, self.onExit, self)


        # IGA panel, where user interacts with IGA
        import iGAPanel
        self.iGAPanel = iGAPanel.iGAPanel(self, size = wSize)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.iGAPanel, 1, wx.EXPAND)
        sizer.Fit(self)
        sizer.SetSizeHints(self)

        self.SetSizer(sizer)

        self.Layout()

        self.env = None
        self.SetTitle('IGA Client - %s' % gaParams.getAppName())
        self.Show(True)
                

#-------------------------------------------#
    def onExit(self, event):
        '''
        Closes application.
        '''
        gaParams.exit()
        self.Destroy()

#-------------------------------------------#
    def onStop(self, event):
        '''
        Stop running the GA.
        '''
        return

#-------------------------------------------#
    def onOpenApp(self, event):
        '''
            Load application specific config file.
        '''
        dirname = getcwd() + '/config'
        dlg = wx.FileDialog(self, "Load Application File", dirname, "", 'YAML files (.yml)|*.yml|All files (*)|*', wx.OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            gaParams.reset()
            gaParams.fileArgs('config/' + filename)
            self.SetTitle('IGA Client - %s' % gaParams.getAppName())

        dlg.Destroy()


#-------------------------------------------#
    def onOpenGAState(self, event):
        '''
        Open GA state file dialog.
        '''
        dirname = ''
        dlg = wx.FileDialog(self, "GA State Load File", dirname, "", 'GA files (.ga)|*.ga|All files (*)|*', wx.OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.controlServer.loadGAState(path)

        dlg.Destroy()

#-------------------------------------------#
    def onSaveGAState(self, event):
        '''
        Save GA state file dialog.
        '''
        dirname = ''
        dlg = wx.FileDialog(self, "GA State Load File", dirname, "", 'GA files (.ga)|*.ga|All files (*)|*', wx.SAVE)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.controlServer.saveGAState(path)
            
        dlg.Destroy()

#-------------------------------------------#
    def onAbout(self, event):
        '''
        About application dialog.
        '''
        from wx.lib.pydocview import AboutDialog
        dlg = AboutDialog(self, wx.Image('aboutdialog.bmp'))
        dlg.Show()


#-------------------------------------------#
    def onRun(self, event):
        '''
        Runs the GA.
        '''
        self.iGAPanel.onRun(event)

#-------------------------------------------#


        # ----------------------------------------------
        # Deprecated code
        # ----------------------------------------------
        # help menu specification
        #helpMenu = wx.Menu()
        #helpMenu.Append(ID_ABOUT, "About", "Brief description of the program.")
        #menuBar.Append(helpMenu, "Help")

        #toolsMenu.Append(wx.NewId(), "Generate Code...", "Generate code for an individual in the population.")
        #toolsMenu.AppendSeparator()
        #toolsMenu.Append(wx.NewId(), "Explore Population...", "Browse individuals in the population.")
        #toolsMenu.AppendSeparator()

        #wx.EVT_MENU(self, ID_ABOUT,  self.onAbout )
        #wx.EVT_MENU(self, ID_OPTIONS, self.onOptions)

        # window tabs
        #notebook = wx.Notebook(self, -1)
        #notebook.AddPage(self.iGAPanel, "iGA")
        #sizer.Add(notebook, 1, wx.EXPAND)
        # options dialog
        #self.options = optionsDialog.OptionsDialog(self, id = wx.ID_ANY, params = self.gaParams)
        # ----------------------------------------------
        # END Deprecated code
        # ----------------------------------------------
##-------------------------------------------#
#    def onOptions(self, event):
#        '''
#        Shows the options dialog.
#        '''
#        self.options.Show()


#ID_OPTIONS = wx.NewId()
#ID_ABOUT = wx.NewId()

        #fileMenu.Append(ID_SAVE_GA_STATE, "&Save GA State...\tCtrl+S", "Save the current state of the GA to a file.")
        #fileMenu.Append(ID_OPEN_GA_STATE, "Open GA State...", "Open a saved state of the GA.")
        #fileMenu.AppendSeparator()

