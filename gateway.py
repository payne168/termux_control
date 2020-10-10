# coding: utf-8
import json
from flask import Flask, request
import logging
import os
import api
from settings import gateway, bot
import misc
from models import BotUtil
from bot_factory import BotFactory
import uiautomator2 as u2

import uiautomator2 as ui2
d = ui2.connect('0.0.0.0')


app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

bot_util = BotUtil()


@app.route('/', methods=['GET'])
def hello():
    return 'Hello, World!'


@app.route('/check_evn', methods=['GET'])
def check():
    try:
        ret = os.popen("python3 -m uiautomator2 init")
        ready = ret.readline() == ""
        res = ready and {'code': 0, 'msg': '环境安装成功！'} or {'code': 1, 'msg': '环境安装失败，请重装！'}
        app.logger.info(res)

    except ConnectionRefusedError:
        res = {'code': 2, 'msg': 'atx未启动，请先插上usb线，运行电脑脚本！'}
    return json.dumps(res)


@app.route('/register', methods=['POST'])
def register():
    if request.is_json:
        try:
            params = request.get_json()
            app.logger.info(params)
            bot_factory = BotFactory(serial_no=misc.load_serial_no(), bank=params['bank'].lower(),
                                     account=params['accountAlias'])
            bot_util.cast_transfer = bot_factory.cast_transfer
            bot_util.cast_inquire_balance = bot_factory.cast_inquire_balance
            bot_util.cast_post_sms = bot_factory.cast_post_sms
            bot_util.cast_stop = bot_factory.cast_stop
            rsp = api.register(misc.load_serial_no(), params['accountAlias'])
            res = rsp is not None and rsp or {'code': 1, 'msg': '服务器未响应，请稍后再试!'}
            app.logger.info(res)

        except ConnectionRefusedError:
            res = {'code': 2, 'msg': 'atx未启动，请先插上usb线，运行电脑脚本！'}
        return res


# @app.route('/start', method=['GET'])
# def start():
#     module = __import__('bots.' + settings.bot.bank)
#     robot = getattr(module, settings.bot.bank)
#     settings.bot.device = robot.connect()
#     robot.start(settings.bot.device)


@app.route('/stop', methods=['GET'])
def stop():
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
        app.logger.info(params)
        bot_util.cast_transfer(params['amount'], params['account'], params['name'], params['bank_name'],
                               params['password'], params['withdraw_password'])

        return json.dumps(res)


@app.route('/upgrade', methods=['GET'])
def upgrade():
    res = {}
    statusRes = False
    result = ""
    evn_need_update = False
    lastLine = ""

    def git_status():
        result = os.popen("git status")  # 执行输入的命令
        readLinesContent = result.readlines()
        app.logger.info(readLinesContent)
        lastLine = readLinesContent[len(readLinesContent) - 1]
        return lastLine == "无文件要提交，干净的工作区\n" or lastLine == "nothing to commit, working tree clean\n"

    if git_status():
        evn_need_update = False
    else:
        os.popen("git fetch")
        pullRes = os.popen("git pull")
        app.logger.info(pullRes.readline())
        if git_status():
            evn_need_update = True
        else:
            evn_need_update = False

    if evn_need_update:
        res = {'code': 0, 'msg': '脚本已经更新成功!'}
    else:
        res = {'code': 1, 'msg': '脚本无需更新'}
    app.logger.info(res)
    return json.dumps(res)


@app.route('/sms_message', methods=['POST'])
def post_sms_message():
    # req={
    #     "sms": "123412314"
    # }
    res = {'code': 2, 'msg': '系统有问题，请稍后再发'}
    if request.is_json:
        params = request.get_json()
        app.logger.info(params)
        res = bot_util.cast_post_sms(params["sms"])
        post_sms = res == 0
        if post_sms:
            res = {'code': 0, 'msg': '已经接收短信验证码!'}
        else:
            res = {'code': 1, 'msg': '验证码已经过期，请重新发送！'}
        app.logger.info(res)
        return json.dumps(res)


@app.route('/inquire_balance', methods=['POST'])
def post_inquiry_amount():
    # req={
    #     "password": "hb741963",
    # }

    res = {
        "msg": "查询余额已经执行"
    }

    if request.is_json:
        params = request.get_json()
        app.logger.info(params)
        bot_util.cast_inquire_balance(params['password'])

        return json.dumps(res)


if __name__ == '__main__':
    app.run(host=gateway['host'], port=gateway['port'])
