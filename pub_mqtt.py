import signal
import sys
import RPi.GPIO as GPIO
from gpiozero import Button
import paho.mqtt.client as mqtt
import argparse
import time

def signal_handler(sig, frame):
        GPIO.cleanup()
        sys.exit(0)
def on_publish(client, userdata, mid):
    print("message published")
def on_pre_connect(client, userdata):
    print("About to connect to the broker...")
parser = argparse.ArgumentParser(description="MQTT Publisher")
parser.add_argument("--broker", required=True, help="MQTT broker address")
parser.add_argument("--port", type=int, default=1883, help="MQTT broker port")
parser.add_argument("--topic", required=True, help="MQTT topic to publish to")
parser.add_argument("--message", type=str, default=None, help="Message to publish")
parser.add_argument("--qos", type=int, default=0, help="Quality of Service (0, 1, or 2)")
parser.add_argument("--client_id", default="mqtt_publisher", help="Client ID")
args = parser.parse_args()

client = mqtt.Client(args.client_id)
client.on_pre_connect = on_pre_connect
client.on_publish = on_publish
client.connect(args.broker, args.port, keepalive=60)

# start a new thread
client.loop_start()

class Joystick:
	def __init__(self, pin_left, pin_right, pin_top, pin_down, pin_center):
		self.pin_left = pin_left
		self.pin_right = pin_right
		self.pin_top = pin_top
		self.pin_down = pin_down
		self.pin_center = pin_center
		self.x_value = 0
		self.y_value = 0
	def update(self, len):
		'''
		X value
		'''
		if Button(self.pin_left).is_pressed:
			if self.x_value > -100:
				self.x_value -= len
		elif Button(self.pin_right).is_pressed:
			if self.x_value < 100:
				self.x_value += len
		else:
			self.x_value = 0
		'''
		y value
		'''
		if Button(self.pin_top).is_pressed:
			if self.y_value < 100:
				self.y_value += len
		elif Button(self.pin_down).is_pressed:
			if self.y_value > -100:
				self.y_value -= len
		else:
			self.y_value = 0
	def get_x(self):
		return self.x_value
	def get_y(self):
		return self.y_value
	def get_center(self):
		return self.center_value
	def get_center_bit(self):
		return Button(self.pin_center).is_pressed

button_left = 17
button_right = 18
button_top = 6
button_down = 23
button_center = 22

joystick = Joystick(button_left, button_right, button_top, button_down, button_center)
signal.signal(signal.SIGINT, signal_handler)
while True:
	try:
		joystick.update(25)
		x = joystick.get_x()
		y = joystick.get_y()
		center = joystick.get_center_bit()
		msg = "{0:4.0f} {1:4.0f} {2:1.0f}".format(x, y, center)
		print(msg)
		pubMsg = client.publish(args.topic, msg, qos=args.qos)
		pubMsg.wait_for_publish()
		print(pubMsg.is_published())
	except Exception as e:
		print(e)
	time.sleep(2)
