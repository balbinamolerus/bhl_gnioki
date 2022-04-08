from gpiozero import Servo
import time

def powiadomienie():
	servo = Servo(14)
	val = 0
	try:
		while True:
			servo.max()
			time.sleep(0.05)
			servo.detach()
			servo.min()
			time.sleep(0.05)
			servo.detach()
			val+=1
			if val==10:
				break

powiadomienie()