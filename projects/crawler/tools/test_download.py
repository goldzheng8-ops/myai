import asyncio
import httpx

URL = "https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg"

async def main():
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(URL)
            print('status_code=', r.status_code)
            print('len=', len(r.content))
    except Exception as e:
        print('error:', type(e), e)

if __name__ == '__main__':
    asyncio.run(main())
