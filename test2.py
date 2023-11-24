# 数据请求模块
import requests
 
# 模拟浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
# 请求链接
url = 'https://b.faloo.com/1328711_1.html'
# 发送请求
requests = requests.get(url=url, headers=headers)
print(requests.text)
