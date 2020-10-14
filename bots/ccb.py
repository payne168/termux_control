# coding: utf8
import time
import sys
from bots.verification.verification_code import VerificationCode
import settings

sys.path.append("..")
from models import Account, Transferee, Transaction

package = 'com.chinamworld.main'
activity = 'com.ccb.start.MainActivity'

# def connect():
#     connection = u2.connect('0.0.0.0')
#     connection = u2.connect('R3CN90724BK')
#     print(connection.info)
#     return connection

trans = Transferee()
self = settings.bot.device


def start():
    self.screen_on()
    self.app_start(package)
    return self.app_wait(package)  # 等待应用运行, return pid(int)


def stop():
    self.app_stop(package)


def login():
    self(resourceId="com.chinamworld.main:id/et_password").click()
    for i in settings.bot.account.login_pwd:
        time.sleep(1)
        self(text=i).click()
    self(resourceId="com.chinamworld.main:id/btn_confirm").click_gone(maxretry=10, interval=1.0)


def change_activity(page_activity):
    LoginActivity = self.wait_activity("com.ccb.framework.security.login.internal.view.LoginActivity", timeout=5)
    print(LoginActivity)
    if LoginActivity:
        login()
    page = self.wait_activity(page_activity, timeout=60)
    return page


def back_activity():
    LoginActivity = self.wait_activity("com.ccb.framework.security.login.internal.view.LoginActivity", timeout=5)
    if LoginActivity:
        login()
    else:
        self(resourceId="com.chinamworld.main:id/ccb_title_left_btn").click()


def input_form():
    SmartTransferMainAct = change_activity("com.ccb.transfer.smarttransfer.view.SmartTransferMainAct")
    if SmartTransferMainAct:
        self(resourceId="com.chinamworld.main:id/et_cash_name").click()
        self(resourceId="com.chinamworld.main:id/et_cash_name").set_text(trans.holder)
        self(resourceId="com.chinamworld.main:id/et_collection_account").click()
        self(resourceId="com.chinamworld.main:id/et_collection_account").set_text(trans.account)
        self.press("back")
        self(resourceId="com.chinamworld.main:id/tv_transfer_way").click()
        if self(text="实时转账").exists(timeout=60):
            self(resourceId="com.chinamworld.main:id/bottom_selector_tv", text="实时转账").click()
            self(resourceId="com.chinamworld.main:id/et_tran_amount").click()
            self.send_keys(trans.amount.toString(), clear=True)
            self.press("back")
            self(resourceId="com.chinamworld.main:id/rl_tran_mark").click()
            self.send_keys("今天发的1元钱", clear=True)
            self.press("back")
            self(resourceId="com.chinamworld.main:id/tv_bank").click()
            if self(text="热门银行").exists(timeout=60):
                print(trans.bank_name)
                bank_btn = self(resourceId="com.chinamworld.main:id/title", text=trans.bank_name)
                if bank_btn.click_gone(maxretry=60, interval=1.0):
                    self(resourceId="com.chinamworld.main:id/btn_right1").click()
                    if self(resourceId="com.chinamworld.main:id/dlg_right_tv").exists(timeout=60):
                        self(resourceId="com.chinamworld.main:id/dlg_right_tv").click()


def remove_float_win():
    if self(text="是否需要向银行卡").exists(timeout=5):
        self(resourceId="com.chinamworld.main:id/btn_cancel").click_gone(maxretry=10, interval=1.0)
    if self(resourceId="com.chinamworld.main:id/close").exists(timeout=5):
        self(resourceId="com.chinamworld.main:id/close").click_gone(maxretry=10, interval=1.0)
    return True


def do_transfer(transferee):
    self(resourceId="com.chinamworld.main:id/main_home_smart_transfer").click()
    waitTransferHomeAct = change_activity("com.ccb.transfer.transfer_home.view.TransferHomeAct")
    print("---------------------------")
    print(transferee)
    print("---------------------------")
    if waitTransferHomeAct:
        trans.amount = transferee.amount
        trans.account = transferee.account
        trans.holder = transferee.holder
        trans.bank_name = transferee.bank_name
        self.xpath('//*[@resource-id="com.chinamworld.main:id/grid_function"]/android.widget.LinearLayout[1]').click()
        input_form()
    return True


def transfer(transferee):
    # 转账
    def do_trans():
        waitRes = self.wait_activity(activity, timeout=60)
        print('waitRes %s' % waitRes)
        if waitRes:
            do_transfer(transferee)

    if remove_float_win():
        do_trans()
    return True


def transaction_history():
    # 抓取流水

    def do_inquire():
        waitRes = self.wait_activity(activity, timeout=60)
        print('waitRes %s' % waitRes)
        if waitRes:
            transaction_history()

    if remove_float_win():
        do_inquire()


def do_transaction():
    self(resourceId="com.chinamworld.main:id/text_item", text="账户").click()
    MyAccountMainAct = change_activity("com.ccb.myaccount.view.MyAccountMainAct")

    if MyAccountMainAct:
        self(text="详情").click()
        TitledActivity = change_activity("com.ccb.framework.app.TitledActivity")

        if TitledActivity:
            self(resourceId="com.chinamworld.main:id/type", text="活期储蓄").click()

            if self(text="总收入").exists(timeout=60):
                transaction_record = do_get_history()
                print(transaction_record)


