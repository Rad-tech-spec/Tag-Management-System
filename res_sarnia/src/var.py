# Smart Cover 
URL_TOKEN = "https://www.mysmartcover.com/api/auth/refresh.php"
URL_LIST = "https://www.mysmartcover.com/api/locations/list.php"
DAY = 15
DATA_PATH = "data.json"
SC_KEY = "SC.key"
TAG_NAMES = "tagnames.txt"

# Historian
URL_TOKEN = "https://snwpcc-hist1:8443/uaa/oauth/token?grant_type=password&username=SNWPCC-HIST1.admin&password=8$arniA"
URL_CREATE_TAG = "https://snwpcc-hist1:8443/historian-rest-api/v1/datapoints/create"
TAGS_PATH = "tag.json"
HS_KEY = "HS.key"

# TK Parameters
Token_cr_at = None  
daysdate_ = None
exp_time_ = None
Token_ = "" # Initialize with new token if expired
TK_INFO_PATH = "info.json"
PATH = "keys"
KEY = "key.key"

# Dictionaries
SENSORS = dict(
    BATT = "PowerPack Voltage", 
    LEVEL = "Water Level above Bottom", 
    ANL = "Analog Sensor",
    SQ =  "Signal Quality", 
    SS =  "Signal Strength", 
    TEMP =  "Temperature", 
    FLOW =  "SmartFLOE(TM)", 
    RAIN = "Rain"
)

# Ignoring ids
IG_ID = (39583, 39704, 40694)
IG_PARA = "Distance below Sensor"


