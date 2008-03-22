import xmlrpclib
from socket import setdefaulttimeout
setdefaulttimeout(2.)
from pickle import loads


#-------------------------------------------#
class PeerNode:
    def __init__(self, ip_address, app_name, port = 55800):
        self.ip_address = ip_address
        self.app_name = app_name
        self.proxy = None
        self.connected = False
        self.port = port
        self.connect()

    def getName(self):
        return self.ip_address

    def connect(self):
        self.proxy = xmlrpclib.Server("http://%s:%i" % 
                        (self.ip_address, self.port))
        try:
            self.proxy.test()
            self.connected = True
        except:
            self.connected = False
            self.proxy = None

        return self.connected


    def getGenomes(self):
        '''
        Check if genomes from peers are the same type as my genomes.
        '''
        peer_data = self.proxy.getGenomes()
        genomes, app_name = loads(peer_data)
        if app_name == self.app_name:
            return genomes
        else:
            return []


    def online(self):
        '''
        Test if node is connected. 
        If the node is online, then do a test call.
        If not online, then try to reconnect.
        '''
        if self.connected:
            try:
                self.proxy.test()
                return True
            except:
                self.connected = False
                self.proxy = None
                return False
        else:
            # try to connect
            result = self.connect()
            return result


#-------------------------------------------#
class CommonParams:
    '''
    Holder for shared variables.
    The variables are set and modified by the GUI.
    The vars are retrieved by the GA.
    '''

    def __init__(self):
        self.ga = None
        self.params = None
        self.peer_list = None
        self.server_thread = None
        self.app_name = None
        self.yaml_file = None
        self.dirty = False

#-------------------------------------------#
    def reset(self):
        '''
            Reset server state.
        '''
        self.exit()
        if self.ga:
            del self.ga
        self.ga = None
        self.params = None
        self.peer_list = None
        self.server_thread = None
        self.app_name = None
        self.yaml_file = None
        self.dirty = False

#-------------------------------------------#
    def getYaml(self):
        try:
            import yaml
        except:
            import _yaml_ as yaml

        return yaml

#-------------------------------------------#
    def fileArgs(self, yaml_file):
        '''
        Parse config files.
        '''
        self.yaml_file = yaml_file
        yaml = self.getYaml()
        f = open(yaml_file, 'r')
        params = yaml.load(f)
        f.close()

        # helper func which recursively inherits dictionaries
        def fillDict(_params, _inherit_params):
            for _key, _value in _params.iteritems():
                if type(_value) is dict and _inherit_params.has_key(_key):
                    fillDict(_value, _inherit_params[_key])
                else:
                    _inherit_params[_key] = _value

        # parse any files from which the
        # yaml config is being inherited from
        if params.has_key('inherits'):
            inherit_params = {}
            base_files = params['inherits'][:]
            base_files.reverse()
            for filename in base_files:
                # fill temp dictionary with inherited attributes
                f = open('config/'+filename, 'r')
                base_params = yaml.load(f)
                f.close()

                # values not defined in derived file are pulled from inherited file
                fillDict(inherit_params, base_params)
                inherit_params = base_params

            # fill our dictionary with values inherited
            fillDict(params, inherit_params)
            self.params = inherit_params                       
        else:
            self.params = params

        self.app_name = self.params['application']['name']

#-------------------------------------------#
    def exit(self):
        '''
        Kill running server.
        '''
        if self.server_thread:
            import time
            proxy = xmlrpclib.Server("http://localhost:%i" % self.params['port'])
            # The first call sets the kill flag
            proxy.__kill__()
            time.sleep(.1)
            # because of racing conditions we may have to call
            # kill again to terminate the server
            try:
                proxy.__kill__()
            except:
                pass
            del(proxy)
            self.server_thread.join()


        if self.dirty:
            self.yaml_file
            f = open(self.yaml_file, 'r')
            params = f.readlines()
            f.close()

            i = 0
            for line in params:
                if line.strip().startswith('peers'):
                    params[i] = 'peers: %s\n' % str(self.params['peers'])
                    break
                i += 1

            f = open(self.yaml_file, 'w')
            for line in params:
                f.write(line)
            f.close()


#-------------------------------------------#
    def addPeer(self, name):
        '''
        Add peer node.
        Duplicate check is done by GUI.
        '''
        plist = self.peer_list

        if plist is None:
            if self.params.has_key('peers'):
                self.params['peers'].append(name)
            else:
                self.params['peers'] = [name]

        else:
            plist.append(PeerNode(name, self.app_name))
            self.params['peers'].append(name)

        self.dirty = True

#-------------------------------------------#
    def delPeer(self, name):
        '''
        Delete the given peer from list.
        '''
        plist = self.peer_list
        if plist is None:
            self.params['peers'].remove(name)
        else:
            for peer in self.peer_list:
                if name == peer.getName():
                    self.peer_list.remove(peer)
                    self.params['peers'].remove(name)
                    break

        self.dirty = True

