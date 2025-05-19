import numpy as np

def rotate_bits(val, bits):
    val = np.array(val, dtype=np.uint8)
    bits %= 8
    return ((val << bits) | (val >> (8 - bits))) & 0xFF

def rotate_bits_reverse(val, bits):
    val = np.array(val, dtype=np.uint8)
    bits %= 8
    return ((val >> bits) | (val << (8 - bits))) & 0xFF
