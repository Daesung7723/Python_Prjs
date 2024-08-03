# program to post data on ThingSpeak using requests module

import time, requests
import random

key = "LG2FO1N2ZGZVGX8O"  # Put your API Key here
def thermometer():
    while True:
        #Calculate CPU temperature of Raspberry Pi in Degrees C
        temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3 # Get Raspberry Pi CPU temp
        #temp = random.randint(30, 50) #random data

        payload = {'field1': temp, 'api_key': key} #payload to post

        try:
            response = requests.post('http://api.thingspeak.com/update', data=payload)
            print(temp)
            print(response.status_code, response.reason)
            print(response.text)
        except:
            print("connection failed")
        break
if __name__ == "__main__":
        while True:
                thermometer()
                time.sleep(20)

