from typing import TypedDict, List
from faker import Faker
from selenium.webdriver.chrome.options import Options
from rich.console import Console
import time
import threading
from abc import ABC, abstractmethod
from rich.progress import Progress
from rich.table import Table

from src.crawler.base_crawler import *




# FakeNewsCrawler Implementation
class FakeNewsCrawler(BaseCrawler):
    def __init__(self, base_url: str, options: Options = Options(), article_limit: int = 100):
        super().__init__(base_url, options, article_limit)
        self.fake = Faker()

    def fetch_news(self) -> NewsList:
        news_list: NewsList = []  # Initialize a list, using NewsList only as a type hint
        for _ in range(self.article_limit):
            news_list.append({
                "id": self.fake.uuid4(),
                "time": self.fake.date_time_this_year().isoformat(),
                "title": self.fake.sentence(nb_words=6),
                "content": self.fake.paragraph(nb_sentences=3),
                "url": self.fake.url(),
                "domain": self.base_url
            })
            time.sleep(0.1)  # Simulate network delay for fetching news data
        return news_list

# # Example usage
# if __name__ == "__main__":
#     console = Console()

#     # Creating multiple crawlers with fake data
  
#     FakeNewsCrawler("https://fakenews.com/site3", article_limit=12)
    
#     FakeNewsCrawler.start()
    
    

  