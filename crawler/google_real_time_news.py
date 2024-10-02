"""
Google新聞即時爬蟲
程式碼撰寫: 蘇彥庭
日期: 20210111

2023/04/08程式修改
1. 處理Google RSS連結: 原本為新聞連結 現在被改為Google頁面連結 連結該Google頁面後才會被轉向實際新聞連結
2. 修改經濟日報新聞內容抓取方式

2024/08/14程式修改
1. 處理日期轉換問題
2. 處理Google RSS連結問題 
採用此Github專案: https://github.com/SSujitX/google-news-url-decoder/tree/main 
提供的Decoder取得正確新聞網址(但實測部分網址可能還是會解析錯誤)
3. 修改鉅亨網新聞內容爬蟲程式碼
"""

# 載入套件
import json
import requests
import pandas as pd
import time
import re
from bs4 import BeautifulSoup
import datetime
import base64
from urllib.parse import quote, urlparse

# 參數設定
# 欲下載新聞的股票關鍵字清單
searchList = ['經濟',]
# 新聞下載起始日
nearStartDate = (datetime.date.today() + datetime.timedelta(days=-10)).strftime('%Y-%m-%d')


# google-news-url-decoder
def fetch_decoded_batch_execute(id):
    s = (
    '[[["Fbv4je","[\"garturlreq\",[[\"en-US\",\"US\",[\"FINANCE_TOP_INDICES\",\"WEB_TEST_1_0_0\"],'
    'null,null,1,1,\"US:en\",null,180,null,null,null,null,null,0,null,null,[1608992183,723341000]],'
    '\"en-US\",\"US\",1,[2,3,4,8],1,0,\"655000234\",0,0,null,0],\"' +
    id +
    '\"]",null,"generic"]]]'
    )

    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        "Referer": "https://news.google.com/"
    }

    response = requests.post(
        "https://news.google.com/_/DotsSplashUi/data/batchexecute?rpcids=Fbv4je",
        headers=headers,
        data={"f.req": s}
    )

    if response.status_code != 200:
        print(response.status_code)
        raise Exception("Failed to fetch data from Google.")

    text = response.text
    header = '[\\"garturlres\\",\\"'
    footer = '\\",'
    if header not in text:
        raise Exception(f"Header not found in response: {text}")
    start = text.split(header, 1)[1]
    if footer not in start:
        raise Exception("Footer not found in response.")
    url = start.split(footer, 1)[0]
    return url


def decode_urls(articles):
    articles_reqs = [
        [
            "Fbv4je",
            f'["garturlreq",[["X","X",["X","X"],null,null,1,1,"US:en",null,1,null,null,null,null,null,0,1],"X","X",1,[1,1,1],1,1,null,0,0,null,0],"{art["gn_art_id"]}",{art["timestamp"]},"{art["signature"]}"]',
        ]
        for art in articles
    ]
    payload = f"f.req={quote(json.dumps([articles_reqs]))}"
    headers = {"content-type": "application/x-www-form-urlencoded;charset=UTF-8"}
    response = requests.post(
        url="https://news.google.com/_/DotsSplashUi/data/batchexecute",
        headers=headers,
        data=payload,
    )
    response.raise_for_status()
    return [json.loads(res[2])[1] for res in json.loads(response.text.split("\n\n")[1])[:-2]]


def get_decoding_params(gn_art_id):
    response = requests.get(f"https://news.google.com/articles/{gn_art_id}")
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    div = soup.select_one("c-wiz > div")
    return {
        "signature": div.get("data-n-a-sg"),
        "timestamp": div.get("data-n-a-ts"),
        "gn_art_id": gn_art_id,
    }


