# 写一个爬虫，爬取https://www.duitang.com/album/?id=102795314 的内容，并保存到本地
import requests
from bs4 import BeautifulSoup
import os

# 创建文件夹
if not os.path.exists('-17我CNM'):
    os.makedirs('-17我CNM')

# 发送请求
url = 'https://www.duitang.com/album/?id=102795314'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0'
}
response = requests.get(url, headers=headers)

# 解析页面
soup = BeautifulSoup(response.text, 'html.parser')
images = soup.find_all('img')

# 保存图片
for i, image in enumerate(images):
    image_url = image['src']
    response = requests.get(image_url, headers=headers)
    with open(f'-17我CNM/{i}.jpg', 'wb') as f:
        f.write(response.content)
print('爬取完成！')

