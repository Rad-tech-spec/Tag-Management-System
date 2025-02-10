import os
from dotenv import load_dotenv, find_dotenv

dotenv_path=find_dotenv()
load_dotenv(dotenv_path)

SMART_COVER = {
    "URL_TOKEN": os.getenv("URL_SC_TOKEN"),
    "URL_LIST": "https://www.mysmartcover.com/api/locations/list.php",
    "DAY": 15,
    "DATA_PATH": "data.json",
    "SC_KEY": "SC.key",
    "TAG_NAMES": "tagnames.txt",
    "SC_TOKEN": "",  
}

HISTORIAN = {
    "URL_HS_TOKEN": os.getenv("URL_HS_TOKEN"),
    "URL_CREATE_TAG": "https://snwpcc-hist1:8443/historian-rest-api/v1/datapoints/create",
    "TAGS_PATH": "",
    "HS_KEY": "HS.key",
    "USER": os.getenv("SC_USER"),
    "PASSWORD": os.getenv("PASSWORD"),
    "HS_TOKEN": "",
    "file_names": []
}

COUNTERS = {
    "Ct": 0,
    "Ct_file": 0,
    "switch": True,
}

TOKEN_INFO = {
    "Token_cr_at": "",
    "daysdate_": None,
    "exp_time_": None,
}

FILE_PATHS = {
    "folder_path": "../tags",
    "TK_INFO_PATH": "info.json",
    "KEYS_PATH": "keys",
    "KEY": "key.key",
}

SENSORS = dict(
    BATT = "PowerPack Voltage", 
    LEVEL = "Water Level above Bottom",
    ANL = "Analog Sensor",
    SQ =  "Signal Quality", 
    SS =  "Signal Strength", 
    TEMP =  "Temperature", 
    FLOW =  "SmartFLOE(TM)", 
    RAIN = "Rain",
    LEVEL_2 = "Distance below Sensor"
)

IG_ID = (2000, 40694)



URL_TOKEN = SMART_COVER["URL_TOKEN"]
URL_LIST = SMART_COVER["URL_LIST"]
DAY = SMART_COVER["DAY"]
DATA_PATH = SMART_COVER["DATA_PATH"]
SC_KEY = SMART_COVER["SC_KEY"]
TAG_NAMES = SMART_COVER["TAG_NAMES"]
SC_TOKEN = SMART_COVER["SC_TOKEN"]

URL_HS_TOKEN = HISTORIAN["URL_HS_TOKEN"]
URL_CREATE_TAG = HISTORIAN["URL_CREATE_TAG"]
TAGS_PATH = HISTORIAN["TAGS_PATH"]
HS_KEY = HISTORIAN["HS_KEY"]
USER = HISTORIAN["USER"]
PASSWORD = HISTORIAN["PASSWORD"]
HS_TOKEN = HISTORIAN["HS_TOKEN"]
file_names = HISTORIAN["file_names"]

Ct = COUNTERS["Ct"]
Ct_file = COUNTERS["Ct_file"]
switch = COUNTERS["switch"]

Token_cr_at = TOKEN_INFO["Token_cr_at"]
daysdate_ = TOKEN_INFO["daysdate_"]
exp_time_ = TOKEN_INFO["exp_time_"]

folder_path = FILE_PATHS["folder_path"]
TK_INFO_PATH = FILE_PATHS["TK_INFO_PATH"]
KEYS_PATH = FILE_PATHS["KEYS_PATH"]
KEY = FILE_PATHS["KEY"]