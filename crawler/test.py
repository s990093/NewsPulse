from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import os

# 確保儲存目錄存在
output_dir = "data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 初始化 Selenium WebDriver
driver = webdriver.Chrome()  # 或者使用其他瀏覽器，例如 Firefox
driver.get("https://money.udn.com/money/vipbloomberg/time?from=edn_navibar")

# 用來存儲結果的列表
data = []

# 設置要爬取的故事數量
target_count = 100
current_count = 0

# CSV 文件名
csv_file = f"{output_dir}/nesurls.csv"

while current_count < target_count:
    # 每次開始前向下滑動3秒
    for _ in range(3):  # 滾動三次，每次間隔1秒
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(1)

    # 爬取所有 story__headline 元素
    elements = driver.find_elements(By.CSS_SELECTOR, "a.story__headline")    
    
    print(len(elements))
    # 只獲取最新的故事
    for element in elements:
        if current_count >= target_count:
            break
        
        title = element.get_attribute("title")  # 獲取 <a> 標籤的 title 屬性
        url = element.get_attribute("href")      # 獲取 <a> 標籤的 href 屬性
        data.append({"title": title, "url": url})
        
        current_count += 1
        
        # 每次獲取後寫入一次 CSV
        df = pd.DataFrame([{"title": title, "url": url}])  # 轉換為 DataFrame
        df.to_csv(csv_file, mode='a', index=False, header=not os.path.exists(csv_file), encoding='utf-8')
        print(f"已寫入 {current_count} 個故事到 CSV")

# 關閉瀏覽器
driver.quit()

