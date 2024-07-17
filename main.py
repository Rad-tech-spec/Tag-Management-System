from cryptography.fernet import Fernet
import requests, urllib3, json, os.path, datetime
import utili, logging, var
import logging

urllib3.disable_warnings()
logger = logging.getLogger(__name__)
logging.basicConfig(filename='myapp.log', level=logging.INFO)

# defs.write_key()
key_ = utili.load_key()
#utili.write_token(var.Token_.encode(), key_)
print(utili.load_token(Fernet(key_)))
var.Token_ = utili.load_token(Fernet(key_))

header_ = {"Authorization": "Bearer {}".format(var.Token_.decode())}

def main(): 
    
    logger.info("Executed " + str(datetime.datetime.now()))
    
    if utili.initDate() == 1: logger.info("Dates initialized.")
    if utili.updateTodayDate() == 1: logger.info("Todays date updated.")
    
    logger.info("Token age: " + str(var.exp_time_) + ".")
    utili.showinfo(var.Token_cr_at, var.daysdate_, var.exp_time_)

    # Check Exp date
    if var.exp_time_ <= 5:
        logging.warning("Token will exprire in " + str(var.exp_time_) + " days.")
        try:
            logging.info("Generating a new Token...")
            gettoken_ = json.loads(
                requests.get(var.URL_TOKEN, headers=header_, verify=False).content
            )
            logging.info(gettoken_)
            print(gettoken_) # To be removed
            var.Token_ = str(gettoken_["token"])
            logger.info("New Token: " + str(var.Token_)) # To be removed

            try:
                if gettoken_["response_code"] == 0:
                    var.exp_time_ = 0
                    utili.write_token(var.Token_.encode(), key_)
                    utili.update_new_token_date(gettoken_["days_remaining"])
                    logger.info(
                        "Token updated and replaced. Expires in "
                        + str(var.exp_time_)
                        + " days."
                    )
            except Exception as ein:
                logger.error("Could not write token: %s", repr(ein))

        except Exception as eout:
            logger.error("Failed to update Token: %s", repr(eout))


### Dealing with content
    response_ = requests.get(var.URL_LIST, headers=header_, verify=False)
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
