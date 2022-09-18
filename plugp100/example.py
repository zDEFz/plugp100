import asyncio

from plugp100 import TapoApiClient, TapoApiClientConfig


async def main():
    # create generic tapo api
    config = TapoApiClientConfig("<ip>", "<email>", "<passwd>")
    sw = TapoApiClient.from_config(config)
    await sw.login()
    await sw.on()
    await sw.set_brightness(100)
    state = await sw.get_state()
    print(state.get_unmapped_state())


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_until_complete(asyncio.sleep(0.1))
loop.close()

if __name__ == "__main__":
    main()
