import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url="https://udn.com/news/cate/2/6638")

if __name__ == "__main__":
    asyncio.run(main())