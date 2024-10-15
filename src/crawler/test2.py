import requests

# 代理信息（如果需要）
proxy = "219.100.37.193"  # 代理 IP
username = "vpn"          # 代理用户名
password = "vpn"          # 代理密码

# 设置代理
proxies = {
    "http": f"http://{username}:{password}@{proxy}",
    "https": f"http://{username}:{password}@{proxy}",
}

# 请求的 URL
url = "https://www.wealth.com.tw/articles/94f6378c-fa52-4c7b-960f-245739d7a346"

try:
    # 发送请求
    response = requests.get(url, proxies=proxies, timeout=10)
    response.raise_for_status()  # 检查请求是否成功

    # 打印响应内容
    print(response.text)

except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
