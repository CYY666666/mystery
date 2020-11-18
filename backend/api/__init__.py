import asyncio
from asyncio import futures
from concurrent.futures.thread import ThreadPoolExecutor

from utils.async_run import get_ioloop

loop = asyncio.get_event_loop()
thread_executor = ThreadPoolExecutor(max_workers=4)


def run_in_thread(fn, *args, **kwargs):
    return futures.wrap_future(
        thread_executor.submit(fn, *args, **kwargs), loop=loop
    )
