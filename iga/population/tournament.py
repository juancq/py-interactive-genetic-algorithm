def tournament(pop, random):
    i1 = random.choice(pop)
    i2 = random.choice(pop)

    if i1.scalefit > i2.scalefit:
        return i1
    else:
        return i2

