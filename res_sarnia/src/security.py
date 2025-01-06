from cryptography.fernet import Fernet
from datetime import datetime
from logconfig import logging
import requests, json, var, utili

def write_key() -> None:
    try:
        key_ = Fernet.generate_key()
        utili.pathassigner("keys")
        with open(var.KEY, "wb") as key_file:
            key_file.write(key_)
        logging.info("New encryption key generated and saved to 'key.key'.")
    except Exception as e:
        logging.error("Failed to generate and write the key: %s", repr(e))

def load_key() -> bytes:
    try:
        utili.pathassigner("keys")  
        with open(var.KEY, "rb") as key_file:
            key = key_file.read()
        logging.info("Encryption key loaded successfully.")
        return key
    except FileNotFoundError:
        logging.error("Key file 'SC.key' not found.")
        raise  
    except Exception as e:
        logging.error("Failed to load the key: %s", repr(e))
        raise 

def write_SC_tk(token: bytes, key: bytes) -> None:
    try:
        utili.pathassigner("keys")  
        f = Fernet(key)  
        with open(var.SC_KEY, "wb") as outfile:
            outfile.write(f.encrypt(token))
        logging.info("Token encrypted and written to 'token.key'.")
    except Exception as e:
        logging.error("Failed to write the token: %s", repr(e))

def load_SC_tk(f: Fernet) -> bytes:
    try:
        utili.pathassigner("keys")  
        with open(var.SC_KEY, "rb") as token_file:
            encrypted_token = token_file.read()
        token = f.decrypt(encrypted_token)
        logging.info("Smart Cover Token decrypted successfully.")
        return token
    except FileNotFoundError:
        logging.error("Token file 'token.key' not found.")
        raise  
    except Exception as e:
        logging.error("Failed to load or decrypt the token: %s", repr(e))
        raise  

def upt_new_tk_dt(days: int) -> int:
    utili.pathassigner("data")  

    var.Token_cr_at = datetime.today().strftime("%m/%d/%y")
    var.exp_time_ = days
    try:
        with open(var.TK_INFO_PATH, "r") as infile:
            data = json.load(infile)
        data["Token_cr_at"] = var.Token_cr_at
        data["exp_time"] = var.exp_time_
        with open(var.TK_INFO_PATH, "w") as outfile:
            json.dump(data, outfile, indent=4)
        if data["Token_cr_at"] == var.Token_cr_at and data["exp_time"] == var.exp_time_:
            return 1
    except FileNotFoundError:
        logging.error("File 'info.json' not found.")
    except json.JSONDecodeError:
        logging.error("Error decoding JSON from 'info.json'.")
    except Exception as e:
        logging.error("Unexpected error in upt_new_tk_dt: %s", repr(e))
    
    return 0


def sc_tk_m(header_, key_):
    try:
        if var.exp_time_ <= var.DAY:
            logging.warning("Token will expire in %d days.", var.exp_time_)
            try:
                logging.info("Generating a new token...")
                response = requests.get(var.URL_TOKEN, headers=header_, verify=False)
                response.raise_for_status()  # Raise an error for bad responses
                gettoken_ = response.json()
                logging.info("New token response: %s", gettoken_)
                print(gettoken_)
                if gettoken_["response_code"] == 0:
                    var.SC_TOKEN = str(gettoken_["token"])
                    write_SC_tk(var.SC_TOKEN.encode(), key_)
                    
                    if upt_new_tk_dt(gettoken_["days_remaining"]) == 1:
                        logging.info("Token information updated in info.json.")
                    logging.info("Token updated. Expires in %d days.", var.exp_time_)
                else:
                    logging.error("Failed to obtain a valid token. Response code: %d", gettoken_["response_code"])
            except requests.RequestException as req_err:
                logging.error("Failed to update token due to request error: %s", repr(req_err))
            except json.JSONDecodeError as json_err:
                logging.error("Failed to decode JSON response: %s", repr(json_err))
            except KeyError as key_err:
                logging.error("Missing expected key in token response: %s", repr(key_err))
            except Exception as e:
                logging.error("Unexpected error while processing token update: %s", repr(e))
    except Exception as e:
        logging.error("Unexpected error in sc_tk_m: %s", repr(e))


def write_HS_tk(token: bytes, key: bytes) -> None:
    try:
        utili.pathassigner("keys") 
        f = Fernet(key)  
        with open(var.HS_KEY, "wb") as outfile:
            outfile.write(f.encrypt(token))
        logging.info("Historian token encrypted successfully.")
    except Exception as e:
        logging.error("Failed to write the token: %s", repr(e))


def load_HS_tk(f: Fernet) -> bytes:
    try:
        utili.pathassigner("keys")  
        with open(var.HS_KEY, "rb") as token_file:
            encrypted_token = token_file.read()
        token = f.decrypt(encrypted_token)
        return token
    except FileNotFoundError:
        logging.error("Token file 'HS.key' not found.")
        raise  
    except Exception as e:
        logging.error("Failed to load or decrypt the token: %s", repr(e))
        raise  