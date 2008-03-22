from pickle import dumps
from iga.gacommon import gaParams

class PeerHandler(object):
    def __init__(self):
        pass

    def getGenomes(self, genomes_requested = 9):
        data = gaParams.getNGenomes(genomes_requested)
        if data:
            return dumps(data)
        else:
            return False

    def test(self):
        return True