#-------------------------------------------#
    def pingPeers(self):
        '''
        Create connections to each peer.
        '''
        from p2p import serverthread
        self.server_thread = serverthread.ServerThread()
        self.server_thread.start()

        if self.peer_list is None:
            if self.params.has_key('peers'):
                peer_list = []
                for peer in self.params['peers']:
                    peer_list.append(PeerNode(peer, self.app_name))

                self.peer_list = peer_list
        else:
            self.peer_list = []

#-------------------------------------------#
    def getGARates(self):
        '''
        Get crossover and mutation rates.
        '''
        return self.params['crossover']['prob'], self.params['mutation']['prob']

#-------------------------------------------#
    def setVar(self, name, value):
        '''
        Set variable in the attributes dictionary, or create new if var doesn't exist.
        directly.
        '''
        if name == 'crossover_prob':
            self.params['crossover']['prob'] = value
        elif name == 'mutation_prob':
            self.params['mutation']['prob'] = value
        elif name == 'population_size':
            self.params['population']['size'] = value
        else:
            self.params[name] = value


#-------------------------------------------#
    def setVars(self, varNames, values):
        '''
        Sets variables from list in the attributes dictionary, or create new if var doesn't exist.
        directly.
        '''
        for i in xrange(len(varNames)):
            self.params[varNames[i]] = values[i]

#-------------------------------------------#
    def getVar(self, name):
        '''
        Get variable from the attributes dictionary. To keep from accessing the dictionary
        directly.
        '''
        if name == 'crossover_prob':
            return self.params['crossover']['prob']
        elif name == 'mutation_prob':
            return self.params['mutation']['prob']
        elif name == 'population_size':
            return self.params['population']['size']

        else:
            if self.params.has_key(name):
                return self.params[name]
            else:
                print 'Variable %s does not exist!' % name
                return None

#-------------------------------------------#
    def getVars(self, varNames):
        '''
        Get list of variables from the attributes dictionary. To keep from accessing the dictionary
        directly.
        '''
        returnList = []
        for name in varNames:
            if self.params.has_key(name):
                returnList.append(self.params[name])
            else:
                print 'Variable %s does not exist!' % name

        return returnList


#-------------------------------------------#
    def setArgs(self, args):
        '''
        Update settings based on command line arguments.
        Command line arguments override file defaults.
        '''
        if args:
            self.setVars(args.keys(), args.values())


#-------------------------------------------#
    def consoleGA(self):
        '''
        Run non-interactive GA.
        '''
        from ga import GA
        ga = GA(self.params)
        ga.run()

#-------------------------------------------#
    def step(self, user_feedback, display_panel, inject_genomes):
        '''
        Take the user input and the individuals to inject
        and step n generations.
        '''
        print 'user_feedback', user_feedback
        return self.ga.step(user_feedback, display_panel, inject_genomes)

#-------------------------------------------#
    def onRun(self, display_panel):
        '''
        Called when GA is created.
        '''
        self.pingPeers()

        from iga import IGA
        self.ga = IGA(self.params)

        return self.ga.run(display_panel)

#-------------------------------------------#
    def draw(self, parent_panel, genomes):
        '''
        Take a list of genomes and have the app file
        create panels for them.
        '''
        panels = self.ga.draw(parent_panel, genomes)
        return panels

#-------------------------------------------#
    def getAppVars(self):
        '''
        Return a reference to the application variables.
        '''
        if self.params['application'].has_key('vars'):
            return self.params['application']['vars']
        else:
            return None

#-------------------------------------------#
    def updateMask(self, mask_vars):
        '''
        Used by the peer handler.
        Returns a list of genomes to be displayed
        on the screen of the requesting peer.
        '''
        vars = self.getAppVars()
        if vars:
            to_update = []
            for var_name, var_state in mask_vars.iteritems():
                if var_state is not vars[var_name]['mask']:
                    to_update.append(var_name)
                    vars[var_name]['mask'] = var_state
            
            # if GA is running, then update pop with new mask
            if self.ga:
                self.ga.updateMask(to_update)


#-------------------------------------------#
    def back(self, display_panel):
        return self.ga.back(display_panel)

#-------------------------------------------#
    def getAppName(self):
        return self.app_name

#-------------------------------------------#
    def getNGenomes(self, genome_num):
        '''
        Used by the peer handler.
        Returns a list of genomes to be displayed
        on the screen of the requesting peer.
        '''
        subset = self.ga.getSubset()
        # just return the subset displayed on the peers' screens

        #random_inds = self.ga.getNRandom(len(subset))
        #subset.extend(random_inds)
        return subset, self.app_name


#-------------------------------------------#


gaParams = CommonParams()
