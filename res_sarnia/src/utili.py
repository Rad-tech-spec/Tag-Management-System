from cryptography.fernet import Fernet
from dateutil import relativedelta
from datetime import datetime
import requests, json, var, os, logging
logger = logging.getLogger(__name__)

# Folder switcher
def pathassigner(b):
    path = os.path.realpath(__file__)
    dir = os.path.dirname(path)
    dir = dir.replace("src", b)
    os.chdir(dir)

pathassigner("log")
logging.basicConfig(filename='myapp.log', level=logging.INFO)

# For testing only
def showinfo():
    print(var.Token_cr_at)
    print(var.daysdate_)
    print(var.exp_time_)
    
# Encryption & Decryption
def write_key():
    key_ = Fernet.generate_key()
    pathassigner("keys")
    with open("key.key", "wb") as key_file:
        key_file.write(key_)

# Returns key
def load_key():
    pathassigner("keys")
    return open("key.key", "rb").read()

# Updates a newly generated token into file
def write_tk(a, key):
    pathassigner("keys")
    f = Fernet(key)
    with open("token.key", "wb") as outfile:
        outfile.write(f.encrypt(a))
    outfile.close()

# Loads the token from file
def load_tk(f: Fernet):
    pathassigner("keys")
    return f.decrypt(open("token.key", "rb").read())

# Updating info.json values when new token is created
def upt_new_tk_dt(days: int) -> int:
    pathassigner("data")  

    # Update the Token creation date and expiration time
    var.Token_cr_at = datetime.today().strftime("%m/%d/%y")
    var.exp_time_ = days

    try:
        # Read the existing JSON data
        with open("info.json", "r") as infile:
            data = json.load(infile)
        
        # Update the JSON data with new values
        data["Token_cr_at"] = var.Token_cr_at
        data["exp_time"] = var.exp_time_

        # Write the updated JSON data back to the file
        with open("info.json", "w") as outfile:
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
                if gettoken_.get("response_code") == 0:
                    var.Token_ = str(gettoken_.get("token"))
                    write_tk(var.Token_.encode(), key_)
                    
                    if upt_new_tk_dt(gettoken_.get("days_remaining")) == 1:
                        logger.info("Token information updated in info.json.")
                    
                    logger.info("Token updated. Expires in %d days.", var.exp_time_)
                else:
                    logger.error("Failed to obtain a valid token. Response code: %d", gettoken_.get("response_code"))

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

# Checking and updating daysdate on every run.
def upt_tk_info():
    try:
        pathassigner("data")
        
        # Update the daysdate_ variable with today's date
        var.daysdate_ = datetime.today().strftime("%m/%d/%y")
        
        # Read and update the JSON file
        with open("info.json", "r") as infile:
            data = json.load(infile)

        # Check if daysdate has changed
        if data.get("daysdate") != var.daysdate_:
            # Calculate expiration time
            value = calc_dt()
            data["daysdate"] = var.daysdate_
            data["exp_time"] = 365 - value
            
            # Write updated data back to the file
            with open("info.json", "w") as outfile:
                json.dump(data, outfile, indent=4)
            
            return 1
        
        return 0  # Return 0 if no update was needed

    except FileNotFoundError:
        logger.error("File 'info.json' not found.")
    except json.JSONDecodeError:
        logger.error("Error decoding JSON from 'info.json'.")
    except Exception as e:
        logger.error("Unexpected error in upt_tk_info: %s", repr(e))

    return 0

# Initializing current updated JSON values every run.
def init_tk_dt():
    pathassigner("data")
    with open("info.json", "r") as infile:
        data = json.loads(infile.read())
        var.Token_cr_at = data["Token_cr_at"]
        var.daysdate_ = data["daysdate"]
        var.exp_time_ = data["exp_time"]
    infile.close()
    return 1

