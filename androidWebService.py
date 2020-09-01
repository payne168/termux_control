from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import simplejson as json
from androidDevices import AndroidDevices as Devices
device = devices()
class TodoHandler(BaseHTTPRequestHandler):
    TODOS = []
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
            self.TODOS.append(post_values)
            getattr(device, self.path.split("/", 1)[1])()
        else:
            self.send_error(415, "Only json data is supported.")
            return

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(post_values)