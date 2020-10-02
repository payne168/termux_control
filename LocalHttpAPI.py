# coding: utf-8
import json
from flask import Flask, request
import logging
import os
import requests
# from api import register
from settings import api

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'

@app.route('/check_evn', methods=['GET'])
def get_check_evn():
    pythonEvn = False
    res = {}
    checkRes = os.popen("python3 -m uiautomator2 init")
    if(checkRes.readline() == ""):
        pythonEvn = True
    else:
        pythonEvn = False

    if(pythonEvn == True):
        res = {'status': 0, 'msg': '环境已经安装成功了！'}
    else:
        res = {'status': 1, 'msg': '环境并没有安装成功，请重装！'}
    app.logger.info(res)
    return json.dumps(res)

@app.route('/register_device', methods=['POST'])
def post_register_device():
    # req = {
    #     "deviceId":"",
    #     "bankAccount": "",
    #     "apiURL": "",
    # }
    res = {}
    if request.is_json:
        params = request.get_json()
        app.logger.info(params)
        app.logger.info(params["deviceId"])
        register_results = True
        # respones = register(params["deviceId"], params["bankAccount"])
        if(register_results == True):
            res = {'status': 0, 'msg': '已经绑定成功!'}
        else:
            res = {'status': 1, 'msg': '服务器未响应，请稍后再试!'}
        app.logger.info(res)
        return json.dumps(res)

@app.route('/check_update', methods=['GET'])
def post_check_update():
    res = {}
    statusRes = False
    result = ""
    evn_need_update = False
    lastLine = ""

    def git_status():
        result = os.popen("git status") # 执行输入的命令
        readLinesContent = result.readlines()
        app.logger.info(readLinesContent)
        lastLine = readLinesContent[len(readLinesContent) - 1]
        return lastLine == "无文件要提交，干净的工作区\n" or lastLine == "nothing to commit, working tree clean\n"

    if(git_status()):
        evn_need_update = False
    else:
        os.popen("git fetch")
        pullRes = os.popen("git pull")
        app.logger.info(pullRes.readline())
        if(git_status()):
            evn_need_update = True
        else:
            evn_need_update = False

    if(evn_need_update == True):
        res = {'status': 0, 'msg': '脚本已经更新成功!'}
    else:
        res = {'status': 1, 'msg': '脚本无需更新'}
    app.logger.info(res)
    return json.dumps(res)

@app.route('/sms_message', methods=['POST'])
def post_sms_message():
    req={
        "sms": ""
    }
    res = {}
    if request.is_json:
        params = request.get_json()
        app.logger.info(params)
        url = api['base'] + '/PostSMS'
        req["sms"] = params["sms"]
        header_dict = {"Content-Type":"application/json; charset=utf8"}
        r = requests.post(url, data=json.dumps(req), headers=header_dict)
        post_sms = True
        if(post_sms == True):
            res = {'status': 0, 'msg': '已经接收短信验证码!'}
        else:
            res = {'status': 1, 'msg': '验证码已经过期，请重新发送！'}
        app.logger.info(res)
        return json.dumps(res)