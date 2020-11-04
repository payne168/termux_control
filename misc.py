# coding: utf-8
import re
import random
import string
import time
from datetime import datetime
import requests
from settings import sms_bank, sms_vc, sms_trans
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


def parse_sms(sms):
    for k, v in sms_bank.items():
        if re.findall(v, sms):
            if '验证码' in sms:
                return 0, re.findall(sms_vc[k], sms)[0]
            else:
                directions = sms_trans[k]['direction']
                for i, direction in enumerate(directions):
                    if direction in sms:
                        pattern = sms_trans[k]['pattern'][i]
                        trans_time = re.findall(pattern['time'], sms)[0]
                        name = re.findall(pattern['name'], sms)[0]
                        amount = re.findall(pattern['amount'], sms)[0]
                        balance = re.findall(pattern['balance'], sms)[0]
                        trans_time = convert_trans_time(k, trans_time)
                        return 1, {'direction': i, 'time': trans_time, 'name': name, 'amount': amount, 'balance': balance}
                return 1, None
    return -1, None


def convert_trans_time(bank, trans_time):
    if bank == 'CCB':
        return datetime.strptime(f'{datetime.today().year}年{trans_time}', '%Y年%m月%d日%H时%M分').strftime('%Y-%m-%d %X')
    return ''


if __name__ == '__main__':
    print(parse_sms('序号03的验证码468134，您向汪仙尾号3275账户转账1.0元。任何索要验证码的都是骗子，千万别给！[建设银行]'))
    ccb_expenditure = '您尾号0333的储蓄卡10月21日15时50分向李文聪转账支取支出人民币5.00元,活期余额20.50元。[建设银行]'
    ccb_income = '李文聪10月21日16时58分向您尾号0333的储蓄卡转账存入人民币1.00元,活期余额21.50元。[建设银行]'
    ccb_span_expenditure = '您尾号0333的储蓄卡11月4日15时59分向李瑶恒跨行转出支出人民币1.00元,活期余额19.50元。[建设银行]'
    # print(parse_sms('您尾号8540的储蓄卡10月21日17时21分向林美娣转账支取支出人民币1.00元,活期余额11.50元。[建设银行]'))
    # print(parse_sms(ccb_income))
    print(parse_sms(ccb_span_expenditure))
    print(parse_sms(ccb_expenditure))
