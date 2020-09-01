import time
import threading
import uiautomator2 as u2

package = 'com.chinamworld.main'
activity = 'com.ccb.start.MainActivity'

class AndroidDevices:
    def __init__(self):
        self.device = u2.connect('0.0.0.0')
        print(self.device.info)

    def start(self):
        runComponent = package + '/' + activity
        self.device.app_start(package)
        time.sleep(5)
        self.touch("查询余额")
        time.sleep(4)
        self.device.press("back")
        time.sleep(2)
        self.device.press("home")

    def stop(self):
        self.device.close()

    def touch(self, objText):
        self.device(text=objText).click()

    def click(self, x, y):
        self.device.click(x, y)

    def screenOn(self):
        self.device.screen_on()
