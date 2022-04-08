from gpiozero import Servo
from time import sleep

servo = Servo(14)
val = 1
try:
	while True:
		val=-val
		servo.value = val
except KeyboardInterrupt:
	print("Program stopfgped")