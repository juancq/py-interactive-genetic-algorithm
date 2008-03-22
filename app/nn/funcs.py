import math

def sigmoid(val):
    if val < -37:
        return 0.0
    if val > 37:
        return 1.0
    return 1.0/(1.0 + math.e ** -val)

sfunc = sigmoid
#sfunc = math.tanh

def dsigmoid(val):
    return val * (1.0 - val)

def dtanh(val):
    return 1.0 - val*val

dfunc = dsigmoid
#dfunc = dtanh
