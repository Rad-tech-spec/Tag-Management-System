from cryptography.fernet import Fernet
from datetime import datetime
import requests, json, var, logging, utili

logger = logging.getLogger(__name__)

# Generates a new encryption key and writes it to a file.
def write_key() -> None:
    try:
        # Generate a new Fernet key
        key_ = Fernet.generate_key()
        
        # Set the path for storing the key
        utili.pathassigner("keys")
        
        # Write the key to a file
        with open(var.KEY, "wb") as key_file:
            key_file.write(key_)
        
        logger.info("New encryption key generated and saved to 'key.key'.")

    except Exception as e:
        logger.error("Failed to generate and write the key: %s", repr(e))

# Loads the encryption key from a file.
def load_key() -> bytes:
    try:
        utili.pathassigner("keys")  # Ensure the correct path is set
        
        # Use a context manager to open and read the key file
        with open(var.KEY, "rb") as key_file:
            key = key_file.read()
        
        logger.info("Encryption key loaded successfully.")
        return key

    except FileNotFoundError:
        logger.error("Key file 'SC.key' not found.")
        raise  # Re-raise the exception for handling upstream
    except Exception as e:
        logger.error("Failed to load the key: %s", repr(e))
        raise  # Re-raise the exception for handling upstream

# Encrypts the token using the provided key and writes it to a file.
def write_SC_tk(token: bytes, key: bytes) -> None:
    try:
        utili.pathassigner("keys")  # Ensure the correct path is set
        
        f = Fernet(key)  # Create a Fernet object for encryption
        
        # Use a context manager to open and write to the file
        with open(var.SC_KEY, "wb") as outfile:
            outfile.write(f.encrypt(token))
        
        logger.info("Token encrypted and written to 'token.key'.")

    except Exception as e:
        logger.error("Failed to write the token: %s", repr(e))

# Loads and decrypts the token from the '.key' file.
def load_SC_tk(f: Fernet) -> bytes:
    try:
        utili.pathassigner("keys")  # Ensure the correct path is set

        # Use a context manager to open and read the file
        with open(var.SC_KEY, "rb") as token_file:
            encrypted_token = token_file.read()
        
        # Decrypt the token
        token = f.decrypt(encrypted_token)
        logger.info("Token loaded and decrypted successfully.")
        return token
    
    except FileNotFoundError:
        logger.error("Token file 'token.key' not found.")
        raise  # Re-raise the exception for handling upstream
    except Exception as e:
        logger.error("Failed to load or decrypt the token: %s", repr(e))
        raise  # Re-raise the exception for handling upstream

# Updating info.json values when new token is created
def upt_new_tk_dt(days: int) -> int:
    utili.pathassigner("data")  

    # Update the Token creation date and expiration time
    var.Token_cr_at = datetime.today().strftime("%m/%d/%y")
    var.exp_time_ = days

    try:
        # Read the existing JSON data
        with open(var.TK_INFO_PATH, "r") as infile:
            data = json.load(infile)
        
        # Update the JSON data with new values
        data["Token_cr_at"] = var.Token_cr_at
        data["exp_time"] = var.exp_time_

        # Write the updated JSON data back to the file
        with open(var.TK_INFO_PATH, "w") as outfile:
            json.dump(data, outfile, indent=4)
        
        # Verify if the update was successful
        if data["Token_cr_at"] == var.Token_cr_at and data["exp_time"] == var.exp_time_:
            return 1

    except FileNotFoundError:
        logger.error("File 'info.json' not found.")
    except json.JSONDecodeError:
        logger.error("Error decoding JSON from 'info.json'.")
    except Exception as e:
        logger.error("Unexpected error in upt_new_tk_dt: %s", repr(e))
    
    return 0

# Checking Smart Cover Token Validity
def sc_tk_m(header_, key_):
    try:
        # Check if the token is about to expire
        if var.exp_time_ <= var.DAY:
            logger.warning("Token will expire in %d days.", var.exp_time_)
            
            try:
                # Request a new token
                logger.info("Generating a new token...")
                response = requests.get(var.URL_TOKEN, headers=header_, verify=False)
                response.raise_for_status()  # Raise an error for bad responses
                
                gettoken_ = response.json()
                logger.info("New token response: %s", gettoken_)
            
                
                # Extract the new token
                if gettoken_["response_code"] == 0:
                    var.SC_Token_ = str(gettoken_["token"])
                    write_SC_tk(var.SC_Token_.encode(), key_)
                    
                    if upt_new_tk_dt(gettoken_["days_remaining"]) == 1:
                        logger.info("Token information updated in info.json.")
                    
                    logger.info("Token updated. Expires in %d days.", var.exp_time_)
                else:
                    logger.error("Failed to obtain a valid token. Response code: %d", gettoken_["response_code"])

            except requests.RequestException as req_err:
                logger.error("Failed to update token due to request error: %s", repr(req_err))
            except json.JSONDecodeError as json_err:
                logger.error("Failed to decode JSON response: %s", repr(json_err))
            except KeyError as key_err:
                logger.error("Missing expected key in token response: %s", repr(key_err))
            except Exception as e:
                logger.error("Unexpected error while processing token update: %s", repr(e))

    except Exception as e:
        logger.error("Unexpected error in sc_tk_m: %s", repr(e))


# Encrypts the token using the provided key and writes it to a file.
def write_HS_tk(token: bytes, key: bytes) -> None:
    try:
        utili.pathassigner("keys")  # Ensure the correct path is set
        
        f = Fernet(key)  # Create a Fernet object for encryption
        
        # Use a context manager to open and write to the file
        with open(var.HS_KEY, "wb") as outfile:
            outfile.write(f.encrypt(token))
        
        logger.info("Token encrypted and written to 'HS.key'.")

    except Exception as e:
        logger.error("Failed to write the token: %s", repr(e))


# Loads and decrypts the token from the '.key' file.
def load_HS_tk(f: Fernet) -> bytes:
    try:
        utili.pathassigner("keys")  # Ensure the correct path is set

        # Use a context manager to open and read the file
        with open(var.HS_KEY, "rb") as token_file:
            encrypted_token = token_file.read()
        
        # Decrypt the token
        token = f.decrypt(encrypted_token)
        logger.info("Token loaded and decrypted successfully.")
        return token
    
    except FileNotFoundError:
        logger.error("Token file 'HS.key' not found.")
        raise  # Re-raise the exception for handling upstream
    except Exception as e:
        logger.error("Failed to load or decrypt the token: %s", repr(e))
        raise  # Re-raise the exception for handling upstream