from cryptography.fernet import Fernet
import urllib3, json, datetime, time
import requests, utili, logging, var, security
from queue import Queue

st = time.time()

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
    # utili.write_token(var.SC_Token_.encode(), key_) 

    # Uncomment the following line to get a new token if expired
    # utili.write_token(var.HS_Token_.encode(), key_) 

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



    # Step 5 - Managing and reforming data into tags
    try:
        utili.m_data_types()
        logger.info("Tag data managed successfully.")
    except Exception as e: 
        logger.error("Failed to manage tag data: %s\n", repr(e))

    # 6 - Placing stored tags into queue then PUSH (TB TESTED)
    # try:

    #     # Openning the Tags file
    #     with open(var.TAGS_PATH, "r") as file: 
    #         file_data = json.load(file)

    #     q = Queue()

    #     # Placing tags into queue one by one.
    #     for item in file_data: 
    #         q.put(item)

    #     # Pushing tags into Historian
    #     while not q.empty():
    #         element = q.get()
    #         res = requests.post(var.URL_CREATE_TAG, json=element)
    #         if res.status_code == 200: 
    #             print(f"Successfully pushed: {element}")
    #         else:
    #             print(f"Failed to push: {element},
    #                 Status code: {res.status_code}")
                
    #     # Emptying file to be reused with a new set
    #     with open(var.TAGS_PATH, "w") as file: 
    #         json.dump([], file)
    #         print("JSON file has been emptied")

    # except FileNotFoundError as e: 
    #     logger.error("File not found: %s", e)
    # except json.JSONDecodeError as e:
    #     logger.error("JSON decoding error: %s", e)
    # except KeyError as e:
    #     logger.error("Key error: %s", e)
    # except Exception as e:
    #     logger.error("Unexpected error in Queue stage: %s", repr(e))


    # Program Timer 
    elapsed_time = time.time() - st 
    logger.info("Execution time: %.2f seconds.\n", elapsed_time)

if __name__ == '__main__':
    main()
  
