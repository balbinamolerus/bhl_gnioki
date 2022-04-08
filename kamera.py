from gpiozero import Servo
from time import sleep

servo = Servo(14)

while True:
    servo.mid()