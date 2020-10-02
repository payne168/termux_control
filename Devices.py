import time
import threading
import uiautomator2 as u2

package = 'com.chinamworld.main'
activity = 'com.ccb.start.MainActivity'

class AndroidDevices:
    def __init__(self):
        self.device = u2.connect('0.0.0.0')
        # self.device = u2.connect('R3CN90724BK')
        print(self.device.info)

    def start(self):
        runComponent = package + '/' + activity
        self.device.app_start(package)
        time.sleep(10.0)
        # self.touch("查询余额")
        # time.sleep(4)
        # self.device.press("back")
        # time.sleep(2)
        # self.device.press("home")
        #中文输入法测试
        # self.device(resourceId="com.chinamworld.main:id/search_city").click()
        # self.device(resourceId="com.chinamworld.main:id/search_edit").click()
        # self.device(resourceId="com.chinamworld.main:id/search_edit").set_text("龙财富")
    def transformAmount(self):
        #转账
        self.device(resourceId="com.chinamworld.main:id/close").click_exists(timeout=3.0)
        self.device(resourceId="com.chinamworld.main:id/main_home_smart_transfer").click()
        self.device.xpath('//*[@resource-id="com.chinamworld.main:id/grid_function"]/android.widget.LinearLayout[1]').click()
        time.sleep(25.0)
        self.device(resourceId="com.chinamworld.main:id/et_password").click()
        self.device(text="h").click()
        self.device(text="b").click()
        self.device(text="7").click()
        self.device(text="4").click()
        self.device(text="1").click()
        self.device(text="9").click()
        self.device(text="6").click()
        self.device(text="3").click()
        self.device(resourceId="com.chinamworld.main:id/btn_confirm").click_gone(maxretry=10, interval=1.0)
        time.sleep(25.0)
        self.device(resourceId="com.chinamworld.main:id/et_cash_name").click()
        self.device(resourceId="com.chinamworld.main:id/et_cash_name").set_text("赵婷")
        self.device(resourceId="com.chinamworld.main:id/et_collection_account").click()
        self.device(resourceId="com.chinamworld.main:id/et_collection_account").set_text("6217996900059953209")
        time.sleep(10.0)
        self.device(resourceId="com.chinamworld.main:id/tv_bank").click()
        self.device(resourceId="com.chinamworld.main:id/tv_bank").click()
        time.sleep(20.0)
        self.device.xpath('//android.widget.GridView/android.widget.LinearLayout[15]/android.widget.ImageView[1]').click()
        time.sleep(10.0)
        self.device(resourceId="com.chinamworld.main:id/tv_transfer_way").click()
        time.sleep(10.0)
        self.device(resourceId="com.chinamworld.main:id/bottom_selector_tv", text="实时转账").click()
        time.sleep(10.0)
        self.device(resourceId="com.chinamworld.main:id/et_tran_amount").click()
        time.sleep(10.0)
        self.device(resourceId="com.chinamworld.main:id/digit_row_one_1").click()
        self.device(resourceId="com.chinamworld.main:id/ct_submit").click()
        time.sleep(10.0)
        self.device(resourceId="com.chinamworld.main:id/rl_tran_mark").click()
        self.device.send_keys("今天发的1元钱", clear=True)
        self.device.press("back")
        time.sleep(5.0)
        self.device(resourceId="com.chinamworld.main:id/btn_right1").click()
        time.sleep(10.0)
        self.device(resourceId="com.chinamworld.main:id/et_code").click()
        self.device.send_keys("112233", clear=True)
        self.device(resourceId="com.chinamworld.main:id/btn_confirm").click()
        time.sleep(10.0)
        ## d(resourceId="com.chinamworld.main:id/native_graph_et").click() 支付验证码页
        # self.device(resourceId="com.chinamworld.main:id/native_graph_iv").click()
        # self.device.send_keys("741963", clear=True)
        # self.device(resourceId="com.chinamworld.main:id/et_code").click()
        # self.device.send_keys("7q8x", clear=True)
        # self.device(resourceId="com.chinamworld.main:id/btn_confirm").click()
        #支付
        # self.device(resourceId="com.chinamworld.main:id/btn_right1").click()
    def inquiryAmount(self):
        #查询余额
        self.device(resourceId="com.chinamworld.main:id/btn_query").click()
        time.sleep(35.0)
        self.device.click(0.5, 0.749)
        self.device(text="h").click()
        self.device(text="b").click()
        self.device(text="7").click()
        self.device(text="4").click()
        self.device(text="1").click()
        self.device(text="9").click()
        self.device(text="6").click()
        self.device(text="3").click()
        self.device(resourceId="com.chinamworld.main:id/btn_confirm").click_gone(maxretry=10, interval=1.0)
        time.sleep(35.0)
        currency = self.device(resourceId="com.chinamworld.main:id/totalMoney").get_text()
        print('<---------当前余额是 %s --------->' %(currency))

    def PostSMS(self, params):
        return params['sms']

    def stop(self):
        self.device.close()

    def touch(self, objText):
        self.device(text=objText).click()

    def click(self, x, y):
        self.device.click(x, y)

    def screenOn(self):
        self.device.screen_on()
