from cryptography.fernet import Fernet
from datetime import datetime
import json, var

# For testing only
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


def datemag():
    if datetime.today() != var.daysdate_:
        updateTodayDate()

# Updating Json value when new token is created
def update_new_token_date(days: int): # Needs Testing
    var.Token_cr_at = datetime.today().strftime("%x")
    var.exp_time_ = days
    with open("info.json", "r") as intfile:
        data = json.loads(intfile.read())
        with open("info.json", "w") as outnfile:
            data["Token_cr_at"] = var.Token_cr_at
            data["exp_time"] = var.exp_time_
            outnfile.write(data)
        outnfile.close()
    intfile.close()

# Checking and updating daysdate on every run.
def updateTodayDate():
    var.daysdate_ = datetime.today().strftime("%x")
    with open("info.json", "r") as intfile:
        data = json.load(intfile)
        if(data["daysdate"] != var.daysdate_):
            with open("info.json", "w") as outnfile:
                data["daysdate"] = var.daysdate_
                outnfile.write(json.dumps(data))
            if(data["daysdate"] == var.daysdate_):
                outnfile.close()
                intfile.close()
                return 1
        outnfile.close()
    intfile.close()
         
# Initializing current updated JSON values every run.
def initDate():
    with open("info.json", "r") as infile:
        data = json.loads(infile.read())
        var.Token_cr_at = data["Token_cr_at"]
        var.daysdate_ = data["daysdate"]
        var.exp_time_ = data["exp_time"]
    infile.close()
    return 1

