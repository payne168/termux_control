# coding: utf8
import time
import sys
from bots.verification.verification_code import VerificationCode
from uiautomator2 import Direction

sys.path.append("..")
from models import Account, Transferee, Transaction

package = 'com.chinamworld.main'
activity = 'com.ccb.start.MainActivity'

# def connect():
#     connection = u2.connect('0.0.0.0')
#     connection = u2.connect('R3CN90724BK')
#     print(connection.info)
#     return connection

acc = Account()
trans = Transferee()


def start(self):
    # runComponent = package + '/' + activity
    self.app_start(package)
    return self.app_wait(package)  # 等待应用运行, return pid(int)


def login(self, password):
    self(resourceId="com.chinamworld.main:id/et_password").click()
    # self.send_keys("aa168168", clear=True)
    for i in password:
        self(text=i).click()
    self(resourceId="com.chinamworld.main:id/btn_confirm").click_gone(maxretry=10, interval=1.0)


def change_activity(self, page_activity):
    LoginActivity = self.wait_activity("com.ccb.framework.security.login.internal.view.LoginActivity", timeout=5)
    if LoginActivity:
        login(self, acc.login_pwd)
    return self.wait_activity(page_activity, timeout=20)


def input_form(self):
    SmartTransferMainAct = change_activity(self, "com.ccb.transfer.smarttransfer.view.SmartTransferMainAct")
    if SmartTransferMainAct:
        self(resourceId="com.chinamworld.main:id/et_cash_name").click()
        self(resourceId="com.chinamworld.main:id/et_cash_name").set_text(trans.name)
        self(resourceId="com.chinamworld.main:id/et_collection_account").click()
        self(resourceId="com.chinamworld.main:id/et_collection_account").set_text(trans.account)
        self(resourceId="com.chinamworld.main:id/tv_bank").click()
        self(resourceId="com.chinamworld.main:id/tv_bank").click()

        if self(text="热门银行").exists(timeout=20):
            bank_btn = self(resourceId="com.chinamworld.main:id/title", text=trans.bank_name)
            if bank_btn.click_gone(maxretry=20, interval=1.0):
                self(resourceId="com.chinamworld.main:id/tv_transfer_way").click()
                if self(text="实时转账").exists(timeout=20):
                    self(resourceId="com.chinamworld.main:id/bottom_selector_tv", text="实时转账").click()
                    self(resourceId="com.chinamworld.main:id/et_tran_amount").click()
                    self.send_keys(trans.amount, clear=True)
                    self.press("back")
                    self(resourceId="com.chinamworld.main:id/rl_tran_mark").click()
                    self.send_keys("今天发的1元钱", clear=True)
                    self.press("back")
                    self(resourceId="com.chinamworld.main:id/btn_right1").click()
                    if self(resourceId="com.chinamworld.main:id/dlg_right_tv").exists(timeout=20):
                        self(resourceId="com.chinamworld.main:id/dlg_right_tv").click()


def remove_float_win(self):
    if self(text="是否需要向银行卡").exists(timeout=5):
        self(resourceId="com.chinamworld.main:id/btn_cancel").click_gone(maxretry=10, interval=1.0)
    if self(resourceId="com.chinamworld.main:id/close").exists(timeout=5):
        self(resourceId="com.chinamworld.main:id/close").click_gone(maxretry=10, interval=1.0)
    return True


def build_trans_object(amount, account, name, bank_name, password, withdraw_password):
    acc.login_pwd = password
    acc.payment_pwd = withdraw_password
    trans.amount = amount
    trans.account = account
    trans.name = name
    trans.bank_name = bank_name


def transaction(self, amount, account, name, bank_name, password, withdraw_password):
    build_trans_object(amount, account, name, bank_name, password, withdraw_password)
    self.xpath(
        '//*[@resource-id="com.chinamworld.main:id/grid_function"]/android.widget.LinearLayout[1]').click()
    input_form(self)


def transfer(self, amount, account, name, bank_name, password, withdraw_password):
    # 转账
    def do_trans():
        waitRes = self.wait_activity(activity, timeout=20)
        print('waitRes %s' % waitRes)
        build_trans_object(amount, account, name, bank_name, password, withdraw_password)
        if waitRes:
            self(resourceId="com.chinamworld.main:id/main_home_smart_transfer").click()
            waitTransferHomeAct = change_activity(change_activity,
                                                  "com.ccb.transfer.transfer_home.view.TransferHomeAct")
            if waitTransferHomeAct:
                transaction(self)

    if remove_float_win(self):
        do_trans()


def inquire_balance(self, password):
    # 抓取流水
    acc.login_pwd = password

    def do_inquire():
        waitRes = self.wait_activity(activity, timeout=20)
        print('waitRes %s' % waitRes)
        if waitRes:
            transaction_history(self)
        # acc.currency = self(resourceId="com.chinamworld.main:id/totalMoney").get_text()
        # print('<---------当前余额是 %s --------->' % (currency))

    if remove_float_win(self):
        do_inquire()


def transaction_history(self):
    self(resourceId="com.chinamworld.main:id/text_item", text="账户").click()
    MyAccountMainAct = change_activity(self, "com.ccb.myaccount.view.MyAccountMainAct")

    if MyAccountMainAct:
        self(text="详情").click()
        TitledActivity = change_activity(self, "com.ccb.framework.app.TitledActivity")

        if TitledActivity:
            self(resourceId="com.chinamworld.main:id/type", text="活期储蓄").click()

            if self(text="总收入").exists(timeout=20):
                transaction_record = do_get_history(self)
                print(transaction_record)


def do_get_history(self, i=1):
    transaction_list = []
    while i < 3:
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
        transaction_list.append(Transaction(trans_time=trans_time, trans_type=trans_type, amount=amount, balance=balance,
                                            postscript=postscript, account=account, summary=summary))
        print("------------------------------")
        print(transaction_list)
        i = i + 1
    return transaction_list


def post_sms(self, sms):
    def success():
        self(resourceId="com.chinamworld.main:id/title_right_view_container").click()
        self(resourceId="com.chinamworld.main:id/ccb_title_left_btn").click()
        if self(resourceId="com.chinamworld.main:id/totalMoney").exists(timeout=20):
            acc.currency = self(resourceId="com.chinamworld.main:id/totalMoney").get_text()

    self(resourceId="com.chinamworld.main:id/et_code").click()
    self.send_keys(sms, clear=True)
    self(resourceId="com.chinamworld.main:id/btn_confirm").click()
    if self(text="收款账户").exists(timeout=20):
        success()
        return 0
    elif self(resourceId="com.chinamworld.main:id/native_graph_iv").exists(timeout=20):

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
            self.send_keys(acc.payment_pwd, clear=True)

            if self(resourceId="com.chinamworld.main:id/btn_confirm").click_gone(maxretry=10, interval=1.0):
                success()
                return 0
            else:
                put_code()

        put_code()


def stop(self):
    self.close()


def touch(self, view_text):
    self(text=view_text).click()


def click(self, x, y):
    self.click(x, y)


def screen_on(self):
    self.screen_on()
