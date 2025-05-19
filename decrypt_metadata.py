import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

def decrypt_metadata(encrypted_metadata, encryption_key):
    encrypted_metadata = base64.b64decode(encrypted_metadata)
    iv = encrypted_metadata[:16]
    cipher_key = hashlib.sha256(encryption_key.encode()).digest()
    cipher = AES.new(cipher_key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted_metadata[16:]), AES.block_size)
    return json.loads(decrypted.decode())