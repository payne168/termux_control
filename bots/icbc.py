# coding: utf8
import json
import time
import sys
import requests
from bots.verification.verification_code_icbc import VerificationCodeIcbc

sys.path.append("..")
import settings
from models import Account, Transferee, Transaction
from api import transaction as trans_api
from api import transfer_status as status_api

package = 'com.icbc'
activity = '.activity.main.MainActivity'

trans = Transferee()
self = settings.bot.device


def start():
    self.screen_on()
    self.app_start(package)
    return self.app_wait(package)  # 等待应用运行, return pid(int)


def stop():
    self.app_stop(package)


def login():
    if self(resourceId="com.icbc:id/login_password").exists(timeout=20):
        self(resourceId="com.icbc:id/login_password").click()
        start_info = self.xpath('//android.widget.RelativeLayout[1]/android.view.View[7]').info
        x = start_info['bounds']['left']
        y = start_info['bounds']['top']
        end_info = self.xpath('//android.widget.RelativeLayout[1]/android.view.View[16]').info
        width = int(start_info['bounds']['left']) + int(end_info['bounds']['right'])
        height = int(start_info['bounds']['bottom']) - int(start_info['bounds']['top'])
        img = "verification.jpg"
        self.screenshot(img)
        vc = VerificationCodeIcbc(x, y, width, height, img)
        code = list(str(vc.image_str()))
        print(code)
        count = 7
        switcher = {}
        for i in code:
            switcher[i] = count
            count += 1
        letters = list("qwertyuiopasdfghjklzxcvbnm")
        for letter in letters:
            if count == 37:
                count += 1
            switcher[letter] = count
            count += 1
        print(switcher)
        for press in settings.bot.account.login_pwd:
            if press.isupper():
                self.xpath(
                    '//android.widget.RelativeLayout[1]/android.view.View[37]').click()
                self.xpath(
                    '//android.widget.RelativeLayout[1]/android.view.View[%s]' % switcher.get(press.lower(),
                                                                                              "Invalid key")).click()
                self.xpath(
                    '//android.widget.RelativeLayout[1]/android.view.View[37]').click()
            else:
                self.xpath(
                    '//android.widget.RelativeLayout[1]/android.view.View[%s]' % switcher.get(press, "Invalid key")).click()
        self.xpath(
            '//*[@resource-id="com.icbc:id/movefragment"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[2]').click()
        time.sleep(25)
        if self(resourceId="MyDiv").exists(timeout=10):
            self.press("back")


def change_activity(page_activity):
    # internet_timeout()
    print("正在等待切换页面！")
    LoginActivity = self.wait_activity(".component.templatelogin.TemplateLoginActivity", timeout=5)
    print(LoginActivity)
    if LoginActivity:
        login()

    page = self.wait_activity(page_activity, timeout=120)
    return page


def back_activity():
    print("正在执行回退页面！")
    # internet_timeout()
    print("正在执行登录页检测！")
    time.sleep(2)
    self.press("back")
    # LoginActivity = self.wait_activity(".MainActivity", timeout=5)
    # if LoginActivity:
    #     print("检测到登录页，正在为您登录！")
    #     login()
    # else:
    #     print("无登录页，执行回退！")
    #     self.press("back")


def put_code():
    return True


def input_form():
    print("准备为您填充表单！")
    if self(resourceId="com.icbc:id/icon_txt", text="转账汇款").exists(timeout=20):
        self(resourceId="com.icbc:id/icon_txt", text="转账汇款").click()
        if self(resourceId="ebdp-pop-ad-fork2").exists(timeout=10):
            self(resourceId="ebdp-pop-ad-fork2").click()
        self.xpath(
            '//*[@resource-id="abs_pos_1"]/android.view.View[1]/android.view.View[2]/android.view.View['
            '1]/android.widget.TextView[1]').click()
        if self(resourceId="accountname").exists(timeout=20):
            time.sleep(3)
            self(resourceId="accountname").click()
            self(resourceId="accountname", focused=True).set_text(trans.holder)
            time.sleep(3)
            self(resourceId="cardnum").click()
            self(resourceId="cardnum", focused=True).set_text(trans.account)
            time.sleep(3)
            self(resourceId="clearBtn_parent").click()
            time.sleep(3)
            self.send_keys(trans.amount, clear=True)
            # for i in trans.amount:
            #     self(text=i).click()
            # self.press("back")
            self(text="下一步").click()
            time.sleep(3)
            switcher = {
                0: [0.498, 0.953],
                1: [0.168, 0.765],
                2: [0.498, 0.764],
                3: [0.828, 0.763],
                4: [0.166, 0.829],
                5: [0.494, 0.827],
                6: [0.836, 0.825],
                7: [0.164, 0.89],
                8: [0.5, 0.889],
                9: [0.832, 0.89],
            }
            passwd = list(settings.bot.account.payment_pwd)
            for letter in passwd:
                btn_xy = switcher.get(int(letter), "Invalid key")
                self.click(btn_xy[0], btn_xy[1])
            if self(text="款项已经汇入收款人账户。").exists(timeout=30):
                print("您已经转账成功了！")
                status_api(trans.order_id, 0)
                back_activity()
                back_activity()
                return True
            else:
                return False


