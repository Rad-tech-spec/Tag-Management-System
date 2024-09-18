from cryptography.fernet import Fernet
import urllib3, json, datetime, time
import requests, utili, logging, var, security
import logging

urllib3.disable_warnings()
logger = logging.getLogger(__name__)

utili.pathassigner("log")
logging.basicConfig(filename='myapp.log', level=logging.INFO)

# Write a new key (uncomment to enable)
# defs.write_key()  # Writes a new key

try:
    
    # Load the encryption key from the key file
    key_ = security.load_key()

    # Uncomment the following line to get a new token if expired
    # utili.write_token(var.Token_.encode(), key_) 

    # Load the token using the loaded key
    var.Token_ = security.load_tk(Fernet(key_))

    header_ = {"Authorization": "Bearer {}".format(var.Token_.decode())}
except Exception as e:
    logger.error("Error occurred during key or token operations: %s", repr(e))

def main():
    
    # Step 1 - Housekeeping
    logger.info("Executed on: %s", datetime.datetime.now())
    
    if utili.init_tk_dt() == 1:
        logger.info("Dates initialized.")
    
    if utili.upt_tk_info() == 1:
        logger.info("Token information updated.")
    
    utili.showinfo()

    # Step 2 - Checking Smart Cover Token
    security.sc_tk_m(header_, key_)

    # Step 3 - GET request collecting live data from Smart Cover
    try:
        response = requests.get(var.URL_LIST, headers=header_, verify=False)
        response.raise_for_status()  # Raise an error for bad responses
        utili.write_sc_data(json.loads(response.content))
        logger.info("Sarnia Data collected successfully.")
    except requests.RequestException as e:
        logger.error("Failed to collect Sarnia Data: %s", repr(e))
    except json.JSONDecodeError as e:
        logger.error("Failed to decode JSON response: %s", repr(e))

    # Step 4 - Checking Historian Token 
    # (Implement your historian token check here)

    # Step 5 & 6 - Managing and reforming data and POST request to update tag  
    try:
        utili.m_data_types()
        logger.info("Tag data managed successfully.")
    except Exception as e: 
        logger.error("Failed to manage tag data: %s", repr(e))

    # Program Timer 
    st = time.time()
    elapsed_time = time.time() - st 
    logger.info("Execution time: %.2f seconds.\n", elapsed_time)

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


