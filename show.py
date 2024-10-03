import pandas as pd

# 讀取 CSV 檔案
df = pd.read_csv('data/csv/report.csv')

# # 移除重複的 ID

# 將 index 賦值給 ID 列
df['ID'] = df.index

# 儲存處理後的資料
df.to_csv('data/news_data_with_index_as_id.csv', index=False)

# 顯示前幾行來確認結果
print(df.head())
