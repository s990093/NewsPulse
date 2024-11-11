#
# 抓單篇新聞(除錯用)
# 
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

# 設定與啟動瀏覽器
# vvv須依照chromedriver位置做更改vvv
ChromeDriverPath = "src\\crawler\\yahoo_news_crawler\\chromedriver.exe"

ChromeDriverPath = Service(ChromeDriverPath)#轉成 Service物件
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')  
chrome_options.add_argument('--ignore-ssl-errors')# 忽略 SSL 錯誤
chrome_options.add_argument('--disable-images')
chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")
chrome_options.add_experimental_option(
    "prefs",
    {
        "profile.default_content_setting_values.media_stream": 2, # 禁用多媒體流
        "profile.default_content_setting_values.plugins": 2,      # 禁用插件（如 Flash）
        "profile.default_content_setting_values.images": 2,        # 禁用圖片
    }
)
browser = webdriver.Chrome(service=ChromeDriverPath,options=chrome_options)

domain = "https://tw.yahoo.com/tv/morning-news"

url = "https://tw.tv.yahoo.com/morning-news/%E6%9B%9D%E8%B2%B7%E5%88%B0-%E7%99%BC%E9%9C%89%E6%B3%A1%E9%BA%B5-%E9%99%B3%E6%80%A1%E5%90%9B-%E6%89%93%E9%96%8B%E9%A3%84%E6%83%A1%E8%87%AD-075432367.html"

