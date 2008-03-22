# Creates a dictionary of the form var_i for ith copy of variable
    # clone attributes for each image
    new_attr = {}
    for i in xrange(num_img):
        for name,value in self.attr.iteritems():
            new_attr[name + ('_%d' % i)] = value

    self.attr = new_attr
    self.geneLen *= num_img


# Maybe return list of dictionaries instead, where each dictionary is for each "individual"
# Allow only parts of the chromosome to be cloned
