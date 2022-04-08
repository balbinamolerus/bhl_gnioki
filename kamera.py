from gpiozero import Servo
from time import sleep

servo = Servo(14)
val = -1
x = 0.1
try:
	while True:
		servo.value = val
		sleep(0.1)
		val = val + x
		if val > 0.3:
			x = -x
		if val < -0.3:
			x = -x
except KeyboardInterrupt:
	print("Program stopfgped")