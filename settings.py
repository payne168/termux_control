# coding: utf-8
from enum import Enum

bot = None

gateway = {
    'host': '127.0.0.1',
    'port': 5000,
}

bank = {
    'ccb': {'pkg': 'com.chinamworld.main', 'launcher': 'com.ccb.start.MainActivity'},
}

api = {
    'key': '1234567887654321',
    'iv': '1234567887654321',
    'ws': 'wss://bot-w.uatcashierapi.com/websocket/',
    'base': 'https://bot-w.uatcashierapi.com',
    'register': '/mobile/register',
    'start': '/mobile/start',
    'status': '/mobile/status',
    'transfer': '/mobile/transfer',
    'transaction': '/mobile/transaction',
}


class Status(Enum):
    IDLE = 0
    BOUND = 1
    STARTING = 2
    RUNNING = 3
    EXCEPTED = 4
    STOP = 5
    PAYING = 6


class Cmd(Enum):
    START = 0
    STOP = 1
    UPGRADE = 2
    TRANSFER = 3
