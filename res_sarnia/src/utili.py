from dateutil import relativedelta
from datetime import datetime
import json, var, os, logging

logger = logging.getLogger(__name__)

# Folder switcher
def pathassigner(new_dir: str) -> None:
    """Changes the current working directory to a specified folder.

    Args:
        new_dir (str): The name of the directory to switch to, replacing 'src'.
    """
    try:
        path = os.path.realpath(__file__)  # Get the path of the current file
        current_dir = os.path.dirname(path)  # Get the current directory
        target_dir = current_dir.replace("src", new_dir)  # Create target directory path
        
        # Change to the target directory
        os.chdir(target_dir)
        
        #logger.info("Changed directory to: %s", target_dir)

    except FileNotFoundError:
        logger.error("Target directory '%s' not found.", target_dir)
    except Exception as e:
        logger.error("Failed to change directory: %s", repr(e))

pathassigner("log")
logging.basicConfig(filename='myapp.log', level=logging.INFO)

# Logs the current token creation date, days date, and expiration time.
def showinfo() -> None:
    logger.info("Days Date: %s", var.daysdate_)
    logger.info("Smart Cover Token Creation Date: %s", var.Token_cr_at)
    logger.info("Smart Cover Token Expirs In: %d days", var.exp_time_)

# Initializing current updated JSON values every run.
def init_tk_dt() -> int:
    pathassigner("data")  # Ensure this sets the correct path for "info.json"

    try:
        # Read the existing JSON data
        with open(var.TK_INFO_PATH, "r") as infile:
            data = json.load(infile)
        
        # Initialize variables with data from the JSON file
        var.Token_cr_at = data.get("Token_cr_at")
        var.daysdate_ = data.get("daysdate")
        var.exp_time_ = data.get("exp_time")

        return 1  # Indicate success
    except FileNotFoundError:
        logger.error("File 'info.json' not found.")
    except json.JSONDecodeError:
        logger.error("Error decoding JSON from 'info.json'.")
    except KeyError as e:
        logger.error("Missing expected key in JSON data: %s", repr(e))
    except Exception as e:
        logger.error("Unexpected error in init_tk_dt: %s", repr(e))
    
    return 0  # Indicate failure

# Checking and updating daysdate on every run.
def upt_tk_info():
    try:
        pathassigner("data")
        
        # Update the daysdate_ variable with today's date
        var.daysdate_ = datetime.today().strftime("%m/%d/%y")
        
        # Read and update the JSON file
        with open(var.TK_INFO_PATH, "r") as infile:
            data = json.load(infile)

        # Check if daysdate has changed
        if data.get("daysdate") != var.daysdate_:
            # Calculate expiration time
            value = calc_dt()
            data["daysdate"] = var.daysdate_
            data["exp_time"] = 365 - value
            
            # Write updated data back to the file
            with open(var.TK_INFO_PATH, "w") as outfile:
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
        with open(var.DATA_PATH, "w") as outfile:
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
        with open(var.DATA_PATH, "r") as infile:
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
        with open(var.TAG_NAMES, "r") as file:
            lines = file.readlines()

        # Find the relevant line containing both the ID and key
        matching_line = next((line for line in lines if str(sensor_id) in line and key in line), None)
        if not matching_line:
            #logger.error("No matching tag found for ID '%s' and key '%s'.", sensor_id, key)
            return
          
        new_tag = {
            "TagName": matching_line.strip(),
            "Samples": 
            [
                {
                    "TimeStamp": fix_dt_format(date).replace(" ", ""),
                    "Value": value,
                    "Quality": 3
                }
            ]
        }

        # Read the JSON file, update it, and write back
        try:
            with open(var.TAGS_PATH, "r") as file:
                tag_data = json.load(file)
                #print(type(tag_data))  # Check if it's a dict or list
                #print(tag_data)        # Print the current structure
        except FileNotFoundError:
            tag_data = []

        tag_data.append(new_tag)
        
        with open(var.TAGS_PATH, "w") as file:
            json.dump(tag_data, file, indent=4)


    except FileNotFoundError as e:
        logger.error("File not found: %s", e)
    except json.JSONDecodeError as e:
        logger.error("JSON decoding error: %s", e)
    except KeyError as e:
        logger.error("Key error: %s", e)
    except Exception as e:
        logger.error("Unexpected error in get_tag_name: %s", repr(e))

# Formatting date base on valid format.
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
    






# def posting_tag():
#     print("Making a POST request.")
#     api_url = "https://snwpcc-hist1:8443/historian-rest-api/v1/datapoints/create"
#     response = requests.post(api_url, json = )
#     response.json()
