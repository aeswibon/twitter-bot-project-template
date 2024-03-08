import asyncio
from time import sleep

import aiohttp


async def main():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "http://localhost:9000/api/v1/bot/refresh/"
            ) as response:
                sleep(5)
                if response.status == 200:
                    print("Success")
                else:
                    response_text = await response.text()
                    raise Exception(
                        f"Job Failed with status {response.status}. Response: {response_text}"
                    )
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
