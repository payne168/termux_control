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
    elif bank == 'ABC':
        return datetime.strptime(f'{datetime.today().year}年{trans_time}', '%Y年%m月%d日%H:%M').strftime('%Y-%m-%d %X')
    elif bank == 'ICBC':
        return datetime.strptime(f'{datetime.today().year}年{trans_time}', '%Y年%m月%d日%H:%M').strftime('%Y-%m-%d %X')
    return ''


if __name__ == '__main__':
    ccb_vc = '序号03的验证码468134，您向汪仙尾号3275账户转账1.0元。任何索要验证码的都是骗子，千万别给！[建设银行]'
    ccb_expenditure = '您尾号0333的储蓄卡10月21日15时50分向李文聪转账支取支出人民币5.00元,活期余额20.50元。[建设银行]'
    ccb_income = '李文聪10月21日16时58分向您尾号0333的储蓄卡转账存入人民币1.00元,活期余额21.50元。[建设银行]'
    ccb_span_expenditure = '您尾号0333的储蓄卡11月4日15时59分向李瑶恒跨行转出支出人民币1.00元,活期余额19.50元。[建设银行]'
    # print(parse_sms(ccb_vc))
    # print(parse_sms(ccb_income))
    # print(parse_sms(ccb_span_expenditure))
    # print(parse_sms(ccb_expenditure))

    # abc_span_expenditure = "【中国农业银行】您尾号0873账户11月18日20:32向张家将完成转支交易人民币-10.00，余额24.53。"
    # abc_income = "【中国农业银行】吴立娜于11月18日19:41向您尾号0873账户完成转存交易人民币30.00，余额34.53。"
    # print(parse_sms(abc_span_expenditure))
    # print(parse_sms(abc_income))

    icbc_span_income = '您尾号4133卡12月8日14:15工商银行收入(他行汇入)10元，余额34元，对方户名：谭世琦，对方账户尾号：9077。【工商银行】'
    icbc_span_expenditure = '您尾号4133卡12月8日11:57手机银行支出(跨行汇款)1元，余额24元，对方户名：潘家旭，对方账户尾号：7497。【工商银行】'
    print(parse_sms(icbc_span_income))
    print(parse_sms(icbc_span_expenditure))

    # other = '温馨提示：您上月结转剩余国内流量1.000G，本月月底前有效。回复"流量查询"或点击http://u.10010.cn/qAagl查询详情。'
    # print(parse_sms(other))

