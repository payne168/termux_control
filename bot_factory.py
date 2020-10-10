import settings
import uiautomator2 as u2
from models import Bot
import misc
import sys


class BotFactory:

    def __init__(self, serial_no=None, bank=None, account=None):
        settings.bot = Bot(serial_no=misc.load_serial_no(), bank=bank, account=account)
        # settings.bot.device = u2.connect('RR8M90JGAXR')
        settings.bot.device = u2.connect('0.0.0.0')
        Bank = __import__("bots.%s" % bank.lower())
        robot = getattr(Bank, bank.lower())
        self.bank = robot

    def cast_transfer(self,  amount, account, name, bank_name, password, withdraw_password):
        settings.bot.pid = self.bank.start(settings.bot.device)
        if not settings.bot.pid:
            print('app没有打开')
        else:
            self.bank.transfer(settings.bot.device, amount, account, name, bank_name, password, withdraw_password)

    def cast_inquire_balance(self, password):
        settings.bot.pid = self.bank.start(settings.bot.device)
        if not settings.bot.pid:
            print('app没有打开')
        else:
            self.bank.inquire_balance(settings.bot.device, password)

    def cast_post_sms(self, params):
        return self.bank.post_sms(settings.bot.device, params)

    def cast_stop(self):
        return self.bank.stop(settings.bot.device)
