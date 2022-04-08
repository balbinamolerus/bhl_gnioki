import time
import smbus
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from pygame import mixer
from telegram import Telegram

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
tele = Telegram()
buzzer = 20
switch = 16
play = 17

mixer.init()
mixer.music.load("/home/pi/Documents/ElevatorMusic.mp3")

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(switch, GPIO.IN)
GPIO.setup(play, GPIO.IN)



def on_message(client, userdata, message):
    pass

broker_address = "192.168.137.50"
client = mqtt.Client()
client.username_pw_set("user1", "user1")
client.on_message = on_message
client.connect(broker_address, 1880)

client.subscribe(
    [("alarm", 1)])

client.loop_start()

def MPU_Init():
    # write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

    # Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

    # Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)

    # Write to Gyro configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

    # Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)


def read_raw_data(addr):
    # Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr + 1)

    # concatenate higher and lower value
    value = ((high << 8) | low)

    # to get signed value from mpu6050
    if (value > 32768):
        value = value - 65536
    return value

bus = smbus.SMBus(1)  # or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68  # MPU6050 device address

MPU_Init()

state = "PAUSED"
last_play = GPIO.HIGH
last_gas = GPIO.HIGH
last_Ay = 1

while True:
    # Read Accelerometer raw value
    acc_y = read_raw_data(ACCEL_YOUT_H)
    Ay = acc_y / 16384.0
    p = GPIO.input(play)
    gas = GPIO.input(switch)

    print("Ay = %.2f g" % Ay, "\tGas = {}".format(GPIO.input(switch)), "\tMusic:", state)

    # Sense CO2 or falling
    if Ay < 0.4 and last_Ay >= 0.4:
        GPIO.output(buzzer, GPIO.HIGH)
        client.publish("alarm", "fall")
        tele.send_message("fall detected! contact babcia")
        time.sleep(1)
    elif gas == GPIO.LOW and last_gas == GPIO.HIGH:
        GPIO.output(buzzer, GPIO.HIGH)
        client.publish("alarm", "CO2")
        tele.send_message("CO2 detected! contact babcia")
        time.sleep(1)
    else:
        GPIO.output(buzzer, GPIO.LOW)

    # Music
    if p == GPIO.LOW and last_play == GPIO.HIGH and state == "PAUSED":
        mixer.music.play()
        state = "PLAYING"
    elif p == GPIO.LOW and last_play == GPIO.HIGH and state == "PLAYING":
        mixer.music.pause()
        state = "PAUSED"

    last_play = p
    last_gas = gas
    last_Ay = Ay
    time.sleep(0.1)


GPIO.cleanup()
