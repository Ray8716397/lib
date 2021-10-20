# coding=utf-8
# @CREATE_TIME: 2021/7/22 下午6:47
# @LAST_MODIFIED: 2021/7/22 下午6:47
# @FILE: AsyncRpcClient.py
# @AUTHOR: Ray
import asyncio
import uuid

from aio_pika import connect_robust, IncomingMessage, Message
from aio_pika.patterns import RPC
from lib.common.singleton_config import config


class AsyncRpcClient:
    mq_name = config["mq_name"] if "mq_name" in config.keys() and config["mq_name"] != '' else 'ocr_queue'

    def __init__(self, aio_loop):
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.futures = {}
        self.loop = aio_loop
        self.rpc = None

    async def connect(self):
        self.connection = await connect_robust(
            "amqp://guest:guest@localhost/", loop=self.loop
        )
        self.channel = await self.connection.channel()
        # self.callback_queue = await self.channel.declare_queue(exclusive=True)
        # await self.callback_queue.consume(self.on_response)
        self.rpc = await RPC.create(self.channel)
        return self

    def on_response(self, message: IncomingMessage):
        future = self.futures.pop(message.correlation_id)
        future.set_result(message.body)

    async def call(self, body, bool_draw_img, target_mq_name=None):
        if target_mq_name is None:
            target_mq_name = self.mq_name
        return await self.rpc.call(target_mq_name, kwargs=dict(img_fp=body, bool_draw_img=bool_draw_img))


if __name__ == "__main__":
    async def main(loop):
        fibonacci_rpc = await AsyncRpcClient(loop).connect()
        print(" [x] Requesting fib(30)")
        response = await fibonacci_rpc.call(30)
        print(" [.] Got %r" % response)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
