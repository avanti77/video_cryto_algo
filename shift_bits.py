import numpy as np

def shift_bits(val, shift):
    val = np.array(val, dtype=np.uint8)
    if shift == 0:
        return val
    return ((val << shift) | (val >> (8 - shift))) & 0xFF

def unshift_bits(val, shift):
    val = np.array(val, dtype=np.uint8)
    if shift == 0:
        return val
    return ((val >> shift) | (val << (8 - shift))) & 0xFF
