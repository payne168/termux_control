# coding: utf8
import json
import time
import sys
import requests
from bots.verification.verification_code_abc import VerificationCodeAbc

sys.path.append("..")
import settings
from models import Account, Transferee, Transaction
from api import transaction as trans_api
from api import transfer_status as status_api

package = 'com.android.bankabc'
activity = '.homepage.HomeActivity'

trans = Transferee()
self = settings.bot.device


def start():
    self.screen_on()
    self.app_start(package)
    return self.app_wait(package)  # 等待应用运行, return pid(int)


def stop():
    self.app_stop(package)


def login():
    if self(text="请输入登录密码").exists(timeout=20):
        self(text="请输入登录密码").click()
        self(text="请输入登录密码", focused=True).set_text(settings.bot.account.login_pwd)
        # for i in settings.bot.account.login_pwd:
        #     time.sleep(1)
        #     self(text=i).click()
        self.xpath('//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.ViewGroup['
                   '2]/android.view.ViewGroup[1]/android.view.ViewGroup[3]/android.view.ViewGroup['
                   '1]/android.widget.Button[1]').click()
        time.sleep(15)


def change_activity(page_activity):
    # internet_timeout()
    print("正在等待切换页面！")
    LoginActivity = self.wait_activity(".MainActivity", timeout=5)
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
    # y = None
    # width = 0
    self(description="下一步").click()
    if self(description="确定").exists(timeout=10):
        self(description="确定").click()
    self(description="确认").click()
    if self(text="8位密码").exists(timeout=50):
        u_key_pwd = "aa168168"
        self(text="a").click()
        self.send_keys(u_key_pwd, clear=True)
        time.sleep(5)
        # self(text="123").click()
        # for key in u_key_pwd:
        #     time.sleep(1)
        #     self(text=key).click()
        # self.send_keys("aa168168", clear=True)
        self(text="确定").click()
        print("您已经转账成功了！")
        status_api(trans.order_id, 0)
        res = requests.post(url=settings.pc_url + '/press', json=settings.presser)
        body = json.loads(res.text)
        if body["code"] == 0:
            if self(description="转账已受理").exists(timeout=180):
                print("您已经转账成功了！")
                status_api(trans.order_id, 0)
        back_activity()
        back_activity()
        back_activity()
        back_activity()

    else:
        button_height = 179
        # self(description="下一步").click()
        # self(description="确认").click()
        time.sleep(5)
        info = self(resourceId="CFCA_KEYBOARD_0").info
        print("-------------------------------->")
        print(info)
        x = info['bounds']['left']
        y = info['bounds']['top']
        width = int(info['bounds']['right'])
        height = button_height * 4

        def get_code():
            img = "verification%s.jpg" % settings.count
            self.screenshot(img)
            vc = VerificationCodeAbc(x, y, width, height, img)
            code = list(str(vc.image_str()))
            passwd = list(settings.bot.account.payment_pwd)
            print("<----------------------keyboard_arr passwd_arr-------------------------->")
            print(code)
            print(passwd)
            settings.count += 1
            print(settings.count)
            # for i in passwd:
            #     print("i", i)
            #     for j in code:
            #         print("j", j)
            #         if i == j:
            #             print("match", j)
            #             key_inx = code.index(j)

            # switcher = {
            #     0: [0.162, 0.76],
            #     1: [0.494, 0.758],
            #     2: [0.842, 0.766],
            #     3: [0.168, 0.827],
            #     4: [0.494, 0.825],
            #     5: [0.834, 0.825],
            #     6: [0.168, 0.884],
            #     7: [0.498, 0.893],
            #     8: [0.824, 0.89],
            #     9: [0.49, 0.949],
            # }
            # jxy = switcher.get(key_inx, "Invalid key")
            # time.sleep(1)
            # print("<----------------------jx jy-------------------------->")
            # print(jxy[0])
            # print(jxy[1])
            # self.click(jxy[0], jxy[1])

        get_code()
        if self(resourceId="btn_cancel").exists(timeout=5):
            self(resourceId="btn_cancel").click()
            # put_code()
            get_code()
        # elif self(resourceId="com.alipay.mobile.antui:id/message").exists(timeout=5):
        #     self(resourceId="com.alipay.mobile.antui:id/ensure").click()
        #     get_code()
        else:
            print("您已经转账成功了！")
            status_api(trans.order_id, 0)
            do_transaction()


def input_form():
    print("准备为您填充表单！")
    time.sleep(5)
    if self(text="请输入名称").exists(timeout=20):
        self(text="请输入名称").click()
        self.send_keys(trans.holder, clear=True)
        self(text="请输入账号").click()
        self.send_keys(trans.account, clear=True)
        self.xpath('//android.webkit.WebView/android.view.View[8]/android.widget.Image[1]').click()
        time.sleep(5)
        # self(description="收款银行").click()
        # print(trans.bank_name)
        # time.sleep(5)
        # self(description=trans.bank_name).click()
        self(description="请输入转账金额").click()
        for i in trans.amount:
            time.sleep(1)
            self(description=i).click()
        self(description="2BsHuD1UCBrbmAAAAAElFTkSuQmCC").click()
        put_code()

    # status_api(trans.order_id, 1, "查询账户开户机构不成功。")
    # back_activity()
    # back_activity()
    # back_activity()
    # back_activity()


def remove_float_win():
    return True


def do_transfer(transferee):
    # if remove_float_win():
    print(self(resourceId="com.android.bankabc:id/scrolltv").exists(timeout=10))
    if self(resourceId="com.android.bankabc:id/scrolltv").exists(timeout=10):
        self(resourceId="com.android.bankabc:id/scrolltv").click()
        time.sleep(5)
        self(resourceId="inputBox").click()
        self(resourceId="inputBox", focused=True).set_text("转账")
        # self.send_keys("转账", clear=True)
        time.sleep(10)
        print("come in")
        self(description="转账").click()
        waitTransferHomeAct = change_activity("com.alipay.mobile.nebulacore.ui.H5Activity")
        if waitTransferHomeAct:
            trans.order_id = transferee.order_id
            trans.amount = transferee.amount
            trans.account = transferee.account
            trans.holder = transferee.holder
            trans.bank_name = transferee.bank_name
            self.xpath('//android.webkit.WebView/android.view.View[1]/android.view.View[1]').click()
            login()
        return input_form()


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
