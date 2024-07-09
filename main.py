# import csv
import requests
import urllib3
import json
import os.path
urllib3.disable_warnings()

#Variables
id = 0
description = ""
ssr_id = []
ssr_description = []
ssr_lastreading = []
ssr_vaue = {}


# JWT token
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX3BrIjoiMTAxNTgiLCJpYXQiOjE3MjA0NzI0MDcsImV4cCI6MTc1MjAwODQwN30.QkZUUqJ7whj9mVag2o1qSf7KWJOW8-VtG8xuCoxRwbE"

# set the authorization header
HEADER={"Authorization": "Bearer {}".format(TOKEN)}

# GET call to recive the list in full.
response = requests.get('https://www.mysmartcover.com/api/locations/list.php', headers=HEADER, verify=False)
#print(response.content)

# Write response into a file
if os.path.isfile("data.json") == False: 
    with open("data.json", "w") as outfile:
        outfile.write(str(response.content))
    outfile.close()

# Filter the file
with open("data.json", "r") as infile: 
    data = infile.read()
    
    with open ("data.json", "w") as outfile: 
        data = data.replace("b'", "")
        data = data.replace("'","")
        outfile.write(data)
infile.close()
outfile.close()


# Tasks: 
#   1) Program must be able to update both Token and verify.
#   2) Program must be able to create a Jason file from a tap-properties-template JSON file.
#   3) Using the created JSON Tag need to use the TAG URL to create a new Tag (Must check current tags before creation) 
#   4) Program must be able to update tag property value with a set time.
#   5) Program must be able to execute on a real time bases.


    




