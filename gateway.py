# coding: utf-8
from flask import Flask, request
import json
import logging
import os
import api
from settings import gateway, serial_no, bank_map
import settings
import misc
from models import BotUtil, Bot, Account, Transaction
from bot_factory import BotFactory
import uiautomator2 as u2
from log import logger

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

bot_util = BotUtil()


@app.route('/', methods=['GET'])
def hello():
    app.logger.info(serial_no)
    return serial_no


@app.route('/check_evn', methods=['GET'])
def check():
    try:
        ready = len(dir(u2)) > 100
        res = ready and {'code': 0, 'msg': '环境安装成功！'} or {'code': 1, 'msg': '环境安装失败，请重装！'}
        logger.info('/check_env rsp: %s', res)
    except ConnectionRefusedError:
        res = {'code': 2, 'msg': 'atx未启动，请先插上usb线，运行电脑脚本！'}
        logger.info('/check_env rsp: %s', res)
    return res


@app.route('/register', methods=['POST'])
def register():
    if request.is_json:
        try:
            params = request.get_json()
            logger.info('/register req: %s', params)
            # update config first, it'll update api{url,ws} in settings, prepare for accessing server api
            update_config(params['apiUrl'], params['accountAlias'], params['bank'])
            rsp = api.register(serial_no, params['accountAlias'])
            res = rsp is not None and rsp or {'code': 1, 'msg': '服务器未响应，请稍后再试!'}
            logger.info('/register rsp: %s', res)
        except ConnectionRefusedError:
            res = {'code': 1, 'msg': '向服务端注册设备失败！'}
            logger.info('/register rsp: %s', res)
        return res


@app.route('/start', methods=['GET'])
def start():
    try:
        config = load_config()
        if config is None or 'account' not in config:
            return {'code': 1, 'msg': '未绑定银行卡'}

        res = api.start(serial_no, config['account']['alias'])
        if res is None or res['code'] != 0:
            return {'code': 1, 'msg': '获取银行卡信息失败'}

        convert(data=res['data'])

        bot_factory = BotFactory()
        bot_util.cast_transfer = bot_factory.cast_transfer
        bot_util.cast_transaction_history = bot_factory.cast_transaction_history
        bot_util.cast_post_sms = bot_factory.cast_post_sms
        bot_util.cast_stop = bot_factory.cast_stop
        bot_util.do_works = bot_factory.do_works
        bot_util.do_works()
    except ConnectionRefusedError:
        res = {'code': 1, 'msg': '启动失败，ConnectionRefusedError！'}
        logger.info('/start rsp: %s', res)
    return {'code': 0, 'msg': '启动成功'}


@app.route('/stop', methods=['GET'])
def stop():
    print(dir(bot_util))
    bot_util.cast_stop()


@app.route('/transfer', methods=['POST'])
def transfer():
    # req={
    #     "amount": "1",
    #     "transform_account": "赵婷",
    #     "bank_kind": "6217996900059953209",
    #     "password": "hb741963",
    #     "withdraw_password": "741963"
    # }

    res = {
        "msg": "存款已经执行"
    }

    if request.is_json:
        params = request.get_json()
        bot_util.cast_transfer(params['amount'], params['account'], params['holder'], bank_map[params['bank']])

        return res


@app.route('/upgrade', methods=['GET'])
def upgrade():
    def git_status():
        result = os.popen("git status").readlines()  # 执行输入的命令
        logger.info('git status: %s', result)
        last_line = result[-1]
        return last_line == "无文件要提交，干净的工作区\n" or last_line == "nothing to commit, working tree clean\n"

    if git_status():
        evn_need_update = False
    else:
        os.popen("git fetch")
        pull_res = os.popen("git pull").readline()
        logger.info('pull result: %s', pull_res)
        if git_status():
            evn_need_update = True
        else:
            evn_need_update = False

    if evn_need_update:
        res = {'code': 0, 'msg': '脚本已经更新成功!'}
    else:
        res = {'code': 1, 'msg': '脚本无需更新'}
    logger.info('/upgrade %s', res)
    return res


@app.route('/sms', methods=['POST'])
def sms():
    if request.is_json:
        params = request.get_json()
        logger.info('sms req: %s', params)
        is_vc, data = misc.parse_sms(params['sms'])
        if is_vc:
            ret = bot_util.cast_post_sms(data)
            rsp = ret == 0 and {'code': 0, 'msg': '已经接收短信验证码!'} or {'code': 1, 'msg': '验证码已经过期，请重新发送！'}
            logger.info('sms rsp: %s', rsp)
            return rsp
        else:
            # 上报流水
            pass


def load_config():
    if os.path.exists(settings.conf_file):
        with open(settings.conf_file, 'r') as conf:
            config = json.loads(conf.read())
            api_url = config['api']['base']
            settings.api['base'] = api_url
            settings.api['ws'] = os.path.join(api_url.replace('http', 'ws'), 'websocket')
            return config
    return None


def update_config(api_url, account, bank):
    settings.api['base'] = api_url
    ws = os.path.join(api_url.replace('http', 'ws'), 'websocket')
    settings.api['ws'] = ws

    with open(settings.conf_file, 'w') as conf:
        conf.write(json.dumps({'api': {'base': api_url, 'ws': ws}, 'account': {'alias': account, 'bank': bank}}))


def convert(data):
    account = Account(alias=data['accountAlias'], login_name=data['loginName'], login_pwd=data['loginPassword'],
                      payment_pwd=data['paymentPassword'])
    settings.bot = Bot(serial_no=serial_no, bank=data['bank'], account=account)
    if 'lastTrans' in data and data['lastTrans']:
        tran = data['lastTrans']
        trans = Transaction(trans_time=tran['time'], trans_type=tran['direction'], name=tran['name'],
                            amount=tran['amount'], balance=tran['balance'], postscript=tran['postscript'])
        settings.bot.last_trans = trans


if __name__ == '__main__':
    app.run(host=gateway['host'], port=gateway['port'])
