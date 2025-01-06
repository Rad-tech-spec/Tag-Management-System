from dateutil import relativedelta
from datetime import datetime, timedelta
import json, var, os, logging

def pathassigner(new_dir: str) -> None:
    try:
        path = os.path.realpath(__file__)  
        current_dir = os.path.dirname(path)  
        target_dir = current_dir.replace("src", new_dir)  
        
        os.chdir(target_dir)
        

    except FileNotFoundError:
        logging.error("Target directory '%s' not found.", target_dir)
    except Exception as e:
        logging.error("Failed to change directory: %s", repr(e))


def showinfo() -> None:
    logging.info("Smart Cover Token Creation Date: %s", var.Token_cr_at)
    logging.info("Smart Cover Token Expirs In: %d days", var.exp_time_)

def init_tk_dt() -> int:
    pathassigner("data")  #
    try:
        with open(var.TK_INFO_PATH, "r") as infile:
            data = json.load(infile)
        
        var.Token_cr_at = data["Token_cr_at"]
        var.daysdate_ = data["daysdate"]
        var.exp_time_ = data["exp_time"]
        crt_tag_file()
        return 1  # Indicate success
    except FileNotFoundError:
        logging.error("File 'info.json' not found.")
    except json.JSONDecodeError:
        logging.error("Error decoding JSON from 'info.json'.")
    except KeyError as e:
        logging.error("Missing expected key in JSON data: %s", repr(e))
    except Exception as e:
        logging.error("Unexpected error in init_tk_dt: %s", repr(e))
    
    return 0  # Indicate failure

def upt_tk_info():
    try:
        pathassigner("data")
        var.daysdate_ = datetime.today().strftime("%m/%d/%y")
        with open(var.TK_INFO_PATH, "r") as infile:
            data = json.load(infile)
        if data["daysdate"] != var.daysdate_:
            value = calc_dt()
            data["daysdate"] = var.daysdate_
            data["exp_time"] = 365 - value
            with open(var.TK_INFO_PATH, "w") as outfile:
                json.dump(data, outfile, indent=4)
            return 1
        return 0 

    except FileNotFoundError:
        logging.error("File 'info.json' not found.")
    except json.JSONDecodeError:
        logging.error("Error decoding JSON from 'info.json'.")
    except Exception as e:
        logging.error("Unexpected error in upt_tk_info: %s", repr(e))

    return 0

def calc_dt():
    try:
        date_format = "%m/%d/%y"
        start_date = datetime.strptime(var.Token_cr_at, date_format).date()
        end_date = datetime.strptime(var.daysdate_, date_format).date()
        difference = relativedelta.relativedelta(end_date, start_date)
        total_days = difference.days + (difference.months * 30)  
        
        return total_days

    except ValueError as e:
        logging.error("Date parsing error: %s", e)
        return None
    except Exception as e:
        logging.error("Unexpected error in calc_dt: %s", repr(e))
        return None

def write_sc_data(response):
    try:
        pathassigner("data")  

        with open(var.DATA_PATH, "w") as outfile:
            json.dump(response, outfile, indent=4)

    except IOError as e:
        logging.error("Error writing to file 'data.json': %s", e)
    except Exception as e:
        logging.error("Unexpected error in write_sc_data: %s", repr(e))

def m_data_types():
    try:
        pathassigner("data")  
        with open(var.DATA_PATH, "r") as infile:
            data = json.load(infile)       
        for location in data["locations"]:
            location_id = location["id"]           
            if location_id in var.IG_ID:
                continue
            for data_type in location["data_types"]:
                if "last_reading" in data_type:
                    description = data_type["description"]
                    last_reading = data_type["last_reading"]
                else: 
                    continue
                if last_reading and description:
                    get_tag_name(
                        location_id, 
                        description,  
                        last_reading[1]
                    )

    except FileNotFoundError:
        logging.error("File 'data.json' not found.")
    except json.JSONDecodeError:
        logging.error("Error decoding JSON from 'data.json'.")
    except KeyError as e:
        logging.error("Missing expected key in JSON data: %s %s", e, location_id)
    except Exception as e:
        logging.error("Unexpected error in m_data_types: %s", repr(e))   
    

def get_tag_name(sensor_id, description, value):
    try:
        sensor_keys = list(var.SENSORS.keys())
        sensor_values = list(var.SENSORS.values())
        if description not in sensor_values:
            logging.error("Description '%s' not found in sensor values.", description)
            return
        
        position = sensor_values.index(description)
        key = sensor_keys[position]

        if key == "LEVEL_2":
            key = "LEVEL"

        pathassigner("data") 
        with open(var.TAG_NAMES, "r") as file:
            lines = file.readlines()
        matching_line = next((line for line in lines if str(sensor_id) in line and key in line), None)
        if not matching_line:
            logging.error("No matching tag found for ID '%s' and key '%s'.", sensor_id, key)
            return
        new_tag = {
            "TagName": matching_line.strip(),
            "samples": 
            [
                {
                    "TimeStamp": fix_dt_format().replace(" ", ""),
                    "Value": str(value),
                    "Quality": 3
                }
            ]
        }

        try:
            pathassigner("tags") 
            with open(var.TAGS_PATH, "r") as file:
                tag_data = json.load(file)
        except FileNotFoundError:
            tag_data = []

        tag_data.append(new_tag)
        pathassigner("tags") 
        with open(var.TAGS_PATH, "w") as file:
            json.dump(tag_data, file, indent=4)

    except FileNotFoundError as e:
        logging.error("File not found: %s", e)
    except json.JSONDecodeError as e:
        logging.error("JSON decoding error: %s", e)
    except KeyError as e:
        logging.error("Key error: %s", e)
    except Exception as e:
        logging.error("Unexpected error in get_tag_name: %s", repr(e))

def fix_dt_format():
    try:
        now = datetime.now() + timedelta(hours=5)
        return now.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        
    except IndexError:
        return None

def crt_tag_file():
    pathassigner("tags")
    now = datetime.now()
    now = now.strftime("%Y-%m-%d-%H-%M")
    var.TAGS_PATH = str(now)+".json"
    with open(var.TAGS_PATH, "w") as file:
        file.write("[]")

def collect_files():
    try: 
        for file_name in os.listdir(var.folder_path):
            file_path = os.path.join(var.folder_path, file_name)

            if os.path.isfile(file_path):
                var.file_names.append(file_path)

        var.file_names.sort()
        var.Ct_file = len(var.file_names)
  
    except FileNotFoundError as e:
        logging.error("The folder path does not exist: %s", e)
    except PermissionError: 
        logging.error("You do not have premission to access folder path: %s", e)