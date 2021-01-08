import RPi.GPIO as GPIO
import time
import redis
import os
import time
import json

configFile = open('../appsettings.json')
config = json.load(configFile)

r = redis.Redis(host=config['Redis']['ip'], port=config['Redis']['port'], db=0, password=config['Redis']['password'])
r_pubsub = r.pubsub()
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def my_callback(self):
    r.publish('ALARM_TRIGGER',1)
    print ('Alarm Triggered on '+ str(self))

GPIO.add_event_detect(26, GPIO.FALLING, callback=my_callback)
#ALSO LISTEN ON TEST PUBSUB CHANNEL
r_pubsub.subscribe(**{'TEST_TRIGGER':my_callback})
r_pubsub.run_in_thread(sleep_time=0.001)

while True:
    time.sleep(1)
    # print ('.')