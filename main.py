from cryptography.fernet import Fernet
import requests, urllib3, json, os.path
import defs
urllib3.disable_warnings()

TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX3BrIjoiMTAxNTgiLCJpYXQiOjE3MjEwNTQ2NzgsImV4cCI6MTc1MjU5MDY3OH0.ikNVfg42AkA_5NF5OJ-Mz8Kuz2XAwjpyZk5KeSB0Jz0"

# Security
defs.write_key()
key = defs.load_key()
defs.write_token(TOKEN.encode(), key) #!
TOKEN = defs.load_token(Fernet(key))
HEADER= {"Authorization": "Bearer {}".format(TOKEN)}


# URLS
URL_TOKEN = 'https://www.mysmartcover.com/api/auth/refresh.php'
URL_LIST = 'https://www.mysmartcover.com/api/locations/list.php'
print("Token age: " + str(defs.EXP_TIME) + ".")
# Check Exp date
if defs.EXP_TIME <= 5:
    print ("Token will exprire in " + defs.EXP_TIME + " days.")
    try: 
        print("Generating a new Token...")
        gettoken_ = json.loads(requests.get(URL_TOKEN,headers=HEADER, verify=False).content)
        print(gettoken_[""]) # Add response code
    except: 
        print(gettoken_["response_text"])
        
    if (gettoken_): # Check response code if successfull proceed
        defs.write_token(gettoken_["api_token"], key) # Add gettoken encoded()
        defs.EXP_TIME = gettoken_["days_remaining"]
        print("Token updated and replaced. Expires in " + defs.EXP_TIME + " days.")


response_ = requests.get(URL_LIST, headers=HEADER, verify=False)
#print(response.content)

# Write response into a file
if os.path.isfile("data.json") == False: 
    with open("data.json", "w") as outfile:
        outfile.write(str(response_.content))
    outfile.close()

# Filter the file
with open("data.json", "r") as infile: 
    data = infile.read()
    
    with open ("data.json", "w") as outfile: 
        data = data.replace("b'", "")
        data = data.replace("'","")
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

    




