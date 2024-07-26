URL_TOKEN = "https://www.mysmartcover.com/api/auth/refresh.php"
URL_LIST = "https://www.mysmartcover.com/api/locations/list.php"
DAY = 5
Token_cr_at = None  
daysdate_ = None
exp_time_ = None
Token_ = "" # To be removed


# Dictionaries
SENSORS = dict(
    BATT = "PowerPack Voltage", 
    LEVEL = "Analog Sensor", 
    SQ =  "Signal Quality", 
    SS =  "Signal Strength", 
    TEMP =  "Temperature", 
    FLOW =  "SmartFLOE(TM)", 
    RAIN = "Water Level above Bottom"
)

# Ignoring ids
IG_ID = (39583, 39704, 40694)
IG_PARA = "Distance below Sensor"

# Classes
class Tag: 

    id_ = None
    name_ = ""
    des_ = ""
    value_ = None  
    date_ = ""

    def __init__(self) -> None:
        pass

    def __init__(self, name, id, des, value, date):
        self.name_ = name
        self.id_ = id
        self.des_ = des
        self.value_ = value
        self.date_ = date
    
