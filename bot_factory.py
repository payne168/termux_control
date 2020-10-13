import uiautomator2 as u2

import settings


class BotFactory:

    def __init__(self):
        # settings.bot.device = u2.connect('RR8M90JGAXR')
        settings.bot.device = u2.connect('0.0.0.0')
        module = __import__("bots.%s" % settings.bot.bank.lower())
        robot = getattr(module, settings.bot.bank.lower())
        self.bank = robot

    def cast_transfer(self,  amount, account, name, bank_name, password, withdraw_password):
        if settings.bot.pid == 0:
            settings.bot.pid = self.bank.start(settings.bot.device)
            if not settings.bot.pid:
                print('app出错了')
            else:
                self.bank.transfer(settings.bot.device, amount, account, name, bank_name, password, withdraw_password)
        else:
            self.bank.transaction(settings.bot.device, amount, account, name, bank_name, password, withdraw_password)

    def cast_inquire_balance(self, password):
        if settings.bot.pid == 0:
            settings.bot.pid = self.bank.start(settings.bot.device)
            if not settings.bot.pid:
                print('app没有打开')
            else:
                self.bank.inquire_balance(settings.bot.device, password)
        else:
            self.bank.transaction_history(settings.bot.device, password)

    def cast_post_sms(self, params):
        return self.bank.post_sms(settings.bot.device, params)

    def cast_stop(self):
        return self.bank.stop(settings.bot.device)
