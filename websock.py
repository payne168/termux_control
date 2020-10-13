import asyncio
import websockets
import ssl
import json
import time
import misc
from settings import api, gateway, serial_no
from log import logger
try:
    import thread
except ImportError:
    import _thread as thread

ssl_context = ssl.SSLContext()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


async def consumer(ws):
    message = await ws.recv()
    logger.info('received: %s', message)
    job = json.loads(message)
    # call gateway to execute task
    url = 'http://%s:%s/%s' % (gateway['host'], gateway['port'], job['task'])
    if 'data' in job and job['data']:
        misc.post(url, job['data'])
    else:
        misc.get(url)


def producer(ws):
    new_loop = asyncio.new_event_loop()
    while True:
        time.sleep(10)

        async def run(ws):
            # logger.info('pulse')
            await ws.send("pulse")

        # asyncio.run_coroutine_threadsafe(run(ws), new_loop)
        new_loop.run_until_complete(run(ws))


async def main():
    uri = '%s/%s' % (api['ws'], serial_no)
    logger.info('web socket:%s', uri)
    async with websockets.connect(uri, ssl=ssl_context) as ws:
        logger.info('web socket connection established')
        thread.start_new_thread(producer, (ws,))
        while True:
            logger.info('ready to receive msg')
            await consumer(ws)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
