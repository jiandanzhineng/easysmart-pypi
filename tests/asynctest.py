import warnings
import traceback
import asyncio

async def t():
    warnings.warn('test warn')
    print('test')
    raise Exception('test exception')

async def t2():
    await t()

loop = asyncio.get_event_loop()
loop.run_until_complete(t2())