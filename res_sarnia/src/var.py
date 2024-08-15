# Smart Cover 
URL_TOKEN = "https://www.mysmartcover.com/api/auth/refresh.php"
URL_LIST = "https://www.mysmartcover.com/api/locations/list.php"
DAY = 5
Token_cr_at = None  
daysdate_ = None
exp_time_ = None
Token_ = "" # Initialize with new token if expired


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


