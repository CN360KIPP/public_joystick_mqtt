'''
import time
import paho.mqtt.client as mqtt
import ssl
import signal
from gpiozero import Button
import pywifi

version = '3' # or '3'
mytransport = 'websockets' # or 'tcp'

if version == '5':
    client = mqtt.Client(client_id="myPy",
                         transport=mytransport,
                         protocol=mqtt.MQTTv5)
if version == '3':
    client = mqtt.Client(client_id="myPy",
                         transport=mytransport,
                         protocol=mqtt.MQTTv311,
                         clean_session=True)

client.username_pw_set("user", "password")
client.tls_set(certfile=None,
               keyfile=None,
               # If these arguments above are not None then they will
               # be used as client information for TLS based
               # authentication and authorization (depends on broker setup).
               cert_reqs=ssl.CERT_REQUIRED)
               # this makes it mandatory that the broker
               # has a valid certificate

import mycallbacks

client.on_connect = mycallbacks.on_connect;
client.on_message = mycallbacks.on_message;
client.on_publish = mycallbacks.on_publish;
client.on_subscribe = mycallbacks.on_subscribe;

broker = 'broker.hivemq.com' # eg. choosen-name-xxxx.cedalo.cloud

myport = 443
if version == '5':
    from paho.mqtt.properties import Properties
    from paho.mqtt.packettypes import PacketTypes
    properties=Properties(PacketTypes.CONNECT)
    properties.SessionExpiryInterval=30*60 # in seconds
    client.connect(broker,
                   port=myport,
                   clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY,
                   properties=properties,
                   keepalive=60);

if version == '3':
    client.connect(broker,port=myport,keepalive=60);

client.loop_start();

mytopic = 'joystick'
client.subscribe(mytopic,2);

from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
properties=Properties(PacketTypes.PUBLISH)
properties.MessageExpiryInterval=30 # in seconds

def signal_handler(sig, frame):
        GPIO.cleanup()
        sys.exit(0)

# joystick pin
pin_left = 17
pin_right = 18
pin_up = 6
pin_down = 23
pin_center = 22

class Joystick:
        def __init__(self, left, right, up, down, center):
                self.pin_left = left
                self.pin_right = right
                self.pin_up = up
                self.pin_down = down
                self.pin_center = center
                self.x = 0
                self.y = 0
                self.center = 0
        def update(self, len):
                if Button(self.pin_center).is_pressed:
                        if self.center+len < 255:
                                self.center += len
                else:
                        if self.center-len > 0:
                                self.center -= len
                if Button(self.pin_left).is_pressed:
                        if self.x-len > 0:
                                self.x -= len
                if Button(self.pin_right).is_pressed:
                        if self.x+len < 255:
                                self.x += len
                if Button(self.pin_up).is_pressed:
                        if self.y+len < 255:
                                self.y += len
                if Button(self.pin_down).is_pressed:
                        if self.y-len > 0:
                                self.y += len
        def get_x(self):
                return self.x
        def get_y(self):
                return self.y
        def get_center(self):
                return self.center

joystick = Joystick(pin_left, pin_right, pin_up, pin_down, pin_center)
signal.signal(signal.SIGINT, signal_handler)
while True:
        # if connect_to_wifi():
	joystick.update(8)
	x = joystick.get_x()
	y = joystick.get_y()
	center = joystick.get_center()
	print(f"X: {x}, Y: {y}, Center: {center}")
	data_to_send = f"X: {x}, Y: {y}, Center: {center}"
	client.publish(mytopic,data_to_send,2,properties=properties)
'''
'''
# WiFi credentials
WIFI_SSID = "KT"
WIFI_PASSWORD = "1234567890"

# MQTT broker settings
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "joystick"
MQTT_USERNAME = "KIPP"
MQTT_PASSWORD = "raspberry"

def connect_to_wifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    profile = pywifi.Profile()
    profile.ssid = WIFI_SSID
    # profile.auth = pywifi.const.AUTH_ALG_OPEN
    # profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
    # profile.cipher = pywifi.const.CIPHER_TYPE_CCMP
    profile.key = WIFI_PASSWORD

    iface.remove_all_network_profiles()
    iface.connect(profile)
    time.sleep(5)

    if iface.status() == const.IFACE_CONNECTED:
        print("Connected to WiFi")
        return True
    else:
        print("Failed to connect to WiFi")
        return False

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
    else:
        print(f"Connection to MQTT Broker failed with code {rc}")

def send_mqtt_data(data):
    client = mqtt.Client()
    client.on_connect = on_connect

    client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
    client.connect(MQTT_BROKER, MQTT_PORT)

    client.loop_start()

    client.publish(MQTT_TOPIC, data)
    time.sleep(2)

    client.loop_stop()
    client.disconnect()
    print(f"Data sent to MQTT: {data}")

def signal_handler(sig, frame):
	GPIO.cleanup()
	sys.exit(0)
send_mqtt_data(data_to_send)
'''
import time
import paho.mqtt.client as mqtt
import signal
from gpiozero import Button

def signal_handler(sig, frame):
        GPIO.cleanup()
        sys.exit(0)
def on_publish(client, userdata, mid):
    print("message published")
def on_pre_connect(client, userdata):
    print("About to connect to the broker...")

client = mqtt.Client("KIPP") #this name should be unique
client.on_pre_connect = on_pre_connect
client.on_publish = on_publish
client.connect('172.20.10.7',1883)
# start a new thread
client.loop_start()
# joystick pin
pin_left = 17
pin_right = 18
pin_up = 6
pin_down = 23
pin_center = 22
class Joystick:
        def __init__(self, left, right, up, down, center):
                self.pin_left = left
                self.pin_right = right
                self.pin_up = up
                self.pin_down = down
                self.pin_center = center
                self.x = 0
                self.y = 0
                self.center = 0
        def update(self, len):
                if Button(self.pin_center).is_pressed:
                        if self.center+len < 255:
                                self.center += len
                else:
                        if self.center-len > 0:
                                self.center -= len
                if Button(self.pin_left).is_pressed:
                        if self.x-len > 0:
                                self.x -= len
                if Button(self.pin_right).is_pressed:
                        if self.x+len < 255:
                                self.x += len
                if Button(self.pin_up).is_pressed:
                        if self.y+len < 255:
                                self.y += len
                if Button(self.pin_down).is_pressed:
                        if self.y-len > 0:
                                self.y += len
        def get_x(self):
                return self.x
        def get_y(self):
                return self.y
        def get_center(self):
                return self.center
joystick = Joystick(pin_left, pin_right, pin_up, pin_down, pin_center)
signal.signal(signal.SIGINT, signal_handler)
while True:
	try:
		joystick.update(8)
		x = joystick.get_x()
		y = joystick.get_y()
		center = joystick.get_center()
		msg = f"X: {x}, Y: {y}, Center: {center}"
		print(msg)
		pubMsg = client.publish(topic='joystick',
		payload=msg.encode('utf-8'),
		qos=0,)
		pubMsg.wait_for_publish()
		print(pubMsg.is_published())
	except Exception as e:
		print(e)
	time.sleep(2)
