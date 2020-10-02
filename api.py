import requests
import time
import random
import string
import json
from settings import api
from log import logger


def register(serial_no, account):
    return post(api['register'], {'serialNo': serial_no, 'accountAlias': account})


def start(device_id, account):
    return post(api['start'], {'deviceId': device_id, 'accountAlias': account})


def status(device_id, state, extra):
    return post(api['status'], {'deviceId': device_id, 'status': state, 'data': extra})


def transfer_status(order_id, state, msg):
    return post(api['transfer'], {'orderId': order_id, 'status': state, 'msg': msg})


def post(url, payload):
    url = api['base'] + url
    params = payload.update(common_data())
    logger.info('url=%s, params=%s', url, params)

    begin = time.time()
    rsp = requests.post(url, json=params)
    logger.info('rsp of url: %s, status=%s, text=%s, cost %s seconds', url, rsp.status_code, rsp.text, time.time() - begin)
    if rsp.ok:
        return json.loads(rsp.text)
    return None


def common_data():
    return {'nonce': ''.join(random.sample(string.ascii_letters + string.digits, 10)), 'timestamp': int(time.time())}


if __name__ == '__main__':
    data = {'serialNo': 'xxxx', 'accountAlias': 'dddd'}
    data.update(common_data())
    print(data)
