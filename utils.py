def bytes2int(bs):
    """ converts a big-endian byte array into a single integer """
    v = 0
    p = 0
    for b in reversed(bs):
        v += b * (2 ** p)
        p += 8
    return v

