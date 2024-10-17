import time
import threading
from abc import ABC, abstractmethod
from selenium import webdriver
from rich.progress import Progress
from rich.table import Table
from rich.console import Console
from src.helper.news_types import NewsList
from selenium.webdriver.chrome.options import Options
from typing import List, Optional
import traceback



__all__ = ['BaseCrawler', 'NewsList']

class BaseCrawler(ABC):
    def __init__(self, base_url: str, options: Options = Options(), article_limit: int = 100):
        """
        Initialize a BaseCrawler instance.

        Parameters:
        - base_url (str): The base URL of the news website to crawl.
        - options (Options, optional): Selenium webdriver options for customizing the browser behavior. Defaults to Options().
        - article_limit (int, optional): The maximum number of articles to crawl. Defaults to 100.

        Attributes:
        - base_url (str): The base URL of the news website.
        - article_limit (int): The maximum number of articles to crawl.
        - news_data (list): A list to store the crawled news data.
        - console (Console): A rich console instance for logging and displaying progress.
        - options (Options): Selenium webdriver options for customizing the browser behavior.
        """
        
        self.base_url = base_url
        self.article_limit = article_limit
        self.news_data = []
        self.console = Console()

        self.options = options
        self.crawl_time = 0  # Initialize crawl time to 0



    @abstractmethod
    def fetch_news(self) -> NewsList:
        pass

    def _crawl(self):
        """
        Crawls the news website and stores the crawled news data.

        This method measures the time taken to crawl the news website, logs the progress,
        and handles any exceptions that may occur during the crawling process.

        Parameters:
        None

        Returns:
        None
        """
        try:
            start_time = time.time()
            self.console.log(f"開始爬取 {self.base_url}")
            news = self.fetch_news()
            self.news_data.extend(news)
            elapsed_time = time.time() - start_time
            # Create and display the result in a table
            self.console.log()
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("新聞來源", justify="left")
            table.add_column("總篇數", justify="right")
            table.add_column("花費時間 (秒)", justify="right")

            # Add the row for this crawl's results
            table.add_row(self.base_url, str(len(news)), f"{elapsed_time:.2f}")

            # Print the table
            self.console.print(table)        
        except Exception as e:
            self.console.log(f"爬取 {self.base_url} 時發生錯誤: {str(e)}")
            self.console.log("詳細錯誤追蹤：")
            self.console.log(traceback.format_exc())  # Log the traceback details

    def start(self):
        """
        Start the crawling process and handle any exceptions that occur.
        Logs detailed errors and traceback information if any exception is raised.
        """
        self.console.log(f"正在啟動 {self.base_url} 爬蟲...")
        self._crawl()
      

    @classmethod
    def run_crawlers(cls, crawlers: List["BaseCrawler"], thread_count: int = 2):
        """
        運行多個爬蟲並決定執行緒數量。

        這個類方法會建立多個執行緒來執行多個爬蟲，每個執行緒會根據 thread_count 參數來決定執行的數量。
        爬蟲會分批次執行，每批次的執行緒數量根據 thread_count 決定。
        執行進度會使用進度條來顯示。

        Parameters:
        - crawlers (List[BaseCrawler]): 要執行的爬蟲列表。
        - thread_count (int, optional): 同時執行的執行緒數量。預設值是 2。

        Returns:
        None
        """
        start_time = time.time()

        threads = []
        with Progress() as progress:
            task = progress.add_task("[green]總進度", total=len(crawlers) * 100)

            def run_in_batches(batch_crawlers: List["BaseCrawler"]):
                for crawler in batch_crawlers:
                    crawler.start()

            # 將爬蟲分批次進行處理，每批次的執行緒數量根據 thread_count 決定
            for i in range(0, len(crawlers), thread_count):
                batch_crawlers = crawlers[i:i + thread_count]
                thread = threading.Thread(target=run_in_batches, args=(batch_crawlers,))
                threads.append(thread)
                thread.start()

            # 使用進度條顯示爬取進度
            while not progress.finished:
                progress.update(task, advance=10)
                time.sleep(0.1)

            for thread in threads:
                thread.join()
            
            cls.crawl_time = time.time() - start_time
        
        
       

        cls.display_results(crawlers)
        
    @staticmethod
    def display_results(crawlers: List["BaseCrawler"]):
        """顯示所有結果"""
        console = Console()
        table = Table(title="爬蟲結果")
        table.add_column("新聞來源", justify="left")
        table.add_column("總篇數", justify="right")

        for crawler in crawlers:
            print(crawler.crawl_time)
            crawl_time_str = f"{crawler.crawl_time:.2f} 秒"
            table.add_row(crawler.base_url, str(len(crawler.news_data)))

        console.print(table)