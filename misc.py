# coding: utf-8
import random
import string
import time
import requests
from log import logger


def get(url):
    logger.info('req %s', url)
    begin = time.time()
    rsp = requests.get(url)
    logger.info('rsp from %s, status=%s, text=%s, cost %s seconds', url, rsp.status_code, rsp.text, time.time() - begin)
    return rsp.ok and rsp.json() or None


def post(url, payload, with_common=False):
    if with_common:
        payload.update(common_data())
    logger.info('req %s, params=%s', url, payload)

    begin = time.time()
    rsp = requests.post(url, json=payload)
    logger.info('rsp from %s, status=%s, text=%s, cost %s seconds', url, rsp.status_code, rsp.text, time.time() - begin)
    return rsp.ok and rsp.json() or None


def common_data():
    return {'nonce': ''.join(random.sample(string.ascii_letters + string.digits, 10)), 'timestamp': int(time.time())}


def load_serial_no():
    return '1ad2838c0107'
