#
# ********************
# yahoo晨間新聞網頁爬蟲
# ********************
# 11/11-yahoo晨間新聞網頁爬蟲完成
#
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime, timedelta
import re
from urllib.parse import urlparse

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from src.crawler.base_crawler import *

class YahooNewsCrawler(BaseCrawler):
    def __init__(self, base_url: str, options: Options = Options(), article_limit: int = 100):
        super().__init__(base_url, options, article_limit)
    
    def fetch_news(self) -> NewsList:
        news_list: NewsList = []  # Initialize a list, using NewsList only as a type hint
        # 設定與啟動瀏覽器
        # *********************注意事項****************************
        # 因為使用 service=Service(ChromeDriverManager().install()) 有問題(原因未知)
        # 所以使用 service=Service(ChromeDriverPath) 
        # 其中 ChromeDriverPath 須依照chromedriver位置做更改
        # 現在路徑是: src\crawler\yahoo_news_crawler\chromedriver.exe
        # 放到ChromeDriverPath內的路徑，" \ " 要改成 " \\ "
        # *********************************************************
        ChromeDriverPath = "src\\crawler\\yahoo_news_crawler\\chromedriver.exe"

        ChromeDriverPath = Service(ChromeDriverPath)#轉成 Service物件

        # option 設定
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')  
        chrome_options.add_argument('--ignore-ssl-errors') # 忽略 SSL 錯誤
        chrome_options.add_argument('--disable-images') # 禁用圖片
        chrome_options.add_argument("--autoplay-policy=no-user-gesture-required") # 禁用自動播放影片
        chrome_options.add_argument("--disable-popup-blocking") 
        chrome_options.add_argument("--disable-notifications") # 禁用通知
        chrome_options.add_argument('--headless') # 不開視窗
        chrome_options.add_experimental_option(
            "prefs",
            {
                "profile.default_content_setting_values.media_stream": 2, # 禁用多媒體流
                "profile.default_content_setting_values.plugins": 2,      # 禁用插件（如 Flash）
                "profile.default_content_setting_values.images": 2,        # 禁用圖片
            }
        )
        # 初始化WebDriver
        browser = webdriver.Chrome(service=ChromeDriverPath,options=chrome_options)

        # 取得今天日期
        today_date = time.strftime("%Y-%m-%d", time.localtime())

        # 設置隱式等待時間為 10 秒
        browser.implicitly_wait(10)

        # 進入網頁
        domain = "https://tw.yahoo.com/tv/morning-news"
        browser.get(domain) 

        # 等待頁面跑完
        time.sleep(3)

        # 儲存所有新聞連結
        news_links = []
        # 檢查新聞連結是否已存在
        check = []

        # 滾動捲軸到網頁的底部
        try:
            last_height = browser.execute_script("return document.body.scrollHeight")
            while True:
                # 滾動到頁面底部
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # 檢查頁面是否已到底(無法再滾動)
                new_height = browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:  # 已到底部
                    break
                last_height = new_height
        except Exception as e:
                print("滾動到網頁失敗",e)

        # 抓取所有新聞連結
        try:
            news_elements = browser.find_elements(By.CSS_SELECTOR, 'a')# 'a.text-GreyHair'
            for news in news_elements:
                #取得連結
                link = news.get_attribute('href') 
                
                if ("/morning-news/" in link ) and link not in check:
                    #儲存連結
                    news_links.append(link)
                    check.append(link)
        except Exception as e:
                print("抓新聞連結失敗",e)

        # 進入每個抓取來的新聞連結，抓取新聞的各項資訊
        # 抓取個數取 新聞連結總數 和 文章限制 的最小值
        for i in range(min(len(news_links), self.article_limit)):  
            url = news_links[i] # 取得新聞連結  
            browser.get(url) # 進入新聞頁面  
            time.sleep(3) # 等待頁面跑完

            # 點擊yahoo新聞頁面的[展開更多内容]按鈕(如果有的話)，以確保能抓取完整新聞資訊
            try: 
                #videoInfo > div:nth-child(4) > div.flex.items-center.justify-center.mt-1 > button
                b = browser.find_element(By.CLASS_NAME, 'flex.items-center.justify-center.mt-1')
                if b:
                    b.click()
            except Exception as e:
                print("",end="") # 無需展開更多内容

          
            # 抓取新聞時間(yahoo新聞的時間屬於相對時間:?小時前 or ?分鐘前 or )
            # 並轉為實際時間(當相對時間是 ?小時前，"分"的部分與真實時間有落差)
            #        (當相對時間是  ? 天前，"時"、"分"的部分與真實時間有落差)   
            try:
                try:
                    time.sleep(1)
                    time_element = browser.find_element(By.CSS_SELECTOR, "div.flex-wrap.text-sm.text-Bob.mt-1 > div:nth-child(2)")
                except Exception as e:
                    # 嘗試其他方法
                    try:
                        #videoInfo > div.flex.flex-wrap.text-sm.text-Bob.mt-1 > div.mb-1 
                        #time.sleep(1)
                        time_element = browser.find_element(By.CSS_SELECTOR, "div.flex.flex-wrap.text-sm.text-Bob.mt-1 > div.mb-1")
                    except Exception as e:
                        # 嘗試其他方法
                        #videoInfo > div.flex.flex-wrap.text-sm.text-Bob.mt-1 > div:nth-child(2)          
                        try: 
                            # 嘗試其他方法              
                            time_element = browser.find_element(By.CSS_SELECTOR, "div.flex.flex-wrap.text-sm.text-Bob.mt-1 > div:nth-child(2)")
                        except Exception as e:
                            try:
                                # 嘗試其他方法
                                time_element = browser.find_element(By.CSS_SELECTOR, "videoInfo > div.flex.flex-wrap.text-sm.text-Bob.mt-1 > div:nth-child(2)")
                            except Exception as e:
                                # 嘗試其他方法
                                time_element = browser.find_element(By.XPATH, "//*[@id='videoInfo']/div[1]/div[2]")

                try:     
                    relative_time = time_element.text.split("・")[1]
                except Exception as e:
                    relative_time = time_element.text
                # 解析「?小時前 or ?分鐘前 or ? 天前」並轉換為具體時間
                if "天前" in relative_time:
                    # 非今天新聞，所以不抓，直接抓下一則新聞
                    continue
                elif "小時前" in relative_time:
                    r_time = int(relative_time.split(" ")[0])
                    publish_time = datetime.now() - timedelta(hours=r_time)
                elif "分鐘前" in relative_time:
                    r_time = int(relative_time.split(" ")[0])
                    publish_time = datetime.now() - timedelta(minutes=r_time)
                else:
                    # 如果格式不符合，改記錄當前時間
                    publish_time = datetime.now()

                publish_time = publish_time.strftime("%Y-%m-%d %H:%M")
            except Exception as e:
                print(url,"\n抓取時間失敗",e)
                publish_time = today_date
   
            # 抓取新聞標題
            try:
                title = browser.find_element(By.TAG_NAME, 'h2')
                news_title = title.text
            except Exception as e:
                print(url,"抓取標題失敗",e)
                news_title = "not found"
    
            # 抓取新聞內容
            try:
                paragraphs = browser.find_elements(By.TAG_NAME, "p")
                content = " ".join([p.text for p in paragraphs])  # 拼接所有非空文章段落

                # 當網頁沒有<p></p>的時候，用其他方式抓
                try:
                    if len(content)< 5:
                        paragraphs = browser.find_element(By.CSS_SELECTOR, "div.text-sm.text-Bob.overflow-hidden.line-clamp-8")
                        content = paragraphs.text
                except Exception as e:
                    paragraphs = browser.find_element(By.CSS_SELECTOR, "div.text-sm.text-Bob.overflow-hidden")
                    content = paragraphs.text
            except Exception as e:
                print(url,"抓取內容失敗",e)
                content = "not found"
    
            # 抓取新聞uuid(從url中取得)
            try:
                parsed_url = urlparse(url)
                news_uuid = parsed_url.path.split('-')[-1].split('.')[0]
            except Exception as e:
                print(url,"抓取uuid失敗",e)
                news_uuid = "not found"

            # 儲存完整新聞資訊
            news_list.append({
                        "id": news_uuid,
                        "time": publish_time,
                        "title": news_title,
                        "content": content,
                        "url": url,
                        "domain": domain
                    })
            
        # 關閉瀏覽器
        browser.quit()        
        return news_list
    
    # 測試用，抓取並列出所有新聞的各項資訊
    def print_news(self):
        N_List = self.fetch_news()
        for x in N_List:
            print("新聞 UUID:",x['id'])
            print("新聞發布時間:",x['time'])
            print("新聞標題:",x['title'])
            print("新聞内容:",x['content'])
            # print("域名:",x['domain'])
            print("網址:",x['url'])
            print('-'*20)

# 使用範例
yahoo_crawler = YahooNewsCrawler("https://tw.yahoo.com/tv/morning-news", article_limit=20)
#yahoo_crawler.start()
yahoo_crawler.print_news()   
"""
for x in N_List:
    print("新聞 UUID:",x['id'])
    print("新聞發布時間:",x['time'])
    print("新聞標題:",x['title'])
    print("新聞内容:",x['content'])
    # print("域名:",x['domain'])
    print("網址:",x['url'])
    print('-'*20)
"""
