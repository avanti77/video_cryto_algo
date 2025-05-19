import numpy as np
from rotate_bits import rotate_bits
from shift_bits import shift_bits

def encrypt_frame(frame, key_bytes):
    key_stream = np.frombuffer(key_bytes, dtype=np.uint8)
    h, w, c = frame.shape
    i, j, k = np.indices((h, w, c))
    idx = (i + j + k) % len(key_stream)

    rotated_key = rotate_bits(key_stream[idx], 3)
    shifted_pixel = shift_bits(frame, 5)

    encrypted_frame = shifted_pixel ^ rotated_key
    return encrypted_frame.astype(np.uint8)
