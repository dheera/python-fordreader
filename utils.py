def bytes2int(bs, signed = False):
    return int.from_bytes(bs, "big", signed = signed)

