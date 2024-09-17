from cryptography.fernet import Fernet
from dateutil import relativedelta
from datetime import datetime
import requests, json, var, os, logging
logger = logging.getLogger(__name__)

# Folder switcher
def pathassigner(b):
    path = os.path.realpath(__file__)
    dir = os.path.dirname(path)
    dir = dir.replace("src", b)
    os.chdir(dir)

pathassigner("log")
logging.basicConfig(filename='myapp.log', level=logging.INFO)

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
def write_tk(a, key):
    pathassigner("keys")
    f = Fernet(key)
    with open("token.key", "wb") as outfile:
        outfile.write(f.encrypt(a))
    outfile.close()

# Loads the token from file
def load_tk(f: Fernet):
    pathassigner("keys")
    return f.decrypt(open("token.key", "rb").read())

# Updating info.json values when new token is created
def upt_new_tk_dt(days: int): # Needs Testing
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

# Checking Smart Cover Token Validity
def sc_tk_m(header_, key_):
    # Check Exp date
    if var.exp_time_ <= var.DAY:
        logging.warning("Token will expire in " + str(var.exp_time_) + " days.")
        try:
            logging.info("Generating a new Token...")
            gettoken_ = json.loads(
                requests.get(var.URL_TOKEN, headers=header_, verify=False).content
            )
            logging.info(gettoken_)
            var.Token_ = str(gettoken_["token"])
            logger.info("New Token: " + str(var.Token_)) # REMOVE
            try:
                if gettoken_["response_code"] == 0:
                    write_tk(var.Token_.encode(), key_)
                    if upt_new_tk_dt(gettoken_["days_remaining"]) == 1:
                        logger.info("Token information updated in info.json.")
                    logger.info(
                        "Token updated. Expires in "
                        + str(var.exp_time_)
                        + " days."
                    )
            except Exception as ein:
                logger.error("Could not write token: %s", repr(ein))

        except Exception as eout:
            logger.error("Failed to update Token: %s", repr(eout))


# Checking and updating daysdate on every run.
def upt_tk_info():
    pathassigner("data")
    var.daysdate_ = datetime.today().strftime("%x")
    with open("info.json", "r") as intfile:
        data = json.load(intfile)
        if(data["daysdate"] != var.daysdate_):
            with open("info.json", "w") as outnfile:
                data["daysdate"] = var.daysdate_
                value = calc_dt() 
                data["exp_time"] = 365 - value 
                outnfile.write(json.dumps(data))
            if(data["daysdate"] == var.daysdate_):
                outnfile.close()
                intfile.close()
                return 1
    intfile.close()

# Initializing current updated JSON values every run.
def init_tk_dt():
    pathassigner("data")
    with open("info.json", "r") as infile:
        data = json.loads(infile.read())
        var.Token_cr_at = data["Token_cr_at"]
        var.daysdate_ = data["daysdate"]
        var.exp_time_ = data["exp_time"]
    infile.close()
    return 1

# Calculate date
def calc_dt():
    format = "%m/%d/%y"
    date1 = datetime.strptime(var.Token_cr_at, format).date()
    date2 = datetime.strptime(var.daysdate_, format).date()
    difference = relativedelta.relativedelta(date2, date1)
    if difference.months > 0:
        return difference.days + (difference.months * 30) # Calculate per each month
    else:
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
def m_data_types():
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
    

# Matches tag from tagname.txt file based on id and key.
def get_tag_name(id, des, date, value):
    try:
        key_list_ = list(var.SENSORS.keys())
        val_list_ = list(var.SENSORS.values())  
        with open("tagnames.txt", "r") as insfile:
            lines_ = insfile.readlines()
            position_ = val_list_.index(des)
            key_ = key_list_[position_]
            for a in lines_:
                if str(id) in a and key_ in a:
                    with open("tag.json", "r") as infile: 
                        inf = json.loads(infile.read())
                        with open("tag.json", "w") as outfile:
                            inf["TagName"] = str(a).replace("\n", "")
                            #print(n_date)
                            for i in inf["Samples"]:
                                i["TimeStamp"] = str(fix_dt_format(date)).replace(" ", "") 
                                i["Value"] = value
                                break
                            outfile.write(json.dumps(inf))
                    break
                continue
    except Exception as e: 
        logger.error("Function get_tag_name %s", repr(e))

# Formating date base on valid format.
# yyyy-MM-dd'T'HH:mm:ss.SSSZ
def fix_dt_format(date):
    x = datetime.now()
    N = 10
    if date != None: 
        return date[ : N] + "T" + date[N : ] + ":00.000Z"
    else: 
        return x.strftime("%Y")+"-"+x.strftime("%m")+"-"+x.strftime("%d")+"T"+x.strftime("%X")+".000Z"




     