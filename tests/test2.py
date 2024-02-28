import time
import asyncio

async def say(text, sec):
    await asyncio.sleep(sec)
    print(text)

async def main():
    print('start main')
    start = time.monotonic()
    await asyncio.gather(
        say("First", 2),
        say("Second", 1),
    )
    end = time.monotonic()
    print(f"Elapsed: {end-start}")


from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy

set_event_loop_policy(WindowsSelectorEventLoopPolicy())
try:
    loop = asyncio.get_event_loop()
except:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
main_co = main()
print(main_co)
asyncio.run(main_co)