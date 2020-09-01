# -*- coding: UTF-8 -*-
from androidDevices import AndroidDevices as Devices
package = 'com.chinamworld.main'
activity = 'com.ccb.start.MainActivity'

def main():
    device = Devices()
    device.start()

if __name__ == '__main__':
    main()