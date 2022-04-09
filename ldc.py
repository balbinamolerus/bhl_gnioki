import os
from lib.waveshare_epd import epd2in9_V2
import time
import paho.mqtt.client as mqtt
from PIL import Image, ImageDraw, ImageFont

alarm = False
alarmType = ''



def on_message(client, userdata, message):
    global alarm
    global alarmType
    if message.topic == "alarm":
        alarm = True
        alarmType = str(message.payload.decode("utf-8"))


broker_address = "192.168.137.50"
client = mqtt.Client()
client.username_pw_set("user1", "user1")
client.on_message = on_message
client.connect(broker_address, 1880)

client.subscribe(
    [("alarm", 1)])

client.loop_start()

picdir = '/home/pi/bhl/bhl_gnioki/pic'
libdir = '/home/pi/bhl/bhl_gnioki/lib'
textpath = '/home/pi/bhl/bhl_gnioki/alerts.txt'
def screen():
    global alarm
    global alarmType

    epd = epd2in9_V2.EPD()
    epd.init()
    epd.Clear(0xFF)
    font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    fontAmelia = ImageFont.truetype('/home/pi/bhl/bhl_gnioki/flowers.ttf', 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    sumo = 0
    Himage = Image.new('1', (epd.height, epd.width), 255)
    print(epd.width, epd.height)
    draw = ImageDraw.Draw(Himage)
    lastTime = time.strftime('%H:%M')
    draw.text((200, 80), lastTime, font=font24, fill=0)
    epd.display_Partial(epd.getbuffer(Himage))
    draw.text((5, 80), "Amelia", font=fontAmelia, fill=0)
    while True:
        try:
            current_time = time.strftime('%H:%M')
            if current_time != lastTime:
                print('xd')

                with open(textpath) as file:
                    lines = file.readlines()
                    for line in lines:
                        idx = line.index(';')
                        event = line[:idx]
                        time1 = line[idx + 1:].replace('\n', '')
                        if current_time == time1:
                            alert = event
                            client.publish('alert', alert)
                            draw.text((50, 5), alert, font=font24, fill=0)
                        elif current_time[:2]==time1[:2] and int(current_time[-2:])-int(time1[-2:])!=0:
                            draw.rectangle((50, 5, 80, 45), fill=255)
                draw.text((200, 80), time.strftime('%H:%M'), font=font24, fill=0)
                lastTime = current_time
            if alarm:
                sumo += 1
                draw.text((10, 5), alarmType, font=font24, fill=0)
                if sumo == 2:
                    alarm = False
                    draw.rectangle((10, 5, 288, 32), fill=255)
                    sumo = 0
            epd.display_Partial(epd.getbuffer(Himage))
            time.sleep(2)
            lastTime = current_time
        except KeyboardInterrupt:
            draw.rectangle((200, 80, 290, 104), fill=255)
            epd.display_Partial(epd.getbuffer(Himage))
            time.sleep(2)
            epd2in9_V2.epdconfig.module_exit()
            exit()

client.loop_start()
client.subscribe([("alarm", 1)])
screen()
