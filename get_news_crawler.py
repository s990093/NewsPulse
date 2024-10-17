
# Example usage
from src.crawler.base_crawler import BaseCrawler
from src.crawler.news_site_a.get_day_news import FakeNewsCrawler


if __name__ == "__main__":

    # Creating multiple crawlers with fake data
    crawlers = [
        FakeNewsCrawler("https://fakenews.com/site1", article_limit=10),
        # FakeNewsCrawler("https://fakenews.com/site2", article_limit=8),
        # FakeNewsCrawler("https://fakenews.com/site3", article_limit=12),
    ]

    # Running the crawlers
    BaseCrawler.run_crawlers(crawlers, thread_count=2)