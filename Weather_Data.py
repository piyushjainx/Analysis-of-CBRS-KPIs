#Importing necessary files
import requests
import json
import datetime

#Key Parameters
api_key = "Insert Your API here"
city = 'Buffalo'
lat = "42.8865"
lon = "-78.8784"

url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)
response = requests.get(url)
print(response.text)

# Serializing json
json_object = json.dumps(response.text, indent=4)

# Writing to sample.json
file1 = open('response.json', 'w')
file1.write(response.text)
file1.close()


