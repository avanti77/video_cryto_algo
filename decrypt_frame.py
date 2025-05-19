import numpy as np
from rotate_bits import rotate_bits_reverse

def decrypt_frame(frame, key_bytes):
    key_stream = np.frombuffer(key_bytes, dtype=np.uint8)
    h, w, c = frame.shape
    i = np.arange(h).reshape(-1, 1, 1)
    j = np.arange(w).reshape(1, -1, 1)
    k = np.arange(c).reshape(1, 1, -1)
    idx = (i + j + k) % len(key_stream)

    rotated_keys = rotate_bits_reverse(key_stream[idx], 3)
    xor_result = frame ^ rotated_keys
    decrypted = ((xor_result >> 5) | (xor_result << (8 - 5))) & 0xFF

    return decrypted.astype(np.uint8)
