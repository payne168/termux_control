# coding: utf-8


class Bot:
    def __init__(self, serial_no=None, device=None, bank=None, account=None, trans=None, last_trans=None):
        self.serial_no = serial_no
        self.device = device
        self.bank = bank
        self.account = account  # Account
        self.trans = trans  # AccountTrans
        self.last_trans = last_trans
        self.payment = False  # mode[receiving, payment]
        self.running = True
        self.pid = 0

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return self.__str__()


class Account:
    def __init__(self, alias=None, login_name=None, login_pwd=None, payment_pwd=None, currency=None):
        self.alias = alias
        self.login_name = login_name
        self.login_pwd = login_pwd
        self.payment_pwd = payment_pwd
        self.currency = currency

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return self.__str__()


class Transferee:
    def __init__(self, amount=None, account=None, holder=None, bank_name=None):
        self.amount = amount
        self.account = account
        self.holder = holder
        self.bank_name = bank_name


    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return self.__str__()


# class AccountTrans:
#     def __init__(self, last_trans=None, trans=None):
#         if trans is None:
#             trans = []
#         self.last_trans = last_trans  # Transaction
#         self.trans = trans  # [Transaction]
#         self.next_page = True  # if it is need to turn to next page
#
#     def __str__(self):
#         return str(self.__class__) + ": " + str(self.__dict__)
#
#     def __repr__(self):
#         return self.__str__()


class Transaction:
    def __init__(self, trans_time, trans_type=None, name=None, amount=None, balance=None, postscript=None, account=None,
                 summary=None, remark=None):
        self.trans_time = trans_time
        self.trans_type = trans_type
        self.name = name
        self.amount = amount
        self.balance = balance
        self.postscript = postscript
        self.account = account
        self.summary = summary

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return self.__str__()


class BotUtil:
    def __init__(self, cast_transfer=None, cast_transaction_history=None, cast_post_sms=None, cast_stop=None, do_works=None):
        self.cast_transfer = cast_transfer
        self.cast_transaction_history = cast_transaction_history
        self.cast_post_sms = cast_post_sms
        self.cast_stop = cast_stop
        self.do_works = do_works
