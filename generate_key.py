import hashlib

def generate_key(frame_data, use_sha256=True):
    if use_sha256:
        return hashlib.sha256(frame_data).hexdigest()  # ✅ returns hex string
    else:
        return hashlib.sha1(frame_data).hexdigest()

