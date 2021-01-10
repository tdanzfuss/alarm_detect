import RPi.GPIO as GPIO
import time
import redis
import os
import time
import json
import datetime

last_trigger_time = datetime.datetime.now()
configFileLocation = os.getenv('alarm_config_location') 
if not configFileLocation :
    configFileLocation = '../appsettings.json'
    
configFile = open(configFileLocation)
config = json.load(configFile)

r = redis.Redis(host=config['Redis']['ip'], port=config['Redis']['port'], db=0, password=config['Redis']['password'])
r_pubsub = r.pubsub()
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(26, GPIO.FALLING)
def my_callback(self):
    global last_trigger_time
    trigger_time = datetime.datetime.now()
    time_since_last_trigger = trigger_time - last_trigger_time
    if time_since_last_trigger.total_seconds() > 30:
        last_trigger_time = trigger_time
        r.publish('ALARM_TRIGGER',0)
        print ('Alarm Triggered')


GPIO.add_event_callback(26, my_callback)

#ALSO LISTEN ON TEST PUBSUB CHANNEL
# r_pubsub.subscribe(**{'TEST_TRIGGER':my_callback})
# r_pubsub.run_in_thread(sleep_time=0.001)

while True:
    time.sleep(1)
    # print ('.')