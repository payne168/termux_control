# -*- coding: UTF-8 -*-
from Devices import AndroidDevices as Devices
from http.server import HTTPServer
from WebService import TodoHandler as WS
package = 'com.chinamworld.main'
activity = 'com.ccb.start.MainActivity'

def main():
    server = HTTPServer(('localhost', 8080), WS)
    print("Starting server, use <Ctrl-C> to stop")
    server.serve_forever()
if __name__ == '__main__':
    main()