from cryptography.fernet import Fernet
from datetime import datetime
import json, var

def showinfo(a, b, c): 
    print(a)
    print(b)
    print(str(c))

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

def updateDate(days: int):
   var.Token_cr_at = datetime.today()
   var.exp_time_ = days

def updateTodayDate():
    var.daysdate = datetime.today()

def initDate():
    with open("info.json", "r") as infile: 
        data = json.loads(infile.read())
        var.Token_cr_at = data["Token_cr_at"]
        var.daysdate = data["daysdate"]
        var.exp_time_ = data["exp_time"]
    infile.close()