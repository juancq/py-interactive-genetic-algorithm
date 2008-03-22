import app

#-------------------------------------------#
class MaskApplication(app.Application):
    def __init__(self, params, random):
        app.Application.__init__(self, params, random)

        defaults = {}
        var_list = self.params['vars']
        for name,value in var_list.iteritems():
            if value.has_key('default'):
                defaults[name] = value['default']
            else:
                defaults[name] = None
        self.defaults = defaults

#-------------------------------------------#
    def createPop(self, popsize):        
        '''
        Create a population of individuals with random
        masked variables.
        '''
        randint = self.random.randint
        defaults = self.defaults
        pop = []
        for i in xrange(popsize):
            chrom = {}
            for name, value in self.attr.iteritems():
                if value['mask']:
                    chrom[name] = None
                    value['init'] = False
                else:
                    chrom[name] = [randint(0, 1) for i in xrange(value['bits'])]
                    value['init'] = True

            ind = app.Individual(self.random, None, chrom)
            ind.defaults = defaults.copy()

            pop.append(ind)
        return pop


#-------------------------------------------#
    def encodeVar(self, attr, var_value):

        top = int(attr['bits'])
        chrom = [0] * top
        scaled_value = (var_value - attr['min']) / (attr['max'] - attr['min'])
        n = int(scaled_value * (2.**attr['bits'] - 1))
        i = top-1
        while n > 0:
            chrom[i] = n % 2
            n /= 2
            i -= 1
        return chrom

#-------------------------------------------#
    def decodeVar(self, attr, chrom):

        if chrom:
            top = int(attr['bits'])
            temp = 0.
            for i in xrange(0, top):
                if chrom[i]:
                    temp += 2**(top-i-1)

            temp = temp / (2.**attr['bits'] - 1)
            temp =  temp * (attr['max']-attr['min']) + attr['min']
            return temp
        else:
            return None


#-------------------------------------------#
    def decode(self, ind):

        chrom = ind.genome
        defaults = ind.defaults
        data = {}
        # for each attribute in chromosome
        # if it's not masked, decode it
        # else return default value
        for name, value in chrom.iteritems():
            if value:
                data[name] = self.decodeVar(self.attr[name], value)
            else:
                data[name] = defaults[name]

        return data

#-------------------------------------------#
    def updateMask(self, pop, mask):
        '''
        Update chromosome of each individual with new mask.
        If value is being masked, then decode current value
        '''
        attr = self.attr
        randint = self.random.randint

        for var in mask:
            attr[var]['mask'] = not attr[var]['mask']

            # if masking a value
            if attr[var]['mask']:
                for ind in pop:
                    ind.defaults[var] = self.decodeVar(attr[var], ind.genome[var])
                    ind.genome[var] = None
            else:
            # if removing the mask of an attribute
            # i.e. expanding search space
                # if not initialized before, then 
                # create random chrom for attribute
                if not attr[var]['init']:
                    for ind in pop:
                        ind.genome[var] = [randint(0, 1) for i in xrange(attr[var]['bits'])]
                    attr[var]['init'] = True

                # if removing the mask, and value was init before
                # then just create a chrom out of current default value
                else:
                    for ind in pop:
                        ind.genome[var] = self.encodeVar(attr[var], ind.defaults[var])

#-------------------------------------------#
