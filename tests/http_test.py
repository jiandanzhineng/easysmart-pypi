import asyncio

import aiohttp


async def post_data(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            return await response.text()


async def feedback():
    filter = 'device_type'
    detail = 'DIANJI'
    url = f"http://127.0.0.1:8555/device/act/{filter}/{detail}/"
    data = {"action": "dian", "voltage": 200, "time": 1000}
    result = await post_data(url, data)
    print("POST请求返回的结果:", result)

if __name__ == '__main__':
    asyncio.run(feedback())