# coding: utf8
import base64
import time
import sys
from bots.verification.verification_code_ccb import VerificationCodeCcb
import requests
import settings

sys.path.append("..")
from models import Account, Transferee, Transaction
from api import transaction as trans_api
from api import transfer_status as status_api
from api import verification_code as verification_code_api

package = 'com.chinamworld.main'
activity = 'com.ccb.start.MainActivity'

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
    self(resourceId="com.chinamworld.main:id/btn_confirm").click()
    if self(text="尊敬的客户，您在我行存留的身份证件即将到期，为避免影响您办理业务，请尽快到建行手机银行、网上银行或网点等渠道更新信息。").exists(timeout=5):
        self(resourceId="com.chinamworld.main:id/btn_cancel").click()


def change_activity(page_activity):
    # internet_timeout()
    print("正在等待切换页面！")
    LoginActivity = self.wait_activity("com.ccb.framework.security.login.internal.view.LoginActivity", timeout=5)
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
    SmartTransferMainAct = change_activity("com.ccb.transfer.smarttransfer.view.SmartTransferMainAct")
    if SmartTransferMainAct:
        self(resourceId="com.chinamworld.main:id/et_cash_name").click()
        self(resourceId="com.chinamworld.main:id/et_cash_name").set_text(trans.holder)
        self(resourceId="com.chinamworld.main:id/et_collection_account").click()
        self(resourceId="com.chinamworld.main:id/et_collection_account").set_text(trans.account)
        self.press("back")
        self(resourceId="com.chinamworld.main:id/tv_transfer_way").click()
        if self(text="实时转账").exists(timeout=120):
            self(resourceId="com.chinamworld.main:id/bottom_selector_tv", text="实时转账").click()
            if self(resourceId="com.chinamworld.main:id/et_tran_amount").exists(timeout=10):
                self(resourceId="com.chinamworld.main:id/et_tran_amount").click()
            self.send_keys(str(trans.amount), clear=True)
            self.press("back")
            # 附言
            # self(resourceId="com.chinamworld.main:id/rl_tran_mark").click()
            # self.send_keys("今天发的1元钱", clear=True)
            # self.press("back")
            self(resourceId="com.chinamworld.main:id/tv_bank").click()
            if self(text="热门银行").exists(timeout=120):
                bank_btn = self(resourceId="com.chinamworld.main:id/title", text=trans.bank_name)
                if bank_btn.click_gone(maxretry=120, interval=1.0):
                    self(resourceId="com.chinamworld.main:id/btn_right1").click()
                    if self(resourceId="com.chinamworld.main:id/dlg_right_tv").exists(timeout=10):
                        self(resourceId="com.chinamworld.main:id/dlg_right_tv").click()
                        if self(resourceId="com.chinamworld.main:id/et_code").exists(timeout=5):
                            print("等待验证码")
                        else:
                            self(resourceId="com.chinamworld.main:id/btn_right1").click()

                    elif self(resourceId="com.chinamworld.main:id/tv_dlg_content").exists(timeout=10):
                        self.xpath('//android.widget.FrameLayout[1]/android.widget.LinearLayout['
                                   '1]/android.widget.FrameLayout[1]/android.widget.LinearLayout['
                                   '1]/android.widget.LinearLayout[1]').click()
                        time.sleep(2)
                        back_activity()
                        back_activity()
                        print("go back ----->")
                        status_api(trans.order_id, 1, "查询账户开户机构不成功。")


def remove_float_win():
    if self(resourceId="com.chinamworld.main:id/close").exists(timeout=5):
        self(resourceId="com.chinamworld.main:id/close").click_gone(maxretry=10, interval=1.0)
    elif self(text="是否需要向银行卡").exists(timeout=5):
        self(resourceId="com.chinamworld.main:id/btn_cancel").click_gone(maxretry=10, interval=1.0)
    else:
        return True


