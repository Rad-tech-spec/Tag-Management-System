from cryptography.fernet import Fernet
import requests, urllib3, json, os.path, datetime
import utili
import logging

logger = logging.getLogger(__name__)
urllib3.disable_warnings()
logging.basicConfig(filename='myapp.log', level=logging.INFO)

# URLS
URL_TOKEN = "https://www.mysmartcover.com/api/auth/refresh.php"
URL_LIST = "https://www.mysmartcover.com/api/locations/list.php"
Token_ = "" # To be removed

# Security
# defs.write_key()
key_ = utili.load_key()
# defs.write_token(Token_.encode(), key_)
Token_ = utili.load_token(Fernet(key_))
header_ = {"Authorization": "Bearer {}".format(Token_.decode())}

def main(): 
    
    logger.info("Executed " + str(datetime.datetime.now()))
    logger.info("Token age: " + str(utili.exp_time_) + ".")

    # Check Exp date
    if utili.exp_time_ <= 5:
        logging.warning("Token will exprire in " + str(utili.exp_time_) + " days.")
        try:
            logging.info("Generating a new Token...")
            gettoken_ = json.loads(
                requests.get(URL_TOKEN, headers=header_, verify=False).content
            )
            logging.info(gettoken_)
            #print(gettoken_) # To be removed
            Token_ = str(gettoken_["token"])
            logger.info(str(Token_)) # To be removed

            try:
                if gettoken_["response_code"] == 0:
                    utili.exp_time_ = 0
                    utili.write_token(Token_.encode(), key_)
                    utili.exp_time_ = gettoken_["days_remaining"]
                    logger.info(
                        "Token updated and replaced. Expires in "
                        + str(utili.exp_time_)
                        + " days."
                    )
            except Exception as ein:
                logger.error("Could not write token: %s", repr(ein))

        except Exception as eout:
            logger.error("Failed to update Token: %s", repr(eout))


### Dealing with content
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

if __name__ == '__main__':
    main()


# Token generated in 7/16/2024

# Tasks:
#   1) Program must be able to update both Token and verify or regenerate a token if neccessery.
#   2) Program must be able to create a Jason file from a tap-properties-template JSON file.
#   3) Using the created JSON Tag need to use the TAG URL to create a new Tag (Must check current tags before creation)
#   4) Program must be able to update tag property value with a set time.
#   5) Program must be able to execute on a real time bases.
#   6) Program must deal with the calls once Historian server is down.