# Calculate date
def calc_dt():
    try:
        date_format = "%m/%d/%y"
        
        # Convert string dates to datetime.date objects
        start_date = datetime.strptime(var.Token_cr_at, date_format).date()
        end_date = datetime.strptime(var.daysdate_, date_format).date()
        
        # Calculate the difference between dates
        difference = relativedelta.relativedelta(end_date, start_date)
        
        # Calculate total difference in days, considering months
        total_days = difference.days + (difference.months * 30)  # Approximate month length
        
        return total_days

    except ValueError as e:
        logger.error("Date parsing error: %s", e)
        return None
    except Exception as e:
        logger.error("Unexpected error in calc_dt: %s", repr(e))
        return None

# Write SC response into a file
def write_sc_data(response):
    try:
        pathassigner("data")  

        # Write JSON response to file
        with open("data.json", "w") as outfile:
            json.dump(response, outfile, indent=4)

    except IOError as e:
        logger.error("Error writing to file 'data.json': %s", e)
    except Exception as e:
        logger.error("Unexpected error in write_sc_data: %s", repr(e))

# Collecting needed prameters from SC
# Task: Compare sensor type
def m_data_types():
    try:
        pathassigner("data")  

        # Read and parse the JSON data
        with open("data.json", "r") as infile:
            data = json.load(infile)
        
        # Process each location in the data
        for location in data.get("locations", []):
            location_id = location.get("id")
            
            # Skip locations with IDs in var.IG_ID
            if location_id in var.IG_ID:
                continue
            
            # Process each data type in the location
            for data_type in location.get("data_types", []):
                description = data_type.get("description")
                last_reading = data_type.get("last_reading")
                
                # Ensure required fields are present
                if last_reading and description and description != var.IG_PARA:
                    # Call the function to get the tag name
                    get_tag_name(
                        location_id, 
                        description, 
                        last_reading[0], 
                        last_reading[1]
                    )

    except FileNotFoundError:
        logger.error("File 'data.json' not found.")
    except json.JSONDecodeError:
        logger.error("Error decoding JSON from 'data.json'.")
    except KeyError as e:
        logger.error("Missing expected key in JSON data: %s", e)
    except Exception as e:
        logger.error("Unexpected error in m_data_types: %s", repr(e))   
    

def get_tag_name(sensor_id, description, date, value):
    try:
        # Retrieve sensor keys and values
        sensor_keys = list(var.SENSORS.keys())
        sensor_values = list(var.SENSORS.values())
        
        # Find the corresponding key for the description
        if description not in sensor_values:
            logger.error("Description '%s' not found in sensor values.", description)
            return
        
        position = sensor_values.index(description)
        key = sensor_keys[position]

        # Read the tag names from file
        with open("tagnames.txt", "r") as file:
            lines = file.readlines()

        # Find the relevant line containing both the ID and key
        matching_line = next((line for line in lines if str(sensor_id) in line and key in line), None)
        if not matching_line:
            logger.error("No matching tag found for ID '%s' and key '%s'.", sensor_id, key)
            return

        # Read the JSON file, update it, and write back
        with open("tag.json", "r") as file:
            tag_data = json.load(file)

        tag_data["TagName"] = matching_line.strip()
        for sample in tag_data["Samples"]:
            sample["TimeStamp"] = fix_dt_format(date).replace(" ", "")
            sample["Value"] = value
            break

        with open("tag.json", "w") as file:
            json.dump(tag_data, file, indent=4)

        posting_tag() # Step 6 making a POST request.

    except FileNotFoundError as e:
        logger.error("File not found: %s", e)
    except json.JSONDecodeError as e:
        logger.error("JSON decoding error: %s", e)
    except KeyError as e:
        logger.error("Key error: %s", e)
    except Exception as e:
        logger.error("Unexpected error in get_tag_name: %s", repr(e))

# Formating date base on valid format.
def fix_dt_format(date):
    if date:
        try:
            # Parameter date format 'YYYY-MM-DD HH:MM:SS'
            # Adjust slicing if 'date' format is different
            return date[:10] + "T" + date[11:] + ":00.000Z"
        except IndexError:
            # Handle cases where 'date' might not be in the expected format
            return None
    else:
        # Generate current datetime in ISO format and adjust to include milliseconds and timezone
        now = datetime.now()
        return now.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    
def posting_tag():
    print("Making a POST request.")
#     api_url = ""
#     response = requests.post(api_url, json = )
#     response.json()
