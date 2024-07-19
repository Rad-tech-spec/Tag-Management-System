from cryptography.fernet import Fernet
from dateutil import relativedelta
from datetime import datetime
import json, var

# For testing only
def showinfo():
    print(var.Token_cr_at)
    print(var.daysdate_)
    print(var.exp_time_)
    

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
            outnfile.write(json.dumps(data))
            if( data["Token_cr_at"] == var.Token_cr_at and  
               data["exp_time"] == var.exp_time_):
                outnfile.close()
                intfile.close()
                return 1
    intfile.close()

# Checking and updating daysdate on every run.
def updateTodayDate():
    var.daysdate_ = datetime.today().strftime("%x")
    with open("info.json", "r") as intfile:
        data = json.load(intfile)
        if(data["daysdate"] != var.daysdate_):
            with open("info.json", "w") as outnfile:
                data["daysdate"] = var.daysdate_
                value = calcDate() 
                data["exp_time"] = 365 - value
                outnfile.write(json.dumps(data))
            if(data["daysdate"] == var.daysdate_):
                outnfile.close()
                intfile.close()
                return 1
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


# Calculate date 
def calcDate():
    format = "%m/%d/%y"
    date1 = datetime.strptime(var.Token_cr_at, format)
    date2 = datetime.strptime(var.daysdate_, format)
    difference = relativedelta.relativedelta(date2, date1)
    return difference.days
