import itertools

def ViridianMap(minval, maxval, steps=1000):

    colors = [None]*steps
    c1 = (0, 0, 0.5, 1)
    c2 = (0.5, 0, 0.5, 1)
    c3= (0.5, 0.5, 0, 1)

    for i in range(steps//2):
        pos = i/(steps/2-1)
        colors[i] = tuple([v2 * pos + v1 * (1 - pos) for v1, v2 in zip(c1, c2)])

    for i in range(steps//2, steps):
        pos = (i - steps/2)/(steps/2-1)
        colors[i] = tuple([v2 * pos + v1 * (1 - pos) for v1, v2 in zip(c2, c3)])


    def colormap(v):
        v = (v - minval)/(maxval - minval)
        idx = min(steps-1, max(0, int(v*steps)))
        return colors[idx]

    return colormap
