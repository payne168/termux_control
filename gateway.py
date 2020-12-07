# coding: utf-8
import requests
from flask import Flask, request
import json
from datetime import datetime
import time
import logging
import os
import api
from settings import gateway, serial_no, bank_map, root_service
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
            update_config(params['apiUrl'], params['accountAlias'])
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
        print(res['data'])
        bot_factory = BotFactory()
        bot_util.cast_transfer = bot_factory.cast_transfer
        bot_util.cast_transaction_history = bot_factory.cast_transaction_history
        bot_util.cast_post_sms = bot_factory.cast_post_sms
        bot_util.cast_stop = bot_factory.cast_stop
        bot_util.do_works = bot_factory.do_works
        bot_util.do_verify_code = bot_factory.do_verify_code
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
    res = {
        "msg": "存款已经执行"
    }

    if request.is_json:
        params = request.get_json()
        print("转账任务-------------------->")
        print(params['orderId'], params['amount'], params['account'], params['holder'], bank_map[params['bank']])
        print("转账任务-------------------->")
        bot_util.cast_transfer(params['orderId'], params['amount'], params['account'], params['holder'],
                               bank_map[params['bank']])

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
        requests.get(url="http://%s%s/restart" % (settings.root_service['host'], settings.root_service['port']))
    else:
        res = {'code': 1, 'msg': '脚本无需更新'}
    logger.info('/upgrade %s', res)
    return res


@app.route('/pc_details', methods=['POST'])
def pc_details():
    if request.is_json:
        params = request.get_json()
        settings.pc_url = params['url']
        usb_key_id = params['usbKeyId']
        config = load_config()
        print(config)
        alias = config['account']['alias']
        print(params)
        print(params['UsbKeyId'])
        print(usb_key_id)
        data = {
            'UsbKeyId': usb_key_id,
            'alias': alias
            # 'alias': '农业银行-WQ(韦强)-0873'
        }
        print(data)
        print(settings.pc_url + '/bind')
        res = requests.post(url=settings.pc_url + '/bind', json=data)
        print(res.text)
        body = json.loads(res.text)
        print(body)
        for usb in body["body"]:
            if usb["alias"] == alias and usb["key_id"] == usb_key_id:
                settings.presser = usb

        return {'code': 0, 'msg': '已经获取PC信息!'}


@app.route('/press', methods=['GET'])
def press():
    print(settings.presser)
    res = requests.post(url=settings.pc_url + '/press', json=settings.presser)
    print(res.text)
    body = json.loads(res.text)
    if body["code"] == 0:
        return {'code': 0, 'msg': '已经点击!'}
    else:
        return {'code': 1, 'msg': '没有点击成功!'}


@app.route('/verify_code', methods=['POST'])
def verify_code():
    if request.is_json:
        params = request.get_json()
        code = params['code']
        # TODO enter verification code
        bot_util.do_verify_code(code)


@app.route('/sms', methods=['POST'])
def sms():
    if request.is_json:
        params = request.get_json()
        logger.info('sms req: %s', params)
        code, data = misc.parse_sms(params['sms'])
        if code == 0:
            # validation code
            received_at = datetime.strptime(params['time'], '%Y-%m-%d %H:%M:%S').timestamp()
            if time.time() - received_at > 180:
                rsp = {'code': 0, 'msg': '发送短信超时'}
            else:
                try:
                    ret = bot_util.cast_post_sms(data)
                    rsp = ret == 0 and {'code': 0, 'msg': '已经接收短信验证码!'} or {'code': 0, 'msg': '验证码已过期'}
                except TypeError:
                    logger.exception('卡机未启动网银应用')
                    rsp = {'code': 0, 'msg': '卡机未启动网银应用'}
            logger.info('sms rsp: %s', rsp)
            return rsp
        elif code == 1:
            # transaction
            trans = Transaction(trans_time=data['time'], trans_type=data['direction'], name=data['name'],
                                amount=data['amount'], balance=data['balance'])
            try:
                rsp = api.transaction(settings.bot.account.alias, data['balance'], (trans,))
                return rsp
            except:
                logger.exception('上报流水网络异常')
                return {'code': 1, 'msg': '上报流水网络异常'}
        else:
            return {'code': 0, 'msg': '非银行短信，已忽略'}


def load_config():
    if os.path.exists(settings.conf_file):
        with open(settings.conf_file, 'r') as conf:
            config = json.loads(conf.read())
            api_url = config['api']['base']
            settings.api['base'] = api_url
            settings.api['ws'] = os.path.join(api_url.replace('http', 'ws'), 'websocket')
            return config
    return None


def update_config(api_url, account):
    settings.api['base'] = api_url
    ws = os.path.join(api_url.replace('http', 'ws'), 'websocket')
    settings.api['ws'] = ws

    with open(settings.conf_file, 'w') as conf:
        conf.write(json.dumps({'api': {'base': api_url, 'ws': ws}, 'account': {'alias': account}}))


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
