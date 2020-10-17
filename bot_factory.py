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
        self.wait_trans = False
        self.trans_process = False
        self.wait_msg = True

    def do_works(self):
        while self.alive:
            time.sleep(10)
            status(settings.bot.serial_no, Status.RUNNING.value)
            print(self.wait_trans)
            if not self.wait_trans:
                if len(self.works_list) > 0:
                    print("正在为您执行转账任务，请耐心等待...")
                    self.wait_trans = self.cast_do_transfer(self.works_list.pop(0))
                else:
                    print("正在为您执行流水查询任务，请耐心等待...")
                    self.cast_transaction_history()
            # times = 0
            # count = 0
            # else:
            #     times += 1
            #     if times > 3:
            #         self.wait_trans = False
            #         self.bank.close_win()
            #         self.bank.back_activity()
            #         self.bank.back_activity()
            #         self.bank.false_msg("短信验证码超时！")
            #         self.do_works()
            #
            #     a = 60
            #     while count < a and self.wait_msg:
            #         count_now = a - count
            #         print(count_now)
            #         time.sleep(1)  # sleep 1 second
            #         count += 1
            #     self.bank.press_resend()
            #     print('done')

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
        print("已经收到短信，准备为您填充手机验证码")
        self.wait_trans = self.bank.post_sms(params)
        return self.wait_trans

    def cast_stop(self):
        self.alive = False
        status(settings.bot.serial_no, Status.STOP.value)
        self.bank.stop()

    def cast_transfer(self, order_id, amount, account, holder, bank_name):
        self.works_list.append(Transferee(order_id, amount, account, holder, bank_name))