def remove_float_win():
    return True


def do_transfer(transferee):
    # if remove_float_win():
    print(self(resourceId="com.icbc:id/tv_remit_bankcard_login").exists(timeout=10))
    if self(resourceId="com.icbc:id/tv_remit_bankcard_login").exists(timeout=10):
        self(resourceId="com.icbc:id/tv_remit_bankcard_login").click()
        login()
        trans.order_id = transferee.order_id
        trans.amount = transferee.amount
        trans.account = transferee.account
        trans.holder = transferee.holder
        trans.bank_name = transferee.bank_name
        input_form()


def transfer(transferee):
    # 转账
    def do_trans():
        waitRes = self.wait_activity(activity, timeout=120)
        print('waitRes %s' % waitRes)
        if waitRes:
            do_transfer(transferee)

    # if remove_float_win():
    do_trans()
    return True


def transaction_history():
    # 抓取流水
    def do_inquire():
        waitRes = self.wait_activity(activity, timeout=120)
        print('waitRes %s' % waitRes)
        if waitRes:
            transaction_history()

    # print("ready")
    # if remove_float_win():
    #     print("remove win done")
    do_inquire()


def do_transaction():
    self(resourceId="com.android.bankabc:id/rl_top_menu").click()
    login()
    self.xpath('//android.widget.ListView/android.view.View[1]').click()
    do_get_history()


def do_get_history():
    print("正在为您抓取流水记录！")
    transaction_list = []
    time.sleep(10)
    last = self.xpath('//android.webkit.WebView/android.view.View[4]/android.view.View').all()
    trans_time = ""
    trans_type = ""
    amount = ""
    balance = ""
    postscript = ""
    summary = ""
    account = ""
    for el in last:
        if el.attrib['index'] == "1":
            print("amount:", el.attrib['content-desc'])
            amount = el.attrib['content-desc'].split("交易金额")[1]

        if el.attrib['index'] == "3":
            print("time:", el.attrib['content-desc'])
            trans_time = el.attrib['content-desc']

        if el.attrib['index'] == "10":
            print("summary:", el.attrib['content-desc'])
            if el.attrib['content-desc'].strip() == "转账":
                trans_type = 0
            else:
                trans_type = 1

        if el.attrib['index'] == "12":
            print("account:", el.attrib['content-desc'])
            account = el.attrib['content-desc']

        if el.attrib['index'] == "6":
            print("summary:", el.attrib['content-desc'])
            summary = el.attrib['content-desc']

        if el.attrib['index'] == "27":
            print("postscript:", el.attrib['content-desc'])
            postscript = el.attrib['content-desc']

        if el.attrib['index'] == "24":
            print("balance:", el.attrib['content-desc'])
            balance = el.attrib['content-desc']

    transaction_list.append(
        Transaction(trans_time=trans_time, trans_type=trans_type, amount=amount, balance=balance,
                    postscript=postscript, account=account, summary=summary))
    print("------------------------------")
    trans_api(settings.bot.account.alias, "0", transaction_list)
    print("------------------------------")
    back_activity()
    back_activity()
    return transaction_list


# def success():
#     self(resourceId="com.chinamworld.main:id/title_right_view_container").click()
#     self(resourceId="com.chinamworld.main:id/ccb_title_left_btn").click()
#     if self(resourceId="com.chinamworld.main:id/totalMoney").exists(timeout=120):
#         settings.bot.account.currency = self(resourceId="com.chinamworld.main:id/totalMoney").get_text()
#
#
# def press_resend():
#     if self(resourceId="com.chinamworld.main:id/re_send").exists(timeout=30):
#         self(resourceId="com.chinamworld.main:id/re_send").click()
#
#
# def close_win():
#     if self(resourceId="com.chinamworld.main:id/iv_close").exists(timeout=12):
#         self(resourceId="com.chinamworld.main:id/iv_close").click()


def false_msg(msg="网络异常"):
    status_api(trans.order_id, 1, msg)


# def internet_timeout():
#     if self(resourceId="com.chinamworld.main:id/tv_dlg_consult").exists(timeout=12):
#         print("正在做网络检查！")
#         if self(text="QU7010.UnknownHostException").get_text():
#             self(resourceId="com.chinamworld.main:id/dlg_right_tv").click()
#             self.false_msg("没有网络！")
#             restart_app()


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
    return False

# if __name__ == '__main__':
# t = Transferee("2232e", "1", "6217003360014105927", "张家将", "abc")
# account = Account(alias="2232e", login_name="1141235413", login_pwd="aa168168",
#                   payment_pwd="168168")
# settings.bot = Bot(serial_no="RR8M90JGAXR", bank="ABC", account="6228413164520093275")
# self = settings.bot.device = u2.connect('RR8M90JGAXR')
# start()
# transfer(t)
# os.popen("rm ui.xml")
# xml = self.dump_hierarchy()
# file = open("ui.xml", "a")
# file.write(xml)
