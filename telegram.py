import time
import telepot
from telepot.loop import MessageLoop


class Telegram:
    def __init__(self):
        self.bot = telepot.Bot('1865773870:AAET2CqaAeUoe_gdTlfyZco887fcskxBdCk')
        self.users = [1255224844, 1990072643]
        MessageLoop(self.bot, self.handle).run_as_thread()


    def send_message(self, message):
        for ID in self.users:
            self.bot.sendMessage(ID, message)

    def handle(self, msg):
        if msg['from']['id'] in self.users:
            if '/ping' in msg['text']:
                self.bot.sendMessage(msg['from']['id'], 'Pong!')
        else:
            self.bot.sendMessage(msg['from']['id'],
                                 'No permisions! Ask admin to add your ID.\nYour ID:\n' + str(msg['from']['id']))