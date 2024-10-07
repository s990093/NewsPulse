import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import numpy as np

# 讀取文件
file_path = 'report.csv'
df = pd.read_csv(file_path)

# 提取連續數據和類別數據
# 假設 '收盤點數', '成交量', '漲跌幅' 是連續型數據，'政策受惠股', '股價表現' 是類別型數據
continuous_columns = ['收盤點數', '成交量', '漲跌幅']
categorical_columns = ['政策受惠股', '股價表現']

# 1. 對連續數據進行標準化
scaler = StandardScaler()
continuous_data = df[continuous_columns]  # 從 DataFrame 中提取連續數據
continuous_data_scaled = scaler.fit_transform(continuous_data)  # 標準化

# 2. 對類別型數據進行獨熱編碼
encoder = OneHotEncoder(sparse=False)
categorical_data = encoder.fit_transform(df[categorical_columns])  # 獨熱編碼

# 3. 將標準化後的連續數據和 One-Hot 編碼後的類別數據拼接
processed_data = np.hstack([continuous_data_scaled, categorical_data])

# 查看最終拼接後的結果
print(processed_data)
