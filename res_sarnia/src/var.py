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

# Classes
class Tag: 
    def __init__(self) -> None:
        pass
    
    id = None
    name = ""
    des = ""
    value = None  
    date = ""

    def getname(self):
        return self.name
    def getdes(self): 
        return self.des
    def getvalue(self): 
        return self.value
    def getdate(self): 
        return self.date
    
