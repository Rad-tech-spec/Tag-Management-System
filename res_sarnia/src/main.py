from cryptography.fernet import Fernet
import requests, urllib3, json, datetime, time
import utili, logging, var 
import logging
st = time.time()

urllib3.disable_warnings()
logger = logging.getLogger(__name__)

utili.pathassigner("log")
logging.basicConfig(filename='myapp.log', level=logging.INFO)

# defs.write_key() # Writes a new key
key_ = utili.load_key()
# Uncomment to get the new token if expired
#utili.write_token(var.Token_.encode(), key_) 
print(utili.load_token(Fernet(key_)))
var.Token_ = utili.load_token(Fernet(key_))

header_ = {"Authorization": "Bearer {}".format(var.Token_.decode())}

def main(): 
    
    # House Keeping
    logger.info("Executed " + str(datetime.datetime.now()))
    if utili.initDate() == 1: logger.info("Dates initialized.")
    if utili.updateTodayDate() == 1: logger.info("Todays date updated.") 
    logger.info("Token age: " + str(var.exp_time_) + ".")
    utili.showinfo()

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
                    utili.write_token(var.Token_.encode(), key_)
                    if utili.update_new_token_date(gettoken_["days_remaining"]) == 1:
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


    # GET request collecting live data
    try:
        utili.write_sc_data( json.loads(
            requests.get(var.URL_LIST, headers=header_, verify=False).content
        ))
    except Exception as e:
        logger.error("Failed to collect Sarnia Data: %s", repr(e)) 

    # Managing and reforming data captured
    try:
        utili.mag_data_types()
    except Exception as e: 
        logger.error("Failed to managing tag data: %s", repr(e))



    # Program Timer 
    et = time.time()
    elapsed_time = et - st
    logger.info("Execution time: " +str(elapsed_time)+" seconds.")
   
if __name__ == '__main__':
    main()


# Token generated in 7/17/2024  

# Tasks:
#   1) Program must be able to update both Token and verify or regenerate a token if neccessery.
#   2) Program must be able to create a Jason file from a tap-properties-template JSON file.
#   3) Using the created JSON Tag need to use the TAG URL to create a new Tag (Must check current tags before creation)
#   4) Program must be able to update tag property value with a set time.
#   5) Program must be able to execute on a real time bases.
#   6) Program must deal with the calls once Historian server is down.


# Formats to use for TimeStamp field
#  yyyy-MM-dd'T'HH:mm:ss.SSSZ, 
#  yyyy-MM-dd'T'HH:mm:ss.SSS'Z', 
#  EEE, dd MMM yyyy HH:mm:ss zzz
#  yyyy-MM-dd