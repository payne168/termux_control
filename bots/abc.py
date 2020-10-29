# coding: utf8
import time
import sys
import requests
import settings

sys.path.append("..")
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
    self(text="请输入登录密码").click()
    self.send_keys("hb741963", clear=True)
    # for i in settings.bot.account.login_pwd:
    #     time.sleep(1)
    #     self(text=i).click()
    self.xpath('//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.ViewGroup['
               '2]/android.view.ViewGroup[1]/android.view.ViewGroup[3]/android.view.ViewGroup['
               '1]/android.widget.Button[1]').click()


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
    LoginActivity = self.wait_activity(".MainActivity", timeout=5)
    if LoginActivity:
        print("检测到登录页，正在为您登录！")
        login()
    else:
        print("无登录页，执行回退！")
        self.press("back")


def input_form():
    print("准备为您填充表单！")
    self(text="请输入名称").click()
    self.send_keys(trans.holder, clear=True)
    self(text="请输入账号").click()
    self.send_keys(trans.account, clear=True)
    self.xpath('//android.webkit.WebView/android.view.View[7]/android.widget.Image[1]').click()
    self(description=trans.bank_name).click()
    self(description="请输入转账金额").click()
    amount = trans.amount.split()
    for i in amount:
        self(description=i).click()
    self(description="2BsHuD1UCBrbmAAAAAElFTkSuQmCC").click()
    self(description="下一步").click()
    self(description="确认").click()
    status_api(trans.order_id, 1, "查询账户开户机构不成功。")
    back_activity()
    back_activity()
    back_activity()
    back_activity()


# def remove_float_win():
#     if self(resourceId="com.chinamworld.main:id/close").exists(timeout=5):
#         self(resourceId="com.chinamworld.main:id/close").click_gone(maxretry=10, interval=1.0)
#     elif self(text="是否需要向银行卡").exists(timeout=5):
#         self(resourceId="com.chinamworld.main:id/btn_cancel").click_gone(maxretry=10, interval=1.0)
#     else:
#         return True


def do_transfer(transferee):
    # if remove_float_win():
    self(resourceId="inputBox").click()
    self.send_keys("转账", clear=True)
    time.sleep(2)
    self(description="转账").click()
    waitTransferHomeAct = change_activity("com.alipay.mobile.nebulacore.ui.H5Activity")
    if waitTransferHomeAct:
        trans.order_id = transferee.order_id
        trans.amount = transferee.amount
        trans.account = transferee.account
        trans.holder = transferee.holder
        trans.bank_name = transferee.bank_name
        self.xpath('//android.webkit.WebView/android.view.View[1]/android.view.View[1]').click()
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
    self.xpath('//android.widget.ListView/android.view.View[1]').click()


def do_get_history(i=1):
    print("正在为您抓取流水记录！")
    transaction_list = []
    for el in self.xpath('//android.webkit.WebView/android.view.View[3]/android.view.View').all():
        print(el.elem)  # 输出lxml解析出来的Node
        print(el.description)
    # transaction_list.append(
    #     Transaction(trans_time=trans_time, trans_type=trans_type, amount=amount, balance=balance,
    #                 postscript=postscript, account=account.split(" ")[1], summary=summary))
    print("------------------------------")
    # trans_api(settings.bot.account.alias, "0", transaction_list)
    print("------------------------------")
    # back_activity()
    # back_activity()
    # back_activity()
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
    # if self(resourceId="com.chinamworld.main:id/et_code").exists(timeout=5):
    #     self(resourceId="com.chinamworld.main:id/et_code").click()
    # else:
    #     return False
    # self.send_keys(sms, clear=True)
    # self(resourceId="com.chinamworld.main:id/btn_confirm").click()
    # if self(text="收款账户").exists(timeout=120):
    #     status_api(trans.order_id, 0)
    #     time.sleep(10)
    #     success()
    #     print("您已经转账成功了！")
    #     do_transaction()
    #     return False
    # else:
    #     false_msg("短信超时")
    #     print("您已经转账超时了！正在为您返回首页！")
    #     close_win()
    #     back_activity()
    #     back_activity()
    return False
    # elif self(resourceId="com.chinamworld.main:id/native_graph_iv").exists(timeout=60):
    #
    #     def put_code():
    #
    #         def get_code():
    #             time.sleep(1)
    #             self(resourceId="com.chinamworld.main:id/native_graph_iv").click()
    #             time.sleep(1)
    #             info = self(resourceId="com.chinamworld.main:id/native_graph_iv").info
    #             x = info['bounds']['left']
    #             y = info['bounds']['top']
    #             self.screenshot("verification.jpg")
    #             vc = VerificationCode(x, y, 313, 165)
    #             return vc.image_str()
    #
    #         code = get_code()
    #         while code == "":
    #             time.sleep(3)
    #             code = get_code()
    #         print(code)
    #         time.sleep(2)
    #         self(resourceId="com.chinamworld.main:id/native_graph_et").click()
    #         self(resourceId="com.chinamworld.main:id/default_row_two_1").click()
    #         self.send_keys(code, clear=True)
    #         time.sleep(2)
    #         self(resourceId="com.chinamworld.main:id/et_code").click()
    #         self.send_keys(settings.bot.account.payment_pwd, clear=True)
    #
    #         if self(resourceId="com.chinamworld.main:id/btn_confirm").click_gone(maxretry=10, interval=1.0):
    #             success()
    #             return False
    #         else:
    #             put_code()

    # put_code()
