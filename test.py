import cv2
import uiautomator2 as u2
import time
package = 'com.chinamworld.bocmbci'
activity = 'com.boc.bocsoft.mobile.bocmobile.buss.system.main.ui.MainActivity'

device = u2.connect('0.0.0.0')
device.app_start(package)
device(resourceId="com.chinamworld.bocmbci:id/tv_item", text="转账").click()
device(resourceId="com.chinamworld.bocmbci:id/loginPasswordSipBox").click()
# device.send_keys("w1472580", clear=True)
# time.sleep(6)
# device.click(0.228, 0.773)
# device(text="w").click()
# device(text="1").click()
# device(resourceId="com.chinamworld.bocmbci:id/loginSubmitBtn").click()
# img = "verification.jpg"
img = device.screenshot()
img.save("verification.jpg")
# image = device.screenshot(format='opencv')
# cv2.imwrite('verification.jpg', image)

# imagebin = device.screenshot(format='raw')
# open("verification.jpg", "wb").write(imagebin)