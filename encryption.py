import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt(key_hex, plain_text):
    key = bytes.fromhex(key_hex)
    aesgcm = AESGCM(key)
    
    nonce = os.urandom(12)
    
    ciphertext = aesgcm.encrypt(nonce, plain_text.encode(), None)
    return (nonce + ciphertext).hex()

def decrypt(key_hex, ciphertext_hex):
    key = bytes.fromhex(key_hex)
    aesgcm = AESGCM(key)
    
    data = bytes.fromhex(ciphertext_hex)
    
    nonce = data[:12]
    ciphertext = data[12:]
    
    return aesgcm.decrypt(nonce, ciphertext, None).decode()

def generate_key():
    return os.urandom(32).hex()