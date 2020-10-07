import websocket
import json
import time
import ssl
from settings import api, gateway
from log import logger
import misc

try:
    import thread
except ImportError:
    import _thread as thread


def on_message(ws, message):
    logger.info('received: %s', message)
    job = json.loads(message)
    # call gateway to execute task
    url = 'http://%s:%s/%s' % (gateway['host'], gateway['port'], job['task'])
    if 'data' in job and job['data']:
        misc.post(url, job['data'])
    else:
        misc.get(url)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print('open')

    def run(*args):
        while True:
            time.sleep(180)
            ws.send("Hello")
        # ws.close()

    thread.start_new_thread(run, ())


def serve():
    websocket.enableTrace(False)
    url = api['ws'] + misc.load_serial_no()
    ws = websocket.WebSocketApp(url, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    while ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}):
        pass


if __name__ == "__main__":
    serve()
