from cryptography.fernet import Fernet
import requests, urllib3, json, os.path
import defs
import logging

urllib3.disable_warnings()

# URLS
URL_TOKEN = "https://www.mysmartcover.com/api/auth/refresh.php"
URL_LIST = "https://www.mysmartcover.com/api/locations/list.php"
Token_ = ""

# Security
#defs.write_key()
key_ = defs.load_key()
#defs.write_token(Token_.encode(), key_) 
Token_ = defs.load_token(Fernet(key_))
header_ = {"Authorization": "Bearer {}".format(Token_.decode())}


print("Token age: " + str(defs.exp_time_) + ".")

# Check Exp date
if defs.exp_time_ <= 5:
    print("Token will exprire in " + str(defs.exp_time_) + " days.")
    try:
        print("Generating a new Token...")
        gettoken_ = json.loads(
            requests.get(URL_TOKEN, headers=header_, verify=False).content
        )
        print(gettoken_)
        Token_ = str(gettoken_["token"])
        print(str(Token_))

        try: 
            if gettoken_["response_code"] == 0:
                defs.exp_time_ = 0
                defs.write_token(Token_.encode(), key_)
                defs.exp_time_ = gettoken_["days_remaining"]
                print("Token updated and replaced. Expires in " + str(defs.exp_time_) + " days.")
        except Exception as ein:
            logging.error('Could not write token: %s', repr(ein))

    except Exception as eout:
        logging.error('Failed to update Token: %s', repr(eout))


response_ = requests.get(URL_LIST, headers=header_, verify=False)
# print(response.content)

# Write response into a file
if os.path.isfile("data.json") == False:
    with open("data.json", "w") as outfile:
        outfile.write(str(response_.content))
    outfile.close()

# Filter the file
with open("data.json", "r") as infile:
    data = infile.read()

    with open("data.json", "w") as outfile:
        data = data.replace("b'", "")
        data = data.replace("'", "")
        outfile.write(data)
infile.close()
outfile.close()


# Tasks:
#   1) Program must be able to update both Token and verify or regenerate a token if neccessery.
#   2) Program must be able to create a Jason file from a tap-properties-template JSON file.
#   3) Using the created JSON Tag need to use the TAG URL to create a new Tag (Must check current tags before creation)
#   4) Program must be able to update tag property value with a set time.
#   5) Program must be able to execute on a real time bases.
#   6) Program must deal with the calls once Historian server is down.
