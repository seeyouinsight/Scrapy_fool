import json
import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from colorama import Fore
from tqdm import tqdm
from win10toast import ToastNotifier
import re
servers = 'https:'
def search1():
    # tar='https://b.faloo.com/l/0/1.html?t=1&k={}'
    bookName = input("请输入小说的名字：")
    str1 = bookName.encode('unicode_escape').decode()  # 编码成\u形式 decode后变成字符串类型
    str1 = str1.replace('\\', '%')  # 编码成%u 形式   特定的url编码

    tar = 'https://b.faloo.com/l/0/1.html?t=1&k=' + str1  # 拼接链接 将编码后的参数（即搜索的小说名字）拼接上

    print(tar)  # 验证链接

    souce = requests.get(tar, timeout=60)  # 发起页面请求
    # print('***', souce)
    html = souce.text  # 获取返回的页面html文本
    div_bf = BeautifulSoup(html, "lxml")  # 用lxml解析器解析html页面
    div = div_bf.find_all('h1')  # 获得 html 信息中所有 h1 标签。

    # 遍历h1文本，如果遍历中有某个小说名等于搜索的小说名字，则将小说名字的链接赋值给target
    for i in div:
        print(i)
        print(str(i.getText()) + str(i.a.get('href')))  # getText()方法获取文本  ，i.a.get('href') 获取h1下一级（子）a标签的href
        if i.getText() == bookName:
            target = servers + i.a.get('href')  # 将https 和匹配到的链接拼接
            return target  # 返回链接

music_list = []

def search2():
    author = input("请输入小说作者名字：")
    str2 = author.encode('unicode_escape').decode()  # 编码成\u形式 decode后变成字符串类型
    str2 = str2.replace('\\', '%')  # 编码成%u 形式   特定的url编码
    tar = 'https://b.faloo.com/l/0/1.html?t=1&k=' + str2  # 拼接链接 将编码后的参数（即搜索的小说名字）拼接上
    souce = requests.get(tar, timeout=60)  # 发起页面请求
    # print('***', souce)
    html = souce.text  # 获取返回的页面html文本
    div_bf = BeautifulSoup(html, "lxml")  # 用lxml解析器解析html页面
    # 作者
    div = div_bf.find_all('span', attrs={'class': 'fontSize14andsHui'})  # 获得 html 信息中所有 h1 标签。
    # 小说名
    name = div_bf.find_all('h1')

    # 遍历h1文本，如果遍历中有某个小说名等于搜索的小说名字，则将小说名字的链接赋值给target
    print('*' * 200)
    print('{0:{4}<5}{1:{4}<20}{2:{4}<20}{3:{4}<25}'
          .format('序号', '小说名', '作者', '小说链接', chr(12288)))
    print('-' * 200)
    xs_dict = {
        'id': [],
        'name': [],
        'url': [],
        'singer': []
    }
    for i in range(len(name)):
        xs_dict["id"].append(i)
        xs_dict["name"].append(name[i].string)

        xs_dict["url"].append(servers + name[i].a.get('href'))
        xs_dict["singer"].append(div[i].text)
        # music_list.append(xs_dict)
    for i in range(len(xs_dict['id'])):
        print('{0:{4}<5}{1:{4}<22}{2:{4}<20}{3:{4}<25}'
              .format(xs_dict['id'][i], xs_dict['name'][i], xs_dict['singer'][i], xs_dict['url'][i],
                      chr(12288)), sep=' ')
    print('*' * 200)
    print(xs_dict)
    lianjie = xs_dict['url']
    idc = xs_dict['id']
    select = int(input('请选择小说：'))
    url = lianjie[select]
    return url

    # print(str(i.getText()) + str(i.a.get('href')))  # getText()方法获取文本  ，i.a.get('href') 获取h1下一级（子）a标签的href
    # if i.getText() == b:
    #     target = servers + i.a.get('href')  # 将https 和匹配到的链接拼接
    #     return target  # 返回链接


def get_download_url(target):

    print(target)  # 输出返回的链接
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36 Edg/91.0.864.53'
    }

    req = requests.get(url=target, headers=headers)
    html = req.text  # 获取页面html文本
    bf = BeautifulSoup(html, "lxml")  # 解析html
    print('-----------------------')
    # print(bf)

    alist = bf.find_all('a', class_='c_con_li_detail')  # 匹配
    print(alist)
    if not alist:
        alist = bf.find_all('div', attrs={'class': 'DivTd'})
    print(alist)

    l = []

    # print(html)
    book_name = bf.find('h1')  # 获取 h1 小说名字
    # 异常 搜索小说 若小说不存在则返回异常输出异常信息 ，反之小说存在则显示搜索成功

    try:
        book_name = book_name.getText()  # 请求url 获取响应文本
        if book_name:
            print('小说已搜索成功')  # 若book_name成功获取文本，则输出搜索成功
            print(book_name)
    except Exception as e:
        print('小说不存在')
        print(e)
        sys.exit()
    finally:
        time.sleep(2)
    book_name = book_name.strip("\r\n目录")  # 书名去除首尾换行符
    # book_name = book_name.replace("\n", "--")  # 将标题内的换行符以--代替

    # 如果磁盘中存在book_name（书名）文件夹，则不创建，如果不存在，则创建{书名}文件夹
    if not os.path.exists(book_name):
        os.makedirs(book_name)

    print(f'《{book_name}》开始下载：')
    k = int(input("请输入要下载的章节数"))
    for i in range(len(alist[:k])):
        print(i)
        naurl = {}

        try:
            naurl['章节名'] = alist[i].a.string
            naurl['章节链接'] = servers + alist[i].a.get('href')
            l.append(naurl)

        except Exception as e:
            print(e)
            del alist[i]
            k-=1

        # names.append(i.string)
        # a_url.append(i.get('href'))
        # naurl['章节名'] = i.a.string
        # naurl['章节链接'] = servers + i.a.get('href')

    print('ddd***************************', l)
    for j in tqdm(range(k), bar_format='{l_bar}%s{bar}%s{r_bar}' % (Fore.LIGHTGREEN_EX, Fore.RESET)):
        # print(l[i]['章节链接'])
        wjm = str(j + 1) + '- ' + l[j]['章节名']
        wjm=re.sub('（\d/\d）','',wjm)

        writer(wjm, book_name, get_contents(l[j]['章节链接']))
    return book_name

def get_contents(target):
    req = requests.get(url=target)
    html = req.text
    # print(html)
    bf = BeautifulSoup(html, "lxml")
    texts = bf.find_all('div', class_='noveContent')
    texts = texts[0].text.replace('\u3000' * 2, '\n\n')
    # print(texts)
    return texts


def writer(name, path, text):
    savePath = path + "\\" + str(name) + ".txt"

    with open(savePath, 'a+', encoding='utf-8') as f:
        f.write(name.center(50) + '\n')
        print('正在下载' +name)

        f.writelines(text)
        f.write('\n\n')



if __name__ == '__main__':
    aa = '''
       1：书名
       2：作者
       '''
    print(aa)
    a = int(input('请选择输入书名还是作者进行查找：（书名|作者）'))
    begin=time.time()
    if a == 1:
        target = search1()  # 调用search1函数
    elif a==2:
        target = search2()

    k = get_download_url(target)
    end=time.time()
    print('程序所耗时间：',end-begin)
    toaster = ToastNotifier()
    toaster.show_toast("爬取完毕",
                       k,
                       icon_path="D:/suiji/image.ico",
                       duration=10)
