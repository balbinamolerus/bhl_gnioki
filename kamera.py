from gpiozero import Servo
from time import sleep

servo = Servo(14)

while True:
    servo.mid()
    print('mid')
    sleep(5)
    x = servo.min()
    print('min')
    print(x)
    sleep(5)
    servo.mid()
    print('mid')
    sleep(5)
    y = servo.max()
    print('max')
    sleep(5)
    print(y)