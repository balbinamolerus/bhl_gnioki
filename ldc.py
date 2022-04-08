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

def screen():
    global alarm
    global alarmType
    epd = epd2in9_V2.EPD()
    epd.init()
    epd.Clear(0xFF)
    font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    sumo = 0
    Himage = Image.new('1', (epd.height, epd.width), 255)
    print(epd.width, epd.height)
    draw = ImageDraw.Draw(Himage)
    lastTime = time.strftime('%H:%M')
    draw.text((200, 80), lastTime, font=font24, fill=0)
    epd.display_Partial(epd.getbuffer(Himage))
    while True:
        if time.strftime('%H:%M')!=lastTime:
            draw.rectangle((200, 80, 224, 104), fill=255)
            draw.text((200, 80), time.strftime('%H:%M'), font=font24, fill=0)
        if alarm:
            sumo+=1
            draw.text((10, 5), alarmType, font=font24, fill=0)
            if sumo==10:
                alarm = False
                draw.rectangle((10, 5, 288, 29), fill=255)
                sumo = 0
        epd.display_Partial(epd.getbuffer(Himage))

        # Drawing on the Vertical image
        # logging.info("2.Drawing on the Vertical image...")
        # Limage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        # draw = ImageDraw.Draw(Limage)
        # draw.text((2, 0), 'hello world', font=font18, fill=0)
        # draw.text((2, 20), '2.9inch epd', font=font18, fill=0)
        # draw.text((20, 50), u'微雪电子', font=font18, fill=0)
        # draw.line((10, 90, 60, 140), fill=0)
        # draw.line((60, 90, 10, 140), fill=0)
        # draw.rectangle((10, 90, 60, 140), outline=0)
        # draw.line((95, 90, 95, 140), fill=0)
        # draw.line((70, 115, 120, 115), fill=0)
        # draw.arc((70, 90, 120, 140), 0, 360, fill=0)
        # draw.rectangle((10, 150, 60, 200), fill=0)
        # draw.chord((70, 150, 120, 200), 0, 360, fill=0)
        # epd.display(epd.getbuffer(Limage))
        # time.sleep(2)
        #
        # logging.info("3.read bmp file")
        # Himage = Image.open(os.path.join(picdir, '2in9.bmp'))
        # epd.display(epd.getbuffer(Himage))
        # time.sleep(2)
        #
        # logging.info("4.read bmp file on window")
        # Himage2 = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        # bmp = Image.open(os.path.join(picdir, '100x100.bmp'))
        # Himage2.paste(bmp, (50, 10))
        # epd.display(epd.getbuffer(Himage2))
        # time.sleep(2)
        #
        # # partial update
        # logging.info("5.show time")
        # time_image = Image.new('1', (epd.height, epd.width), 255)
        # time_draw = ImageDraw.Draw(time_image)
        # epd.display_Base(epd.getbuffer(time_image))
        # num = 0
        # while (True):
        #     time_draw.rectangle((10, 10, 120, 50), fill=255)
        #     time_draw.text((10, 10), time.strftime('%H:%M:%S'), font=font24, fill=0)
        #     newimage = time_image.crop([10, 10, 120, 50])
        #     time_image.paste(newimage, (10, 10))
        #     epd.display_Partial(epd.getbuffer(time_image))
        #
        #     num = num + 1
        #     if (num == 10):
        #         break


client.loop_start()
client.subscribe([("alarm", 1)])
screen()