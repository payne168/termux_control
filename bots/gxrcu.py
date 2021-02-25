# coding: utf8
import time
import sys
import requests
import settings

sys.path.append("..")
from models import Account, Transferee, Transaction
from api import transfer_status as status_api

package = 'com.nxy.mobilebank.gx'
activity = 'com.nxy.mobilebank.activity.MainActivity'

trans = Transferee()
self = settings.bot.device
already_sms = False


def start():
    self.screen_on()
    self.app_start(package)
    return self.app_wait(package)  # 等待应用运行, return pid(int)


def stop():
    self.app_stop(package)


def login():
    self(resourceId="com.nxy.mobilebank.gx:id/login_debit_et_pass").click()
    for i in settings.bot.account.login_pwd:
        time.sleep(1)
        if self(text="123").exists(timeout=20):
            if not i.isdigit():
                self(text=i).click()
            else:
                self(text="123").click()
                self(text=i).click()
        else:
            if not i.isdigit():
                self(text="ABC").click()
                self(text=i).click()
            else:
                self(text=i).click()
    self(resourceId="com.nxy.mobilebank.gx:id/login_debit_bt").click()
    self(resourceId="com.nxy.mobilebank.gx:id/login_btn").click()


def change_activity(page_activity):
    # internet_timeout()
    print("正在等待切换页面！")
    LoginActivity = self.wait_activity("com.nxy.mobilebank.login.LoginActivity", timeout=5)
    print(LoginActivity)
    if LoginActivity:
        login()

    page = self.wait_activity(page_activity, timeout=120)
    return page


def back_activity():
    print("正在执行回退页面！")
    # internet_timeout()
    print("正在执行登录页检测！")
    LoginActivity = self.wait_activity("com.ccb.framework.security.login.internal.view.LoginActivity", timeout=5)
    if LoginActivity:
        print("检测到登录页，正在为您登录！")
        login()
    else:
        print("无登录页，执行回退！")
        self.press("back")


def input_form():
    print("准备为您填充表单！")
    SmartTransferMainAct = change_activity("com.nxy.mobilebank.service.transferaccount.BankSmartTransferActivityNew")
    if SmartTransferMainAct:
        self(resourceId="com.nxy.mobilebank.gx:id/login_debit_bt").click()
        time.sleep(1)
        self(resourceId="com.nxy.mobilebank.gx:id/login_btn").click()
        time.sleep(1)
        self(resourceId="com.nxy.mobilebank.gx:id/et_payAmount").click()
        time.sleep(1)
        self.send_keys(str(trans.amount), clear=True)
        time.sleep(1)
        self(resourceId="com.nxy.mobilebank.gx:id/et_accName").click()
        time.sleep(1)
        self.send_keys(trans.holder, clear=True)
        time.sleep(1)
        self(resourceId="com.nxy.mobilebank.gx:id/et_account").click()
        time.sleep(1)
        self.send_keys(trans.account, clear=True)
        time.sleep(1)
        self(resourceId="com.nxy.mobilebank.gx:id/et_accOpenBankName").click()
        time.sleep(1)
        self(resourceId="com.nxy.mobilebank.gx:id/filter_edit").click()
        time.sleep(1)
        self.send_keys(trans.bank_name, clear=True)
        time.sleep(3)
        self(resourceId="com.nxy.mobilebank.gx:id/refresh").click()
        time.sleep(1)
        self.xpath(
            '//*[@resource-id="com.nxy.mobilebank.gx:id/lv_smart_sor"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]').click()
        time.sleep(2)
        self(resourceId="com.nxy.mobilebank.gx:id/bt_next").click()


def remove_float_win():
    return True

def do_transfer(transferee):
    if remove_float_win():
        if self(resourceId="com.nxy.mobilebank.gx:id/tv_icon_name", text="跨行转账").exists(timeout=20):
            self(resourceId="com.nxy.mobilebank.gx:id/tv_icon_name", text="跨行转账").click()
            waitTransferHomeAct = change_activity("com.ccb.transfer.transfer_home.view.TransferHomeAct")
            if waitTransferHomeAct:
                trans.order_id = transferee.order_id
                trans.amount = transferee.amount
                trans.account = transferee.account
                trans.holder = transferee.holder
                trans.bank_name = transferee.bank_name
                self.xpath(
                    '//*[@resource-id="com.chinamworld.main:id/grid_function"]/android.widget.LinearLayout[1]').click()
    input_form()


def transfer(transferee):
    # 转账
    def do_trans():
        waitRes = self.wait_activity(activity, timeout=120)
        print('waitRes %s' % waitRes)
        if waitRes:
            do_transfer(transferee)

    if remove_float_win():
        do_trans()


def transaction_history():
    return True


def do_transaction():
    return True


def do_get_history(i=1):
    return True


def success():
    if self(resourceId="com.nxy.mobilebank.gx:id/btn_back").exists(timeout=120):
        self(resourceId="com.nxy.mobilebank.gx:id/btn_back").click()
        status_api(trans.order_id, 0)


def press_resend():
    if self(resourceId="com.chinamworld.main:id/re_send").exists(timeout=30):
        self(resourceId="com.chinamworld.main:id/re_send").click()


def close_win():
    return True


def false_msg(msg="网络异常"):
    status_api(trans.order_id, 1, msg)


def internet_timeout():
    if self(resourceId="com.chinamworld.main:id/tv_dlg_consult").exists(timeout=12):
        print("正在做网络检查！")
        if self(text="QU7010.UnknownHostException").get_text():
            self(resourceId="com.chinamworld.main:id/dlg_right_tv").click()
            self.false_msg("没有网络！")
            restart_app()


def restart_app():
    def restart():
        requests.get(url="http://%s%s/start" % (settings.gateway['host'], settings.gateway['port']))

    print("---------------------------->")
    print("网络异常，系统自动关闭app！")
    print("---------------------------->")
    print("因为没有网络，正在帮您重启APP！")
    stop()
    restart()


def toast_msg(msg):
    self.toast.show(msg)


def post_sms(sms):
    if settings.post_sms_already:
        return
    if self(resourceId="com.nxy.mobilebank.gx:id/et_sms").exists(timeout=5):
        self(resourceId="com.nxy.mobilebank.gx:id/et_sms").click()
        settings.post_sms_already = True
    else:
        return
    if self(resourceId="com.nxy.mobilebank.gx:id/et_sms").exists(timeout=5):
        self(resourceId="com.nxy.mobilebank.gx:id/et_sms").click()
        self.send_keys(sms, clear=True)
        print(settings.bot.account.payment_pwd)
        self(resourceId="com.nxy.mobilebank.gx:id/et_trade_password").click()
        for i in settings.bot.account.payment_pwd:
            time.sleep(1)
            self(text=i).click()
        time.sleep(2)
        self(resourceId="com.nxy.mobilebank.gx:id/bt_confirm").click()
        success()
    else:
        status_api(trans.order_id, 1, "查询账户开户机构不成功。")


def get_code():
    return True


def post_server_code():
    return True


def post_verify_code():
    return True


def ai_verify_code():
    return True


def do_verify_code():
    return True
