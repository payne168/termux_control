# coding: utf-8
from enum import Enum
import os

conf_file = 'config.json'
bot = None

with open('../device_id.txt') as fd:
    serial_no = fd.readline().strip()

gateway = {
    'host': '127.0.0.1',
    'port': 5000,
}

root_service = {
    'host': '127.0.0.1',
    'port': 8081,
}

api = {
    'key': '1234567887654321',
    'iv': '1234567887654321',
    'ws': 'wss://bot-w.uatcashierapi.com/websocket',
    'base': 'https://bot-w.uatcashierapi.com',
    'register': '/mobile/register',
    'start': '/mobile/start',
    'status': '/mobile/status',
    'transfer': '/mobile/transfer',
    'transaction': '/mobile/transaction',
}

bank_map = {
    'CCB': '中国建设银行',
    'ICBC': '中国工商银行',
    'ABC': '中国农业银行',
    'BOCSH': '中国银行',
    'BCM': '交通银行',
    'CMB': '招商银行',
    'MSB': '中国民生银行',
    'CITTIC': '中信银行',
    'SHPDB': '上海浦东发展银行',
    'PAB': '平安银行（原深圳发展银行）',
    'INB': '兴业银行',
    'EBB': '中国光大银行',
    'GDB': '广发银行股份有限公司',
    'HXB': '华夏银行',
    'PSBC': '中国邮政储蓄银行',
    'BOS': '上海银行',
    'JSBK': '江苏银行股份有限公司',
}

sms_bank = {
    'CCB': r'\[建设银行]$',
}

sms_vc = {
    'CCB': r'验证码(\d{6})',
}

sms_trans = {
    'CCB': {'direction': (r'支出', r'存入'), 'pattern': (
        {'time': r'储蓄卡(.+)向', 'name': r'向(.+)转账', 'amount': r'人民币(\d+\.?\d{0,2})元', 'balance': r'余额(\d+\.?\d{0,2})元'},
        {'time': r'(\d{1,2}.+分)', 'name': r'^(\D+)', 'amount': r'人民币(\d+\.?\d{0,2})元', 'balance': r'余额(\d+\.?\d{0,2})元'},
    )},
}


class Status(Enum):
    IDLE = 0
    BOUND = 1
    STARTING = 2
    RUNNING = 3
    EXCEPTED = 4
    STOP = 5
    PAYING = 6

