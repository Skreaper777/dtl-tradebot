import asyncio
import os

from tinkoff.invest import AsyncClient

TOKEN = "t.zSv0PvqY9KLK07vFsbvdjHAW0fh-qeN4TXr6PksjPJDUVdIkIFI0RZ-hhHHC2gMY7RHpDxnEcJlnWWmMQZztGg"


async def main():
    async with AsyncClient(TOKEN) as client:
        print(await client.users.get_accounts())


if __name__ == "__main__":
    asyncio.run(main())