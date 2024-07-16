from cryptography.fernet import Fernet
from datetime import date

exp_time_ = 365


# Encryption & Decryption
def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    return open("key.key", "rb").read()


def write_token(a, key):
    f = Fernet(key)
    with open("token.key", "wb") as outfile:
        outfile.write(f.encrypt(a))
    outfile.close()


def load_token(f: Fernet):
    return f.decrypt(open("token.key", "rb").read())
