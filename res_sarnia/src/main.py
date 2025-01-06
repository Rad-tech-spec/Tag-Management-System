import urllib3, json, time, requests, utili, var, security, os
from cryptography.fernet import Fernet
from logconfig import logging
from queue import Queue
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
0

def main():
    st = time.time()
    urllib3.disable_warnings()
    logging.info("------ Exceution Started. ------")

    try:
        # defs.write_key()  # Writes a new key
        # Load the encryption key from the key file
        key_ = security.load_key()
        #security.write_SC_tk(var.SC_TOKEN.encode(), key_) 
        var.SC_TOKEN = security.load_SC_tk(Fernet(key_))
        header_sc = {"Authorization": "Bearer {}".format(var.SC_TOKEN.decode())}
    except Exception as e:
        logging.error("Error occurred during key or token operations: %s", repr(e))
    
    if utili.init_tk_dt() == 1:
        logging.info("Dates initialized successully.")
    
    if utili.upt_tk_info() == 1:
        logging.info("Token infomation updated successfully.")
    
    utili.showinfo()
    security.sc_tk_m(header_sc, key_)

    try:
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        response = session.get(var.URL_LIST, headers=header_sc, verify=False)
        response.raise_for_status()  
        utili.write_sc_data(json.loads(response.content))
        logging.info("Sarnia Data collected successfully.")
    except requests.RequestException as e:
        logging.error("Failed to collect Sarnia Data: %s", repr(e))
    except json.JSONDecodeError as e:
        logging.error("Failed to decode JSON response: %s", repr(e))

    try: 
        res = requests.get(var.URL_HS_TOKEN, auth=(var.USER,var.PASSWORD), verify=False)
        response.raise_for_status()     
        res_data = res.json()
        var.HS_TOKEN = res_data["access_token"]
        security.write_HS_tk(str(var.HS_TOKEN).encode(), key_) 

    except requests.RequestException as e:
        logging.error("Failed to get Historian Token Data: %s", repr(e))
    except json.JSONDecodeError as e:
        logging.error("Failed to decode JSON response: %s", repr(e))
    

    try:
        utili.m_data_types()
        logging.info("Tags generated successfully.")
    except Exception as e: 
        logging.error("Failed to manage tag data: %s\n", repr(e))

    try:
        q = Queue(106)
        var.HS_TOKEN = security.load_HS_tk(Fernet(key_))

        utili.pathassigner("tags")  
        
        utili.collect_files()
        logging.info("------ Files to be pushed: "+str(var.Ct_file)+" ------")
        for path_ in var.file_names:
            with open(path_, "r") as file: 
                file_data = json.load(file)
            for item in file_data: 
                q.put(item)
            size_ = q.qsize() 
            header_ = {"Authorization": "Bearer {}".format(var.HS_TOKEN.decode())}

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
            var.Ct = 0 
            if var.switch == True: 
                with open(path_, "w") as file:
                    file.close() 
                    os.remove(path_)
                    var.file_names = []
                    logging.info(str(path_) + " Deleted.")
                    
    except FileNotFoundError as e: 
        logging.error("File not found: %s", e)
    except json.JSONDecodeError as e:
        logging.error("JSON decoding error: %s", e)
    except KeyError as e:
        logging.error("Key error: %s", e)
    except Exception as e:
        logging.error("Unexpected error in Queue stage: %s", repr(e))


    elapsed_time = time.time() - st 
    logging.info("Execution time: %.2f seconds.\n", elapsed_time)
    #elapsed_time = 0

if __name__ == '__main__':
    main()