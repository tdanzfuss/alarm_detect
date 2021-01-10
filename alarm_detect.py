import RPi.GPIO as GPIO
import time
import redis
import os
import time
import json
import datetime

last_trigger_time = []
configFileLocation = os.getenv('alarm_config_location') 
if not configFileLocation :
    configFileLocation = '../appsettings.json'
    
configFile = open(configFileLocation)
config = json.load(configFile)

r = redis.Redis(host=config['Redis']['ip'], port=config['Redis']['port'], db=0, password=config['Redis']['password'])
r_pubsub = r.pubsub()

def my_callback(zoneID):
    global last_trigger_time
    trigger_time = datetime.datetime.now()
    time_since_last_trigger = trigger_time - last_trigger_time[zoneID]
    if time_since_last_trigger.total_seconds() > 30:
        last_trigger_time[zoneID] = trigger_time
        r.publish('ALARM_TRIGGER',zoneID)
        print ('Alarm Triggered')

GPIO.setmode(GPIO.BCM)
sensorPins = config["Sensors"]["Pins"]
for idx, pin in enumerate(sensorPins):
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(pin, GPIO.FALLING)
    GPIO.add_event_callback(pin, callback=lambda x:my_callback(idx))
    last_trigger_time.append(datetime.datetime.now())

#ALSO LISTEN ON TEST PUBSUB CHANNEL
# r_pubsub.subscribe(**{'TEST_TRIGGER':my_callback})
# r_pubsub.run_in_thread(sleep_time=0.001)

while True:
    time.sleep(1)
    # print ('.')