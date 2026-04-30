import hashlib


def md5_encrypt(text):
    return hashlib.md5(text.encode()).hexdigest()
