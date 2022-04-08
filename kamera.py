from gpiozero import Servo
import time

servo = Servo(14)
val = 1
try:
	while True:
		servo.max()
		time.sleep(0.02)
		servo.detach()
except KeyboardInterrupt:
	print("Program stopfgped")