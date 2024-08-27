# Smart Cover 
URL_TOKEN = "https://www.mysmartcover.com/api/auth/refresh.php"
URL_LIST = "https://www.mysmartcover.com/api/locations/list.php"
DAY = 15
Token_cr_at = None  
daysdate_ = None
exp_time_ = None
Token_ = "" # Initialize with new token if expired

# Historian
URL_TOKEN = "https://snwpcc-hist1:8443/uaa/oauth/token?grant_type=password&username=SNWPCC-HIST1.admin&password=8$arniA"
URL_CREATE_TAG = "https://snwpcc-hist1:8443/historian-rest-api/v1/datapoints/create"

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


