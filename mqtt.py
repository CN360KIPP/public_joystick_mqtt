import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

import signal
import gpiozero import Button

def signal_handler(sig, frame):
	GPIO.cleanup()
	sys.exit(0)

# joystick pin
pin_left = 17
pin_right = 18
pin_up = 6
pin_down = 23
pin_center = 22

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Wi-Fi AP","PASSWORD")

time.sleep(5)
print(wlan.isconnected())

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
	joystick.update(8)
	x = joystick.get_x()
	y = joystick.get_y()
	center = joystick.get_center()
	print(f"X: {x}, Y: {y}, Center: {center}")