def do_get_history(i=1):
    transaction_list = []
    while i < 2:
        def get_trans_type():
            return self.xpath('//*[@resource-id="com.chinamworld.main:id/detail_list"]/android.widget.LinearLayout['
                              '%s]/android.widget.LinearLayout[1]/android.widget.LinearLayout['
                              '1]/android.widget.RelativeLayout[1]/android.widget.TextView[1]' % i).get_text()

        def get_time():
            if i == 1:
                return self.xpath(
                    '//*[@resource-id="com.chinamworld.main:id/more"]/android.widget.RelativeLayout['
                    '1]/android.widget.TextView[2]').get_text()
            else:
                return self.xpath(
                    '//*[@resource-id="com.chinamworld.main:id/detail_list"]/android.widget.LinearLayout['
                    '%s]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout['
                    '1]/android.widget.RelativeLayout[1]/android.widget.TextView[2]' % i).get_text()

        def get_account():
            if i == 1:
                return self.xpath(
                    '//*[@resource-id="com.chinamworld.main:id/more"]/android.widget.RelativeLayout['
                    '3]/android.widget.TextView[2]').get_text()
            else:
                return self.xpath(
                    '//*[@resource-id="com.chinamworld.main:id/detail_list"]/android.widget.LinearLayout['
                    '%s]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout['
                    '1]/android.widget.RelativeLayout[3]/android.widget.TextView[2]' % i).get_text()

        self.xpath('//*[@resource-id="com.chinamworld.main:id/detail_list"]/android.widget.LinearLayout['
                   '%s]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.RelativeLayout['
                   '1]/android.widget.ToggleButton[1]' % i).click()
        time.sleep(2)
        amount = self.xpath('//*[@resource-id="com.chinamworld.main:id/detail_list"]/android.widget.LinearLayout['
                            '%s]/android.widget.LinearLayout[1]/android.widget.LinearLayout['
                            '1]/android.widget.RelativeLayout[1]/android.widget.TextView[2]' % i).get_text()
        balance = self.xpath('//*[@resource-id="com.chinamworld.main:id/detail_list"]/android.widget.LinearLayout['
                             '%s]/android.widget.LinearLayout[1]/android.widget.LinearLayout['
                             '1]/android.widget.RelativeLayout[2]/android.widget.TextView[2]' % i).get_text()
        summary = self.xpath('//*[@resource-id="com.chinamworld.main:id/detail_list"]/android.widget.LinearLayout['
                             '%s]/android.widget.LinearLayout[1]/android.widget.LinearLayout['
                             '1]/android.widget.RelativeLayout[3]/android.widget.TextView[2]' % i).get_text()
        postscript = self.xpath('//*[@resource-id="com.chinamworld.main:id/detail_list"]/android.widget.LinearLayout['
                                '%s]/android.widget.LinearLayout[1]/android.widget.LinearLayout['
                                '1]/android.widget.RelativeLayout[4]/android.widget.TextView[2]' % i).get_text()
        trans_time = get_time()
        account = get_account()
        trans_type = get_trans_type()
        transaction_list.append(
            Transaction(trans_time=trans_time, trans_type=trans_type, amount=amount, balance=balance,
                        postscript=postscript, account=account, summary=summary))
        print("------------------------------")
        print(transaction_list)
        if i == 1:
            settings.bot.last_trans = Transaction(trans_time=trans_time, trans_type=trans_type, amount=amount,
                                                  balance=balance,
                                                  postscript=postscript, account=account, summary=summary)
        i = i + 1

    back_activity()
    back_activity()
    back_activity()
    return transaction_list


def post_sms(sms):
    def success():
        self(resourceId="com.chinamworld.main:id/title_right_view_container").click()
        self(resourceId="com.chinamworld.main:id/ccb_title_left_btn").click()
        if self(resourceId="com.chinamworld.main:id/totalMoney").exists(timeout=60):
            settings.bot.account.currency = self(resourceId="com.chinamworld.main:id/totalMoney").get_text()

    self(resourceId="com.chinamworld.main:id/et_code").click()
    self.send_keys(sms, clear=True)
    self(resourceId="com.chinamworld.main:id/btn_confirm").click()
    if self(text="收款账户").exists(timeout=60):
        success()
        return 0
    elif self(resourceId="com.chinamworld.main:id/native_graph_iv").exists(timeout=60):

        def put_code():

            def get_code():
                time.sleep(1)
                self(resourceId="com.chinamworld.main:id/native_graph_iv").click()
                time.sleep(1)
                info = self(resourceId="com.chinamworld.main:id/native_graph_iv").info
                x = info['bounds']['left']
                y = info['bounds']['top']
                self.screenshot("verification.jpg")
                vc = VerificationCode(x, y, 313, 165)
                return vc.image_str()

            code = get_code()
            while code == "":
                time.sleep(3)
                code = get_code()
            print(code)
            time.sleep(2)
            self(resourceId="com.chinamworld.main:id/native_graph_et").click()
            self(resourceId="com.chinamworld.main:id/default_row_two_1").click()
            self.send_keys(code, clear=True)
            time.sleep(2)
            self(resourceId="com.chinamworld.main:id/et_code").click()
            self.send_keys(settings.bot.account.payment_pwd, clear=True)

            if self(resourceId="com.chinamworld.main:id/btn_confirm").click_gone(maxretry=10, interval=1.0):
                success()
                return False
            else:
                put_code()

        put_code()
