import urllib3, json, time, requests, utili, var, security, os
from cryptography.fernet import Fernet
from logconfig import logging
from queue import Queue
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
#from apscheduler.schedulers.blocking import BlockingScheduler

st = time.time()
urllib3.disable_warnings()

def main():
    logging.info("------ Exceution Started. ------")
    try:
        # Write a new key (uncomment to enable)
        # defs.write_key()  # Writes a new key

        # Load the encryption key from the key file
        key_ = security.load_key()

        # Uncomment the following line to get a new token if expired
        #security.write_SC_tk(var.SC_TOKEN.encode(), key_) 

        # Load the token using the loaded key
        var.SC_TOKEN = security.load_SC_tk(Fernet(key_))

        # Smart Cover Header
        header_sc = {"Authorization": "Bearer {}".format(var.SC_TOKEN.decode())}

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
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        response = session.get(var.URL_LIST, headers=header_sc, verify=False)
        response.raise_for_status()  # Raise an error for bad responses
        utili.write_sc_data(json.loads(response.content))
        logging.info("Sarnia Data collected successfully.")
    except requests.RequestException as e:
        logging.error("Failed to collect Sarnia Data: %s", repr(e))
    except json.JSONDecodeError as e:
        logging.error("Failed to decode JSON response: %s", repr(e))

    # Step 4 - Managing Historian Token 
    try: 
        res = requests.get(var.URL_HS_TOKEN, auth=(var.USER,var.PASSWORD), verify=False)
        response.raise_for_status()  # Raise an error for bad responses    
        res_data = res.json()
        var.HS_TOKEN = res_data["access_token"]

        # Writes and encrypts the new token 
        security.write_HS_tk(str(var.HS_TOKEN).encode(), key_) 

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
        q = Queue(87)
        #Load the token using the loaded key
        var.HS_TOKEN = security.load_HS_tk(Fernet(key_))

        # Ensure the correct path is set
        utili.pathassigner("tags")  
        
        # Collecting file names 
        utili.collect_files()
        logging.info("------ Files to be pushed: "+str(var.Ct_file)+" ------")
        for path_ in var.file_names:
            
            # Openning the Tags file
            with open(path_, "r") as file: 
                file_data = json.load(file)

            # Placing tags into queue one by one
            for item in file_data: 
                q.put(item)
            size_ = q.qsize() 
            #logging.info("Total Tags in Queue: " + str(q.qsize()))

            # Header 
            header_ = {"Authorization": "Bearer {}".format(var.HS_TOKEN.decode())}

            # Pushing tags into Historian
            session = requests.Session()
            while not q.empty():
                try:
                    element = q.get()
                    res = session.post(var.URL_CREATE_TAG, json=element, headers=header_, verify=False)
                    if res.status_code == 200:
                        var.Ct += 1
                    else:
                        var.switch = False

                except res.status_code != 200: 
                    logging.error("Failed to push Tag, Status code: " + str(res.status_code))
                except Exception as e:
                    logging.error("An error occurred: " + str(e))
               
            logging.info("Total Tags in Queue: " + str(size_) + " ~ Total tags Pushed: " + str(var.Ct))
            var.Ct = 0 # Resetting count
            # Emptying file to be reused with a new set
            if var.switch == True: 
                with open(path_, "w") as file:
                    file.close() 
                    os.remove(path_)
                    logging.info(str(path_) + " Deleted.")
                    
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
    #elapsed_time = 0

if __name__ == '__main__':
    main()


# scheduler = BlockingScheduler()
# scheduler.add_job(main, 'interval', seconds=300)
# scheduler.start()
  