today_date = time.strftime("%Y-%m-%d", time.localtime())
print("today is:",today_date)
#  新聞網頁
# https://tw.tv.yahoo.com/morning-news/%E7%A7%9F%E9%87%91%E6%BC%B2-%E5%85%92%E5%A5%B3%E4%B8%8D%E6%8E%A5%E6%A3%92-%E9%B9%BF%E6%B8%AF60%E5%B9%B4%E7%B2%89%E7%B2%BF%E5%86%B0%E5%B0%87%E5%81%9C%E6%A5%AD-075557517.html
# https://tw.tv.yahoo.com/morning-news/%E6%9B%9D%E8%B2%B7%E5%88%B0-%E7%99%BC%E9%9C%89%E6%B3%A1%E9%BA%B5-%E9%99%B3%E6%80%A1%E5%90%9B-%E6%89%93%E9%96%8B%E9%A3%84%E6%83%A1%E8%87%AD-075432367.html
# https://tw.tv.yahoo.com/morning-news/%E9%A4%A8%E9%95%B7%E4%BB%A5%E8%87%AA%E8%BA%AB%E7%82%BA%E4%BE%8B%E7%A8%B1-%E7%B5%A6%E9%8C%A2%E5%BF%83%E7%94%98%E6%83%85%E9%A1%98-%E6%8C%BA%E6%9F%AF-%E5%BE%8B%E5%B8%AB-%E6%94%B6%E9%8C%A2%E5%8F%88%E5%9C%96%E5%88%A9%E5%B0%B1%E6%A7%8B%E6%88%90%E8%B2%AA%E6%B1%99-104603221.html
# https://tw.tv.yahoo.com/morning-news/%E6%8E%A7%E6%A9%9F%E8%BB%8A%E8%A1%8C%E6%95%B2%E7%AB%B9%E6%A7%93-%E7%94%B7%E5%AD%90%E7%8B%82%E5%88%B7-%E6%98%9F%E8%B2%A0%E8%A9%95%E9%82%84%E6%94%B9%E5%90%8D%E9%BB%91%E5%BA%97-%E6%A9%9F%E8%BB%8A%E8%A1%8C%E4%B9%9F%E8%A6%81%E6%8F%90%E5%91%8A-111603398.html
# https://tw.tv.yahoo.com/morning-news/%E9%A0%90%E6%B8%ACai%E8%B5%B0%E4%B8%8A-%E8%B6%85%E7%B4%9A%E6%91%A9%E7%88%BE%E5%AE%9A%E5%BE%8B-%E9%BB%83%E4%BB%81%E5%8B%B3-%E4%B8%96%E7%95%8C%E5%B7%B2%E7%B6%93%E8%AE%8A%E4%BA%86-104010486.html
# https://tw.tv.yahoo.com/morning-news/%E9%A7%95%E9%A7%9B%E9%96%8B%E8%BB%8A%E7%94%A8%E6%89%8B%E6%A9%9F-%E6%B2%92%E7%B9%AB%E5%AE%89%E5%85%A8%E5%B8%B6-%E9%81%87%E7%9B%A4%E6%9F%A5%E4%B8%8D%E9%85%8D%E5%90%88%E9%82%84%E8%A1%9D%E6%92%9E%E8%AD%A6-103627979.html
# https://tw.tv.yahoo.com/morning-news/%E7%8D%A8%E5%AE%B6-%E5%82%B3%E9%AB%98%E5%98%89%E7%91%9C%E6%8E%A5%E6%AC%A3%E6%AC%A3%E7%99%BE%E8%B2%A8%E8%91%A3%E8%A2%AB%E9%85%B8-%E8%AC%9D%E6%AC%A3%E9%9C%93-%E6%88%91%E6%9E%95%E9%A0%AD%E4%B9%BE%E6%B7%A8-121631864.html
# https://tw.tv.yahoo.com/morning-news/%E6%9C%89%E7%A5%9E%E9%BE%9C%E8%AB%8B%E5%B0%8F%E5%BF%83-%E8%B7%AF%E6%A8%99%E4%B8%8D%E6%98%AF%E6%83%A1%E4%BD%9C%E5%8A%87-%E7%9C%9F%E6%9C%89%E7%83%8F%E9%BE%9C%E5%87%BA%E6%B2%92-074246864.html
# https://tw.tv.yahoo.com/morning-news/2023%E6%B5%B7%E4%B8%8A%E8%B2%A8%E6%AB%83%E4%B8%9F%E5%A4%B1221%E5%80%8B-%E4%BD%86%E5%83%85%E6%9C%893%E6%88%90%E8%83%BD%E6%89%BE%E5%9B%9E-053200595.html
# https://tw.tv.yahoo.com/morning-news/%E9%87%91%E6%BE%8E%E6%B4%BE-%E5%BD%8C%E9%99%80%E8%99%B1%E7%9B%AE%E9%AD%9A%E7%AF%80%E5%B8%AD%E9%96%8B%E7%99%BE%E6%A1%8C-%E5%AE%A2-%E6%AF%8F%E5%B9%B4%E9%83%BD%E4%BE%86%E5%90%83-074428268.html
# https://tw.tv.yahoo.com/morning-news/%E8%A9%90%E5%9C%98%E9%BB%91%E5%90%83%E9%BB%91-19%E6%AD%B2%E8%BB%8A%E6%89%8B%E7%A7%81%E5%90%9E100%E8%90%AC-%E9%81%AD%E8%A8%AD%E5%B1%80%E6%9A%B4%E6%89%93-074444521.html
# https://tw.tv.yahoo.com/%E6%8D%B7%E5%85%8B%E6%A3%92%E7%90%83%E9%9A%8A%E5%8F%83%E8%A8%AA%E9%BE%8D%E5%B1%B1%E5%AF%BA-%E6%8A%95%E6%89%8B%E5%B8%A5%E7%BF%BB-%E7%90%83%E8%BF%B7%E7%9B%AE%E4%B8%8D%E8%BD%89%E7%9D%9B-%E9%8F%A1%E6%96%B0%E8%81%9E-120134856.html
# https://tw.tv.yahoo.com/morning-news/%E6%96%87%E7%AD%96%E9%99%A2-%E5%89%B5%E6%84%8F%E5%86%85%E5%AE%B9%E5%A4%A7%E6%9C%83-%E5%9C%93%E6%BB%BF%E8%90%BD%E5%B9%95-%E7%9B%BC%E6%8B%93%E5%B1%95%E5%9C%8B%E9%9A%9B%E5%B8%82%E5%A0%B4-160010578.html
# https://tw.tv.yahoo.com/morning-news/%E5%B7%9D%E6%99%AE%E5%8B%9D%E9%81%B8%E6%8A%95%E8%B3%87%E5%B8%83%E5%B1%80%E6%9B%9D%E5%85%89-%E9%81%94%E4%BA%BA-%E9%80%99%E4%B8%89%E9%A1%9E%E8%82%A1%E5%B0%87%E6%88%90%E7%82%BA%E6%9C%80%E5%A4%A7%E8%B4%8F%E5%AE%B6-091604516.html
# https://tw.tv.yahoo.com/ftv/%E5%AE%B6%E6%97%8F%E5%9D%90%E6%93%81%E6%95%B8%E8%99%95%E8%B1%AA%E5%AE%85-%E5%8D%BB%E4%BD%94%E7%94%A8%E5%AE%98%E8%88%8D-%E8%94%A3%E8%90%AC%E5%AE%89%E5%9B%9E%E6%87%89%E4%BA%86-040000809.html
# https://tw.tv.yahoo.com/morning-news/%E9%9B%B2%E7%AB%AF%E7%99%BC%E7%A5%A8-%E9%87%8D%E8%A6%86%E4%B8%AD%E7%8D%8E-%E9%BB%91%E7%AE%B1-%E6%8A%BD%E7%8D%8E%E9%81%94%E4%BA%BA-%E8%AA%BF%E6%95%B4%E6%AC%8A%E9%87%8D%E4%B8%8D%E5%85%AC%E5%B9%B3-152713783.html
# https://tw.yahoo.com/tv/morning-news

