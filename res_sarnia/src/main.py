from cryptography.fernet import Fernet
import urllib3, json, datetime, time
import requests, utili, logging, var 
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
print(utili.load_tk(Fernet(key_)))
var.Token_ = utili.load_tk(Fernet(key_))

header_ = {"Authorization": "Bearer {}".format(var.Token_.decode())}

def main(): 
    
    # Step 1 - House Keeping
    logger.info("Executed " + str(datetime.datetime.now()))
    if utili.init_tk_dt() == 1: logger.info("Dates initialized.")
    if utili.upt_tk_info() == 1: logger.info("Token infomation updated.") 
    logger.info("Token age: " + str(var.exp_time_) + ".")
    utili.showinfo()
    
    # Step 2 - Checking Smart Cover Token
    utili.sc_tk_m(header_, key_)
    
    # Step 3 - GET request collecting live data from Smart Cover
    try:
        utili.write_sc_data( json.loads(
            requests.get(var.URL_LIST, headers=header_, verify=False).content
        ))
    except Exception as e:
        logger.error("Failed to collect Sarnia Data: %s", repr(e)) 

    # Step 4 - Checking Historian Token 



    # Step 5 & 6 - Managing and reforming data and POST requst to update tag  
    try:
        utili.m_data_types()
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
#   7) Jason Files Should not lose content when there is an error.


