import asyncio
import socket
import websockets
import ssl
import json
import time
import os
import misc
from settings import gateway, serial_no, conf_file
from log import logger
try:
    import thread
except ImportError:
    import _thread as thread

ssl_context = ssl.SSLContext()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


async def consume(ws):
    while True:
        logger.info('ready to receive msg')
        message = await ws.recv()
        logger.info('received: %s', message)
        job = json.loads(message)
        # call gateway to execute task
        url = 'http://%s:%s/%s' % (gateway['host'], gateway['port'], job['task'])
        if 'data' in job and job['data']:
            misc.post(url, job['data'])
        else:
            misc.get(url)


async def produce(ws):
    while True:
        await asyncio.sleep(300)
        logger.info('pulse')
        await ws.send("pulse")


async def load_conf():
    ws = None
    while True:
        if os.path.exists(conf_file):
            try:
                with open(conf_file, 'r') as fd:
                    conf = json.loads(fd.read())
                    ws = conf['api']['ws']
            except:
                logger.exception('load conf error')
        if ws:
            return ws
        else:
            logger.info('未加载到WebSocket配置，请先扫码绑定银行卡')
            time.sleep(10)


async def main():
    ws_url = await load_conf()
    uri = '%s/%s' % (ws_url, serial_no)
    logger.info('web socket:%s', uri)

    while True:
        try:
            async with websockets.connect(uri, ssl=ssl_context) as ws:
                while True:
                    logger.info('web socket connection established')
                    await asyncio.gather(produce(ws), consume(ws))
        except (socket.gaierror, ConnectionRefusedError, websockets.exceptions.ConnectionClosed):
            logger.info('web socket lost connectivity, reconnect...')
            continue


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
