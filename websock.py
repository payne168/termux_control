import websocket
import json
from log import logger

try:
    import thread
except ImportError:
    import _thread as thread
import time


def on_message(ws, message):
    print('received: ', message)
    data = json.loads(message)
    if data['task'] == 'upgrade':
        upgrade()
    elif data['task'] == 'transfer':
        transfer()


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print("thread terminating...")

    thread.start_new_thread(run, ())


def upgrade():
    pass


def transfer():
    pass


if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("ws://echo.websocket.org/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
