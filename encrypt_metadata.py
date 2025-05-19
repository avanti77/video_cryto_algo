import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import hashlib

def encrypt_metadata(metadata, encryption_key):
    cipher_key = hashlib.sha256(encryption_key.encode()).digest()
    iv = get_random_bytes(16)
    cipher = AES.new(cipher_key, AES.MODE_CBC, iv)
    json_data = json.dumps(metadata).encode()
    encrypted = cipher.encrypt(pad(json_data, AES.block_size))
    return base64.b64encode(iv + encrypted).decode()