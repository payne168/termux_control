import os
import signal
from asyncio import Queue
import uiautomator2 as u2
import settings
import time
from models import Transferee
from api import status
from settings import Status


class BotFactory:

    def __init__(self):
        # settings.bot.device = u2.connect('RR8M90JGAXR')
        settings.bot.device = u2.connect('0.0.0.0')
        module = __import__("bots.%s" % settings.bot.bank.lower())
        robot = getattr(module, settings.bot.bank.lower())
        self.bank = robot
        settings.bot.pid = self.bank.start()
        status('RR8M90JGAXR', Status.RUNNING.value)
        self.works_list = []
        self.alive = True
        self.waitTrans = False

    def do_works(self):
        while self.alive:
            time.sleep(10)
            status('RR8M90JGAXR', Status.RUNNING.value)
            if not self.waitTrans:
                if len(self.works_list) > 0:
                    self.waitTrans = self.cast_do_transfer(self.works_list.pop(0))
                else:
                    self.cast_transaction_history()

    def cast_do_transfer(self, trans):
        if settings.bot.pid == 0:
            settings.bot.pid = self.bank.start()
            if not settings.bot.pid:
                print('app出错了')
                return False
            else:
                return self.bank.transfer(trans)
        else:
            return self.bank.do_transfer(trans)

    def cast_transaction_history(self):
        if settings.bot.pid == 0:
            settings.bot.pid = self.bank.start()
            if not settings.bot.pid:
                print('app没有打开')
            else:
                self.bank.transaction_history()
        else:
            self.bank.do_transaction()

    def cast_post_sms(self, params):
        self.waitTrans = self.bank.post_sms(params)
        return self.waitTrans

    def cast_stop(self):
        self.alive = False
        self.bank.stop()
        os.kill(settings.bot.pid, signal.SIGSTOP)

    def cast_transfer(self, amount, account, holder, bank_name):
        self.works_list.append(Transferee(amount, account, holder, bank_name))
