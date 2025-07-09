import requests
from bs4 import BeautifulSoup
import os
import time

# 创建一个文件夹，用于保存图片
if not os.path.exists('果园爬取的图片'):
    os.makedirs('果园爬取的图片')

# 设置请求头，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
# 设置搜索关键词
keyword = '洛天依'

# 设置爬取的页数
page = 1

# 设置爬取的图片数量
num = 100

# 设置爬取的图片保存路径
path = '果园爬取的图片/'

# 循环爬取图片
while True:
    # 构造请求URL
    url = 'https://cn.bing.com/images/async?q=' + keyword + '&first=' + str((page - 1) * 35) + '&count=35&relp=35&lostate=r&mmasync=1&dgState=x1&exps=Async&ajaxRequest=1'
    # 发送请求
    response = requests.get(url, headers=headers)
    # 解析响应内容
    soup = BeautifulSoup(response.text, 'html.parser')
    # 获取图片链接
    img_urls = soup.find_all('img', {'class': 'mimg'})
    # 循环下载图片
    for img_url in img_urls:
        # 获取图片链接
        img_url = img_url['src']
        # 发送请求
        response = requests.get(img_url, headers=headers)
        # 保存图片
        with open(path + keyword + '_' + str(num) + '.jpg', 'wb') as f:
            f.write(response.content)
        # 输出进度
        print('已下载第' + str(num) + '张图片')
        # 下载一张图片后，暂停1秒，防止被封IP
        time.sleep(0.00000000000000000000000000001)
        # 下载一张图片后，图片数量减1
        num -= 1
        # 如果图片数量为0，则退出循环
        if num == 0:
            break
    # 如果图片数量为0，则退出循环
    if num == 0:
        break
    # 下载一页图片后，页数加1
    page += 1
# 输出完成信息
print('图片下载完成')
