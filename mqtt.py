import network
import time
import paho.mqtt.client as mqtt
import signal
from gpiozero import Button
from pywifi import PyWiFi, const

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
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]

    profile = iface.add_network_profile()
    profile.ssid = WIFI_SSID
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
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

joystick = joystick(pin_left, pinh_right, pin_up, pin_down, pincenter)
signal.signal(signal.SIGINT, signal_handler)
while True:
	if connect_to_wifi():
		joystick.update(8)
		x = joystick.get_x()
		y = joystick.get_y()
		center = joystick.get_center()
		print(f"X: {x}, Y: {y}, Center: {center}")
		data_to_send = f"X: {x}, Y: {y}, Center: {center}"
		send_mqtt_data(data_to_send)