# google-news-url-decoder
def decode_google_news_url(source_url):
    url = requests.utils.urlparse(source_url)
    
    
    
    path = url.path.split("/")
    
    
    if url.hostname == "news.google.com" and len(path) > 1 and path[-2] == "articles":
        base64_str = path[-1]
        decoded_bytes = base64.urlsafe_b64decode(base64_str + "==")
        decoded_str = decoded_bytes.decode("latin1")

        prefix = b"\x08\x13\x22".decode("latin1")
        if decoded_str.startswith(prefix):
            decoded_str = decoded_str[len(prefix) :]

        suffix = b"\xd2\x01\x00".decode("latin1")
        if decoded_str.endswith(suffix):
            decoded_str = decoded_str[: -len(suffix)]

        bytes_array = bytearray(decoded_str, "latin1")
        length = bytes_array[0]
        if length >= 0x80:
            decoded_str = decoded_str[2 : length + 1]
        else:
            decoded_str = decoded_str[1 : length + 1]
    

        if decoded_str.startswith("AU_yqL"):
            return decode_urls(base64_str)

        return decoded_str
    else:
        return source_url
    

# 整理Google新聞資料用
def arrangeGoogleNews(elem):
    return ([elem.find('title').getText(),
             elem.find('link').getText(),
             elem.find('pubDate').getText(),
             BeautifulSoup(elem.find('description').getText(), 'html.parser').find('a').getText(),
             elem.find('source').getText()])


# 擷取各家新聞網站新聞函數
def beautifulSoupNews(url):

    # 設定hearers
    headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0'
}

    # 取得Google跳轉頁面的新聞連結
    # newsUrl = decode_google_news_url(url)
    encoded_urls = [url]
    articles_params = [get_decoding_params(urlparse(url).path.split("/")[-1]) for url in encoded_urls]
    newsUrl = decode_urls(articles_params)[0]
    

    # 取得該篇新聞連結內容
    response = requests.get(newsUrl, headers=headers)
    
    soup = BeautifulSoup(response.text, 'html.parser') 
    
    

    # 判斷url網域做對應文章擷取
    try:
        domain = re.findall('https://[^/]*', newsUrl)[0].replace('https://', '')
        print(domain)
    except:
        print(f'網址解析錯誤: {newsUrl}')
        content = 'unknow domain'
        return newsUrl, content

    if domain == 'udn.com':

        # 聯合新聞網
        item = soup.find_all('section', class_='article-content__editor')[0].find_all('p')
        content = [elem.getText() for elem in item]
        content = ''.join(content)
        content = content.replace('\r', ' ').replace('\n', ' ')

    elif domain == 'ec.ltn.com.tw':

        # 自由財經
        item = soup.find_all('div', class_='text')[0].find_all('p', class_='')
        content = [elem.getText() for elem in item]
        content = ''.join(content)
        content = content.replace('\r', ' ').replace('\n', ' ').replace(u'\xa0', ' '). \
            replace('一手掌握經濟脈動', '').replace('點我訂閱自由財經Youtube頻道', '')

    elif domain in ['tw.stock.yahoo.com', 'tw.news.yahoo.com']:

        # Yahoo奇摩股市
        item = soup.find_all('div', class_='caas-body')[0].find_all('p')
        content = [elem.getText() for elem in item]
        del_text = soup.find_all('div', class_='caas-body')[0].find_all('a')
        del_text = [elem.getText() for elem in del_text]
        content = [elem for elem in content if elem not in del_text]
        content = ''.join(content)
        content = content.replace('\r', ' ').replace('\n', ' ').replace(u'\xa0', ' ')

    elif domain == 'money.udn.com':

        # 經濟日報
        item = soup.find_all('section', id='article_body')[0].find_all('p')
        content = [elem.getText() for elem in item]
        content = [elem for elem in content]
        content = ''.join(content)
        content = content.replace('\r', ' ').replace('\n', ' ')

    elif domain == 'www.chinatimes.com':

        # 中時新聞網
        item = soup.find_all('div', class_='article-body')[0].find_all('p')
        content = [elem.getText() for elem in item]
        content = [elem for elem in content]
        content = ''.join(content)
        content = content.replace('\r', ' ').replace('\n', ' ')

    elif domain == 'ctee.com.tw':

        # 工商時報
        item = soup.find_all('div', class_='entry-content clearfix single-post-content')[0].find_all('p')
        content = [elem.getText() for elem in item]
        content = [elem for elem in content]
        content = ''.join(content)
        content = content.replace('\r', ' ').replace('\n', ' ')

    elif domain == 'news.cnyes.com':

        # 鉅亨網
        sections = soup.find_all('section', style='margin-top:30px')
        content = list()
        for section in sections:
            p_tag = section.find('p')
            if p_tag:
                content.append(p_tag.getText())
        content = ''.join(content)
        content = content.replace('\r', ' ').replace('\n', ' ').replace(u'\xa0', ' ')

    elif domain == 'finance.ettoday.net':

        # ETtoday
        item = soup.find_all('div', itemprop='articleBody')[0].find_all('p')
        content = [elem.getText() for elem in item]
        content = [elem for elem in content]
        content = ''.join(content)
        content = content.replace('\r', ' ').replace('\n', ' ').replace(u'\xa0', ' ')

    elif domain == 'fnc.ebc.net.tw':

        # EBC東森財經新聞
        content = str(soup.find_all('script')[-2]).split('ReactDOM.render(React.createElement(')[1]
        content = content.split(',')[1].replace('{"content":"', '').replace('"})', '')
        content = re.sub(u'\\\\u003[a-z]+', '', content)
        content = content.replace('/p', ' ').replace('\\n', '')

    else:

        # 未知domain
        
        print(f"未知domain -> {domain}")
        content = 'unknow domain'

    return newsUrl, content


