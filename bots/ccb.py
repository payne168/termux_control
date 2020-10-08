# coding: utf8
import time
import threading
import uiautomator2 as u2

package = 'com.chinamworld.main'
activity = 'com.ccb.start.MainActivity'


# def connect():
#     connection = u2.connect('0.0.0.0')
#     connection = u2.connect('R3CN90724BK')
#     print(connection.info)
#     return connection

def start(self):
    runComponent = package + '/' + activity
    self.app_start(package)
    return self.app_wait(package)  # 等待应用运行, return pid(int)


def transfer(self, amount, transform_account, bank_kind, password, withdraw_password):
    # 转账
    waitRes = self.wait_activity(activity, timeout=20)
    print('waitRes %s' % waitRes)
    if waitRes:
        self(resourceId="com.chinamworld.main:id/close").click_exists(timeout=3.0)
        self(resourceId="com.chinamworld.main:id/main_home_smart_transfer").click()
        waitTransferHomeAct = self.wait_activity("com.ccb.transfer.transfer_home.view.TransferHomeAct", timeout=20)
        if waitTransferHomeAct:
            self.xpath(
                '//*[@resource-id="com.chinamworld.main:id/grid_function"]/android.widget.LinearLayout[1]').click()
            LoginActivity = self.wait_activity("com.ccb.framework.security.login.internal.view.LoginActivity",
                                               timeout=20)
            if LoginActivity:
                self(resourceId="com.chinamworld.main:id/et_password").click()
                self(text="h").click()
                self(text="b").click()
                self(text="7").click()
                self(text="4").click()
                self(text="1").click()
                self(text="9").click()
                self(text="6").click()
                self(text="3").click()
                self(resourceId="com.chinamworld.main:id/btn_confirm").click_gone(maxretry=10, interval=1.0)
                SmartTransferMainAct = self.wait_activity("com.ccb.transfer.smarttransfer.view.SmartTransferMainAct",
                                                          timeout=20)
                if SmartTransferMainAct:
                    self(resourceId="com.chinamworld.main:id/et_cash_name").click()
                    self(resourceId="com.chinamworld.main:id/et_cash_name").set_text("赵婷")
                    self(resourceId="com.chinamworld.main:id/et_collection_account").click()
                    self(resourceId="com.chinamworld.main:id/et_collection_account").set_text("6217996900059953209")
                    time.sleep(10.0)
                    self(resourceId="com.chinamworld.main:id/tv_bank").click()
                    self(resourceId="com.chinamworld.main:id/tv_bank").click()
                    time.sleep(20.0)
                    self.xpath(
                        '//android.widget.GridView/android.widget.LinearLayout[15]/android.widget.ImageView[1]').click()
                    time.sleep(10.0)
                    self(resourceId="com.chinamworld.main:id/tv_transfer_way").click()
                    time.sleep(10.0)
                    self(resourceId="com.chinamworld.main:id/bottom_selector_tv", text="实时转账").click()
                    time.sleep(10.0)
                    self(resourceId="com.chinamworld.main:id/et_tran_amount").click()
                    time.sleep(10.0)
                    self(resourceId="com.chinamworld.main:id/digit_row_one_1").click()
                    self(resourceId="com.chinamworld.main:id/ct_submit").click()
                    time.sleep(10.0)
                    self(resourceId="com.chinamworld.main:id/rl_tran_mark").click()
                    self.send_keys("今天发的1元钱", clear=True)
                    self.press("back")
                    time.sleep(5.0)
                    self(resourceId="com.chinamworld.main:id/btn_right1").click()
                    # time.sleep(10.0)
                    ## d(resourceId="com.chinamworld.main:id/native_graph_et").click() 支付验证码页
                    # self(resourceId="com.chinamworld.main:id/native_graph_iv").click()
                    # self.send_keys("741963", clear=True)
                    # self(resourceId="com.chinamworld.main:id/et_code").click()
                    # self.send_keys("7q8x", clear=True)
                    # self(resourceId="com.chinamworld.main:id/btn_confirm").click()
                    # 支付
                    # self(resourceId="com.chinamworld.main:id/btn_right1").click()


def inquire_balance(self, password):
    # 查询余额
    waitRes = self.wait_activity(activity, timeout=20)
    print('waitRes %s' % waitRes)
    if waitRes:
        self(resourceId="com.chinamworld.main:id/btn_query").click()
        time.sleep(35.0)
        self.click(0.5, 0.749)
        self(text="h").click()
        self(text="b").click()
        self(text="7").click()
        self(text="4").click()
        self(text="1").click()
        self(text="9").click()
        self(text="6").click()
        self(text="3").click()
        self(resourceId="com.chinamworld.main:id/btn_confirm").click_gone(maxretry=10, interval=1.0)
        time.sleep(35.0)
        currency = self(resourceId="com.chinamworld.main:id/totalMoney").get_text()
        print('<---------当前余额是 %s --------->' % (currency))


def post_sms(self, sms):
    time.sleep(10.0)
    self(resourceId="com.chinamworld.main:id/et_code").click()
    self.send_keys(sms, clear=True)
    # self(resourceId="com.chinamworld.main:id/btn_confirm").click()
    return 0


def stop(self):
    self.close()


def touch(self, view_text):
    self(text=view_text).click()


def click(self, x, y):
    self.click(x, y)


def screen_on(self):
    self.screen_on()