def do_transfer(transferee):
    if remove_float_win():
        if self(resourceId="com.chinamworld.main:id/main_home_smart_transfer").exists(timeout=20):
            self(resourceId="com.chinamworld.main:id/main_home_smart_transfer").click()
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
    # 抓取流水
    def do_inquire():
        waitRes = self.wait_activity(activity, timeout=120)
        print('waitRes %s' % waitRes)
        if waitRes:
            transaction_history()

    print("ready")
    if remove_float_win():
        print("remove win done")
        do_inquire()


def do_transaction():
    if remove_float_win():
        if self(text="账户").exists(timeout=5):
            self(text="账户").click()
            MyAccountMainAct = change_activity("com.ccb.myaccount.view.MyAccountMainAct")
            if MyAccountMainAct:
                if self(text="详情").exists(timeout=10):
                    self(text="详情").click()

                    TitledActivity = change_activity("com.ccb.framework.app.TitledActivity")

                    if TitledActivity:
                        if self(resourceId="com.chinamworld.main:id/type", text="活期储蓄").exists(timeout=120):
                            self(resourceId="com.chinamworld.main:id/type", text="活期储蓄").click()

                            if self(text="总收入").exists(timeout=120):
                                transaction_record = do_get_history()
                                print(transaction_record)
                else:
                    back_activity()
                    do_transaction()


def do_get_history(i=1):
    print("正在为您抓取流水记录！")
    transaction_list = []
    while i < 2:
        def get_trans_type():
            trans_type_txt = self.xpath(
                '//*[@resource-id="com.chinamworld.main:id/detail_list"]/android.widget.LinearLayout['
                '%s]/android.widget.LinearLayout[1]/android.widget.LinearLayout['
                '1]/android.widget.RelativeLayout[1]/android.widget.TextView[1]' % i).get_text()
            if trans_type_txt.strip() == "支出":
                return 0
            elif trans_type_txt.strip() == "收入":
                return 1

        def get_time():
            if i == 1:
                time_txt = self.xpath(
                    '//*[@resource-id="com.chinamworld.main:id/more"]/android.widget.RelativeLayout['
                    '1]/android.widget.TextView[2]').get_text()
                array = time.strptime(time_txt, u"%Y%m%d %H:%M:%S")
                return time.strftime("%Y-%m-%d %H:%M:%S", array)
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

        time.sleep(20)
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
                        postscript=postscript, account=account.split(" ")[1], summary=summary))
        print("------------------------------")
        trans_api(settings.bot.account.alias, balance, transaction_list)
        print("------------------------------")
        i = i + 1

    back_activity()
    back_activity()
    back_activity()
    return transaction_list


def success():
    back_activity()
    self(resourceId="com.chinamworld.main:id/ccb_title_left_btn").click()
    if self(resourceId="com.chinamworld.main:id/totalMoney").exists(timeout=120):
        settings.bot.account.currency = self(resourceId="com.chinamworld.main:id/totalMoney").get_text()


def press_resend():
    if self(resourceId="com.chinamworld.main:id/re_send").exists(timeout=30):
        self(resourceId="com.chinamworld.main:id/re_send").click()


def close_win():
    if self(resourceId="com.chinamworld.main:id/iv_close").exists(timeout=12):
        self(resourceId="com.chinamworld.main:id/iv_close").click()


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


already_sms = False


