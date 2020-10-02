import cgi
import json
from Devices import AndroidDevices as Devices
from http.server import BaseHTTPRequestHandler
device = Devices()
class TodoHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        if self.path != '/':
            self.send_error(404, "File not found.")
            return

        message = json.dumps(self.TODOS)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(message)

    def do_POST(self):

        ctype, pdict = cgi.parse_header(self.headers['content-type'])

        if ctype == 'application/json':
            length = int(self.headers['content-length'])
            post_values = json.loads(self.rfile.read(length))
            fun = self.path.split("/", 1)[1]
            if(fun == "PostSMS"):
                sms = getattr(device, fun)(post_values)
                print(sms)
            else:
                device.start()
                getattr(device, fun)()
        else:
            self.send_error(415, "Only json data is supported.")
            return

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write('指令已经接收成功'.encode())