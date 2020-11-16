# coding: utf-8
from settings import api, Status
import misc


def register(serial_no, account):
    return post(api['register'], {'serialNo': serial_no, 'accountAlias': account})


def start(serial_no, account):
    return post(api['start'], {'serialNo': serial_no, 'accountAlias': account})


def status(serial_no, state, extra=None):
    return post(api['status'], {'serialNo': serial_no, 'status': state, 'data': extra})


def transfer_status(order_id, state, msg=None):
    return post(api['transfer'], {'orderId': order_id, 'status': state, 'msg': msg})


def transaction(account, balance, transactions):
    if transactions:
        trans = [{'direction': i.trans_type, 'time': i.trans_time, 'amount': i.amount, 'name': i.name, 'balance': i.balance, 'postscript': i.postscript} for i in transactions]
    else:
        trans = None
    return post(api['transaction'], {'accountAlias': account, 'balance': balance, 'trans': trans})


def verification_code(serial_no, img_base64):
    return post(api['upload_img_vc'], {'serialNo': serial_no, 'image': img_base64})


def post(url, payload):
    url = api['base'] + url
    return misc.post(url, payload, True)


if __name__ == '__main__':
    # data = {'serialNo': 'xxxx', 'accountAlias': 'dddd'}
    # data.update(common_data())
    # print(data)
    # print(register("1ad2838c0107", "农业银行-LYF(刘亦菲)-8888"))
    # print(start('ABC_mobile_1601868756975', '农业银行-LYF(刘亦菲)-8888'))
    # print(status('RR8M90JGAXR', Status.RUNNING.value))
    # print(transfer_status(94, 0)
    pass