def post_sms(sms):
    if settings.post_sms_already:
        return
    if self(resourceId="com.chinamworld.main:id/et_code").exists(timeout=5):
        self(resourceId="com.chinamworld.main:id/et_code").click()
        settings.post_sms_already = True
    else:
        return
    self.send_keys(sms, clear=True)
    self(resourceId="com.chinamworld.main:id/btn_confirm").click()
    print("支付最后一步")
    if self(resourceId="com.chinamworld.main:id/et_code").exists(timeout=5):
        self(resourceId="com.chinamworld.main:id/default_row_two_1").click()
        time.sleep(1)
        self(resourceId="com.chinamworld.main:id/et_code").click()
        print("settings.bot.account.payment_pwd")
        print(settings.bot.account.payment_pwd)
        self.send_keys(settings.bot.account.payment_pwd, clear=True)
        time.sleep(5)
    post_server_code()
    # print(self(resourceId="com.chinamworld.main:id/native_graph_iv").exists(timeout=5))
    # if self(resourceId="com.chinamworld.main:id/native_graph_iv").exists(timeout=20):
    # def put_code():
    #     if self(resourceId="com.chinamworld.main:id/et_code").exists(timeout=5):
    #         self(resourceId="com.chinamworld.main:id/et_code").click()
    #         print("settings.bot.account.payment_pwd")
    #         print(settings.bot.account.payment_pwd)
    #         self.send_keys(settings.bot.account.payment_pwd, clear=True)
    #         time.sleep(5)
    #
    #     def get_code():
    #         if self(resourceId="com.chinamworld.main:id/native_graph_iv").exists(timeout=20):
    #             self(resourceId="com.chinamworld.main:id/native_graph_iv").click()
    #             info = self(resourceId="com.chinamworld.main:id/native_graph_iv").info
    #             x = info['bounds']['left']
    #             y = info['bounds']['top']
    #             img = "verification%s.jpg"
    #             self.screenshot(img)
    #             vc = VerificationCodeCcb(x, y, 313, 165, img)
    #
    #             return vc.image_str()
    #
    #     code = get_code()
    #     while code == "":
    #         time.sleep(3)
    #         # settings.count += 1
    #         code = get_code()
    #     print(code)
    #
    #     self(resourceId="com.chinamworld.main:id/native_graph_et").click()
    #     self(resourceId="com.chinamworld.main:id/default_row_two_1").click()
    #     self.send_keys(code, clear=True)
    #     # time.sleep(5)
    #
    #     if self(resourceId="com.chinamworld.main:id/btn_confirm").click_gone(maxretry=5, interval=1.0):
    #         # time.sleep(2)
    #         success()
    #     else:
    #         put_code()
    #
    # put_code()

    # elif self(text="收款账户").exists(timeout=10):
    #     status_api(trans.order_id, 0)
    #     time.sleep(20)
    #     success()
    #     print("您已经转账成功了！")
    #     # do_transaction()
    #     settings.bot.post_sms_already = False
    #
    # else:
    #     false_msg("短信超时")
    #     print("您已经转账超时了！正在为您返回首页！")
    #     close_win()
    #     back_activity()
    #     back_activity()
    #     settings.bot.post_sms_already = False


def post_server_code():
    if self(resourceId="com.chinamworld.main:id/native_graph_iv").exists(timeout=20):
        self(resourceId="com.chinamworld.main:id/native_graph_iv").click()
        print("开始识别验证码了")
        info = self(resourceId="com.chinamworld.main:id/native_graph_iv").info
        x = info['bounds']['left']
        y = info['bounds']['top']
        img = "verification.jpg"
        self.screenshot(img)
        vc = VerificationCodeCcb(x, y, 313, 165, img)
        vc.image_str()
        # img_file = {'images': }

        with open(img, "rb") as image_file:
            image_str = image_file.read()
            encoded_string = base64.b64encode(image_str).decode("ascii")
            print("1--------------------------1--------------->")
            print(image_str)
            print(encoded_string)
            res = verification_code_api(settings.bot.serial_no, encoded_string)
            print("res----------->%s" % res)

    elif self(text="收款账户").exists(timeout=10):
        status_api(trans.order_id, 0)
        time.sleep(20)
        success()
        print("您已经转账成功了！")
        # do_transaction()
        settings.bot.post_sms_already = False

    else:
        false_msg("短信超时")
        print("您已经转账超时了！正在为您返回首页！")
        close_win()
        back_activity()
        back_activity()
        settings.bot.post_sms_already = False


def post_verify_code(code):
    if self(resourceId="com.chinamworld.main:id/et_code").exists(timeout=5):
        self(resourceId="com.chinamworld.main:id/native_graph_et").click()
        self(resourceId="com.chinamworld.main:id/default_row_two_1").click()
        self.send_keys(code, clear=True)
        time.sleep(5)

        if self(resourceId="com.chinamworld.main:id/btn_confirm").click_gone(maxretry=5, interval=1.0):
            success()
        else:
            post_server_code()
