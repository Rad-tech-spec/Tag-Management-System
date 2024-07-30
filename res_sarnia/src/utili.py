from cryptography.fernet import Fernet
from dateutil import relativedelta
from datetime import datetime
import json, var, os


# Folder switcher
def pathassigner(b):
    path = os.path.realpath(__file__)
    dir = os.path.dirname(path)
    dir = dir.replace("src", b)
    os.chdir(dir)


# For testing only
def showinfo():
    print(var.Token_cr_at)
    print(var.daysdate_)
    print(var.exp_time_)
    

# Encryption & Decryption
def write_key():
    key_ = Fernet.generate_key()
    pathassigner("keys")
    with open("key.key", "wb") as key_file:
        key_file.write(key_)

# Returns key
def load_key():
    pathassigner("keys")
    return open("key.key", "rb").read()

# Updates a newly generated token into file
def write_token(a, key):
    pathassigner("keys")
    f = Fernet(key)
    with open("token.key", "wb") as outfile:
        outfile.write(f.encrypt(a))
    outfile.close()

# Loads the token from file
def load_token(f: Fernet):
    pathassigner("keys")
    return f.decrypt(open("token.key", "rb").read())

# Updated todays date
def datemag():
    if datetime.today() != var.daysdate_:
        updateTodayDate()

# Updating Json value when new token is created
def update_new_token_date(days: int): # Needs Testing
    pathassigner("data")
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
    pathassigner("data")
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
    pathassigner("data")
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


# Write SC response into a file
def write_sc_data(res):
    pathassigner("data")
    if os.path.isfile("data.json"):
        with open("data.json", "w") as outfile:
            outfile.write(json.dumps(res))
        outfile.close()

# Collecting needed prameters from SC
# Task: Compare sensor type
def mag_data_types():
  pathassigner("data")
  with open("data.json", "r") as infile: 
        data_ = json.loads(infile.read())
        for x in data_["locations"]:
            if x["id"] not in var.IG_ID:
                for y in x["data_types"]:
                    if "last_reading" in y and y["description"] != var.IG_PARA:
                        get_tag_name(
                            x["id"], 
                            y["description"], 
                            y["last_reading"][0], 
                            y["last_reading"][1])
    
# Make new function to make the POST call to update tag
# Returns the matching value
def get_tag_name(id, des, date, value):
    #print(des)
    key_list = list(var.SENSORS.keys())
    val_list = list(var.SENSORS.values())  
    with open("tagnames.txt", "r") as insfile:
     lines = insfile.readlines()
     position_ = val_list.index(des)
     key = key_list[position_]
     for a in lines:
        if str(id) in a and key in a:
            # print (a) Testing Only
            break
        continue