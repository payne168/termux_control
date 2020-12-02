import uiautomator2 as u2
import settings
import time
from models import Transferee
from api import status
from settings import Status


class BotFactory:

    def __init__(self):
        settings.bot.device = u2.connect('RR8M90JGAXR')
        # settings.bot.device = u2.connect('0.0.0.0')
        module = __import__("bots.%s" % settings.bot.bank.lower())
        robot = getattr(module, settings.bot.bank.lower())
        self.bank = robot
        settings.bot.pid = self.bank.start()
        print("您的银行应用已经由脚本接管")
        status(settings.bot.serial_no, Status.RUNNING.value)
        self.works_list = []
        self.alive = True
        # self.wait_trans = False
        self.trans_process = False
        self.wait_msg = True

    def do_works(self):
        self.bank.remove_float_win()
        while self.alive:
            time.sleep(10)
            res = status(settings.bot.serial_no, Status.RUNNING.value)
            for work in self.works_list:
                print(work)
            if len(self.works_list) > 0:
                print("正在为您执行转账任务，请耐心等待...")
                self.cast_do_transfer(self.works_list.pop(0))

    def cast_do_transfer(self, trans):
        if settings.bot.pid == 0:
            settings.bot.pid = self.bank.start()
            if not settings.bot.pid:
                print('app出错了')
                return False
            else:
                self.bank.transfer(trans)
        else:
            self.bank.do_transfer(trans)

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
        print("已经收到短信，准备为您填充手机验证码")
        self.bank.post_sms(params)

    def cast_stop(self):
        self.alive = False
        status(settings.bot.serial_no, Status.STOP.value)
        self.bank.stop()

    def cast_transfer(self, order_id, amount, account, holder, bank_name):
        self.works_list.append(Transferee(order_id, amount, account, holder, bank_name))

    def do_verify_code(self, code):
        self.bank.post_verify_code(code)
