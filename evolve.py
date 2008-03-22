#!/usr/bin/python

import getopt, sys

def parse():
    try:
        start_index = 1
        if len(sys.argv) > 1:
            if not sys.argv[1].startswith('-'):
                start_index = 2
        optlist, args = getopt.getopt(sys.argv[start_index:], 'c:d:ef:g:hm:n:o:s:p:', ['folder', 'help', 'popsize=', 'generations=', 'selection='])
    except:
        optlist = []

    _args = {}

    # Parse command line
    for o, value in optlist:
        if o == "-c":
            # Who to compare to based on the user input
            value = value.strip()
            _args['compare'] = value

        elif o == "-e":
            # Use elitist selection
            _args['elitist'] = True

        elif o in ("-f"):
            # other config file name
            _args['config'] = value.strip()

        elif o in ("-n", '--popsize'):
            # Specify population size in command line
            _args['popSize'] = int(value.strip())
        elif o == "-o":
            # Output file
            _args['output'] = value.strip()
        elif o == "-m":
            # Output file
            _args['mutation'] = float(value.strip())
        elif o == "-d":
            _args['displayNum'] = value.strip()

        elif o in ("-s", '--step'):
            # number of iterations
            _args['stepSize'] = int(value.strip())

        elif o == "--generations":
            # number of iterations
            _args['generations'] = int(value.strip())

        elif o == "--selection":
            # number of iterations
            value = value.strip()
            if value.startswith('roul'):
                _args['selection'] = 'roulette'
            elif value.startswith('tour'):
                _args['selection'] = 'tournament'
            else:
                _args['selection'] = value

        elif o == "-p":
            # port number
            _args['port'] = int(value.strip())

        elif o == "-g":
            # port number
            _args['gui'] = value.strip()


        elif o in ("-h", '--help'):
            # display help
            print 'Help Menu:'
#            helpStr = '''
#        -h, --help          Display help menu
#        -m                  Mutation rate
#        -n, --popsize       Population size
#        -o                  Output file name
#        -s, --step          Step size; how many time steps to skip without user picking
#
#        --generations       Number of generations to run
#            '''

            helpStr = '''
        python evolve -f config/file.yaml

        -f  name            yaml config file name
        -h, --help          Display help menu
            '''
            print helpStr
            sys.exit(0)

    return _args



if __name__ == "__main__":

    try:
        import psyco
        psyco.full()
    except:
        print 'No psyco! Oh well...'

    args = parse()

    from iga.gacommon import gaParams
    if args.has_key('config'):
        filename = args['config']
        if not filename.startswith('config'):
            filename = 'config/' + filename
        gaParams.fileArgs(filename)
    else:
        gaParams.fileArgs('config/floorplan.yml')

    gaParams.setArgs(args)

    if gaParams.getVar('mode') == 'ga':
        gaParams.consoleGA()
    else:
        from gui import gawindow
        import wx

        app = wx.PySimpleApp()

        gaWindow = gawindow.GAWindow()
        gaWindow.SetFocus()

        app.MainLoop()
        app.Destroy()
#-------------------------------------------#
