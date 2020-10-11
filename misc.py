# coding: utf-8
import re
import random
import string
import time
import requests
from settings import id_file, sms_bank, sms_vc
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
    with open(id_file) as fd:
        serial_no = fd.readline()
        logger.info('serial no:%s', serial_no)
        return serial_no


def parse_sms(sms):
    for k, v in sms_bank.items():
        if re.findall(v, sms):
            if '验证码' in sms:
                return True, re.findall(sms_vc[k], sms)[0]
            else:
                # TODO 提取流水
                return False, {}


if __name__ == '__main__':
    print(parse_sms('序号03的验证码468134，您向汪仙尾号3275账户转账1.0元。任何索要验证码的都是骗子，千万别给！[建设银行1]'))