if __name__ == '__main__':

    # 迴圈下載股票清單的Google新聞資料
    stockNews = pd.DataFrame()
    for iSearch in range(len(searchList)):

        try:
            print('目前正在搜尋股票: ' + searchList[iSearch] +
                ' 在Google的新聞清單  進度: ' + str(iSearch + 1) + ' / ' + str(len(searchList)))

            # 建立搜尋網址
            url = 'https://news.google.com/news/rss/search/section/q/' + \
                searchList[iSearch] + '/?hl=zh-tw&gl=TW&ned=zh-tw_tw'
            response = requests.get(url)
            response.raise_for_status()  # 檢查 HTTP 請求狀態
            soup = BeautifulSoup(response.text, 'xml')
            item = soup.find_all('item')
            rows = [arrangeGoogleNews(elem) for elem in item]

            # 組成pandas
            df = pd.DataFrame(data=rows, columns=['title', 'link', 'pub_date', 'description', 'source'])
            # 新增時間戳記欄位
            df.insert(0, 'search_time', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), True)
            # 新增搜尋字串
            df.insert(1, 'search_key', searchList[iSearch], True)
            # 篩選最近的新聞
            df['pub_date'] = pd.to_datetime(df['pub_date'])
            df = df[df['pub_date'] >= nearStartDate]
            # 按發布時間排序
            df = df.sort_values(['pub_date']).reset_index(drop=True)

            # 迴圈爬取新聞連結與內容
            newsUrls = list()
            contents = list()

            for iLink in range(len(df['link'])):
                try:
                    print('目前正在下載: ' + searchList[iSearch] +
                        ' 各家新聞  進度: ' + str(iLink + 1) + ' / ' + str(len(df['link'])))

                    newsUrl, content = beautifulSoupNews(url=df['link'][iLink])
                    newsUrls.append(newsUrl)
                    contents.append(content)
                    time.sleep(1)

                except Exception as e:
                    print(f"新聞下載錯誤 (股票: {searchList[iSearch]}, 連結: {df['link'][iLink]}): {e}")
                    newsUrls.append(None)  # 如果失敗，加入None以保持資料一致性
                    contents.append(None)

            # 新增新聞連結與內容欄位
            df['newsUrl'] = newsUrls
            df['content'] = contents

            # 儲存資料
            stockNews = pd.concat([stockNews, df])

        except Exception as e:
            print(f"搜尋股票錯誤 (股票: {searchList[iSearch]}): {e}")

    # 輸出結果檢查
    try:
        stockNews.to_csv('checkData.csv', index=False, encoding='utf-8-sig')
    except Exception as e:
        print(f"儲存資料錯誤: {e}")
