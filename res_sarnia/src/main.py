import urllib3, json, datetime, time, requests, utili, var, security, os
from cryptography.fernet import Fernet
from logconfig import logging
from queue import Queue


st = time.time()
urllib3.disable_warnings()

def main():
    logging.info("Exceution Started.")
    try:
        # Write a new key (uncomment to enable)
        # defs.write_key()  # Writes a new key

        # Load the encryption key from the key file
        key_ = security.load_key()

        # Uncomment the following line to get a new token if expired
        #security.write_SC_tk(var.SC_Token_.encode(), key_) 

        # Load the token using the loaded key
        var.SC_Token_= security.load_SC_tk(Fernet(key_))

        # Smart Cover Header
        header_sc = {"Authorization": "Bearer {}".format(var.SC_Token_.decode())}

    except Exception as e:
        logging.error("Error occurred during key or token operations: %s", repr(e))
    
    # Step 1 - Housekeeping
    if utili.init_tk_dt() == 1:
        logging.info("Dates initialized successully.")
    
    if utili.upt_tk_info() == 1:
        logging.info("Token infomation updated successfully.")
    
    utili.showinfo()

    # Step 2 - Checking Smart Cover Token
    security.sc_tk_m(header_sc, key_)

    # Step 3 - GET request collecting live data from Smart Cover
    try:
        response = requests.get(var.URL_LIST, headers=header_sc, verify=False)
        response.raise_for_status()  # Raise an error for bad responses
        utili.write_sc_data(json.loads(response.content))
        logging.info("Sarnia Data collected successfully.")
    except requests.RequestException as e:
        logging.error("Failed to collect Sarnia Data: %s", repr(e))
    except json.JSONDecodeError as e:
        logging.error("Failed to decode JSON response: %s", repr(e))

    # Step 4 - Managing Historian Token 
    try: 
        res = requests.get(var.URL_HS_TOKEN, auth=(var.User_,var.Pass_), verify=False)
        response.raise_for_status()  # Raise an error for bad responses    
        res_data = res.json()
        var.HS_Token_ = res_data["access_token"]

        # Writes and encrypts the new token 
        security.write_HS_tk(str(var.HS_Token_).encode(), key_) 

    except requests.RequestException as e:
        logging.error("Failed to get Historian Token Data: %s", repr(e))
    except json.JSONDecodeError as e:
        logging.error("Failed to decode JSON response: %s", repr(e))
    

    # Step 5 - Managing and reforming data into tags
    try:
        utili.m_data_types()
        logging.info("Tags generated successfully.")
    except Exception as e: 
        logging.error("Failed to manage tag data: %s\n", repr(e))

    # Step 6 - Pushing tag from Queue 
    try:
        q = Queue()
        #Load the token using the loaded key
        var.HS_Token_= security.load_HS_tk(Fernet(key_))

        # Ensure the correct path is set
        utili.pathassigner("tags")  
        
        # Collecting file names 
        utili.collect_files()
        
        for path_ in var.file_names:
            
            # Openning the Tags file
            with open(path_, "r") as file: 
                file_data = json.load(file)

            # Placing tags into queue one by one
            for item in file_data: 
                q.put(item)

            logging.info("------ Files to be pushed: "+str(var.Ct_file)+" ------")
            logging.info("Total Tags in Queue: " + str(q.qsize()))

            # Header 
            header_ = {"Authorization": "Bearer {}".format(var.HS_Token_.decode())}

            # Pushing tags into Historian
            while not q.empty():
                element = q.get()
                res = requests.post(var.URL_CREATE_TAG, json=element, headers=header_ ,verify=False)
                if res.status_code == 200: 
                    print("Successfully pushed Tag")
                    var.Ct += 1
                else:
                    print("Failed to push Tag , Status code: " + str(res.status_code))
                    var.switch = False
            
            logging.info("Total tags Pushed: " + str(var.Ct))
            # Emptying file to be reused with a new set
            if var.switch == True: 
                with open(path_, "w") as file:
                    file.close() 
                    os.remove(path_)
                    print(str(path_) + " Deleted")
                    
    except FileNotFoundError as e: 
        logging.error("File not found: %s", e)
    except json.JSONDecodeError as e:
        logging.error("JSON decoding error: %s", e)
    except KeyError as e:
        logging.error("Key error: %s", e)
    except Exception as e:
        logging.error("Unexpected error in Queue stage: %s", repr(e))


    # Program Timer 
    elapsed_time = time.time() - st 
    logging.info("Execution time: %.2f seconds.\n", elapsed_time)

if __name__ == '__main__':
    main()



  