# 進入網頁
browser.get(url) 

# 等待頁面跑完
time.sleep(3)

# 儲存所有新聞標題和連結
news_links = []
check = []
titles = []
last_height = browser.execute_script("return document.body.scrollHeight")

# 抓取新聞內容
# news_elements = browser.find_elements(By.CSS_SELECTOR, 'a')#'a.text-GreyHair'
#videoInfo > div:nth-child(4) > div.text-sm.text-Bob.overflow-hidden
try:
    try:
        #videoInfo > div:nth-child(4) > div.flex.items-center.justify-center.mt-1 > button
        b = browser.find_element(By.CLASS_NAME, 'flex.items-center.justify-center.mt-1')
        if b:
            b.click()
    except Exception as e:
        print("",end="")

    title = browser.find_element(By.TAG_NAME, 'h2')
    #video_info_div = browser.find_element(By.CLASS_NAME, 'text-sm.text-Bob.overflow-hidden')
    #paragraphs = video_info_div.find_elements(By.CSS_SELECTOR, 'p')#By.TAG_NAME, "p"
    try:
        paragraphs = browser.find_elements(By.TAG_NAME, "p")
        content = " ".join([p.text for p in paragraphs])  # 拼接所有非空文本段落
        try:
            if len(content)< 5:
                paragraphs = browser.find_element(By.CSS_SELECTOR, "div.text-sm.text-Bob.overflow-hidden.line-clamp-8")
                content = paragraphs.text
        except Exception as e:
            paragraphs = browser.find_element(By.CSS_SELECTOR, "div.text-sm.text-Bob.overflow-hidden")
            content = paragraphs.text
    except Exception as e:
        print("抓取內容失敗",e)
        content = "not found"

    try:
        try:
            time_element = browser.find_element(By.CSS_SELECTOR, "div.flex-wrap.text-sm.text-Bob.mt-1 > div:nth-child(2)")
            print("0")
        except Exception as e:
            # 嘗試其他方法
            try:
                #videoInfo > div.flex.flex-wrap.text-sm.text-Bob.mt-1 > div.mb-1 
                time.sleep(1)
                time_element = browser.find_element(By.CSS_SELECTOR, "div.flex.flex-wrap.text-sm.text-Bob.mt-1 > div.mb-1")
                print("1")
            except Exception as e:
                # 嘗試其他方法
                #videoInfo > div.flex.flex-wrap.text-sm.text-Bob.mt-1 > div:nth-child(2)            
                try:               
                    time_element = browser.find_element(By.CSS_SELECTOR, "div.flex.flex-wrap.text-sm.text-Bob.mt-1 > div:nth-child(2)")
                    print("2")
                except Exception as e:
                    try:
                        time_element = browser.find_element(By.CSS_SELECTOR, "videoInfo > div.flex.flex-wrap.text-sm.text-Bob.mt-1 > div:nth-child(2)")
                        print("3")
                    except Exception as e:
                        time_element = browser.find_element(By.XPATH, "//*[@id='videoInfo']/div[1]/div[2]")
                        print("4")
    
        relative_time = time_element.text.split("・")[1]
        #print("相對發布時間:", relative_time)
        # 解析「? 小時前」並轉換為具體時間
        hours_ago = int(relative_time.split(" ")[0])  # 假設格式為 "? 小時前"
        publish_time = datetime.now() - timedelta(hours=hours_ago)
        publish_time = publish_time.strftime("%Y-%m-%d %H:%M")
    except Exception as e:
        print("抓取時間失敗",e)

    if today_date in publish_time:
        print("today's news")
    else:
        print("not today's news")

    parsed_url = urlparse(url)
    news_uuid = parsed_url.path.split('-')[-1].split('.')[0]

    print("新聞 UUID:", news_uuid)
    print("新聞發布時間:", publish_time)
    print("\n新聞標題:", title.text)  
    print("\n新聞内容:", content)
    print("\n域名:", domain)
    print("\n網址:", url)



except Exception as e:
    print("抓取新聞内容失敗:", e)
finally:
    # 關閉瀏覽器
    browser.quit()

"""
for news in news_elements:
    #取得連結
    link = news.get_attribute('href')
    if "/morning-news/" in link and link not in check:
        #儲存連結
        news_links.append(link)
        check.append(link)

        #取得連結標題並只保留中文字部分
        data_ylk = news.get_attribute('data-ylk')
        title_match = re.search(r'slk:(.*?);', data_ylk)
        title = title_match.group(1) if title_match else "No title found(或首頁最上面的新聞)"
        #儲存連結標題       
        titles.append(title)

#列出抓取內容
for index, (link, title) in enumerate(zip(news_links, titles), start=1):   
    print(index,". ", title)
    print(link,"\n")
"""


