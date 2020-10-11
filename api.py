# coding: utf-8
from settings import api, Status
import misc


def register(serial_no, account):
    return post(api['register'], {'serialNo': serial_no, 'accountAlias': account})


def start(device_id, account):
    return post(api['start'], {'deviceId': device_id, 'accountAlias': account})


def status(device_id, state, extra=None):
    return post(api['status'], {'serialNo': device_id, 'status': state, 'data': extra})


def transfer_status(order_id, state, msg=None):
    return post(api['transfer'], {'orderId': order_id, 'status': state, 'msg': msg})


def post(url, payload):
    url = api['base'] + url
    return misc.post(url, payload, True)


if __name__ == '__main__':
    # data = {'serialNo': 'xxxx', 'accountAlias': 'dddd'}
    # data.update(common_data())
    # print(data)
    # print(register("1ad2838c0107", "农业银行-LYF(刘亦菲)-8888"))
    # print(start('ABC_mobile_1601868756975', '农业银行-LYF(刘亦菲)-8888'))
    print(status('1ad2838c0107', Status.RUNNING.value))
    # print(transfer_status(94, 0))
