import requests
from bs4 import BeautifulSoup
 
def get_chapter_urls(url):
    # 发送请求
    response = requests.get(url)
    # 创建BeautifulSoup对象
    soup = BeautifulSoup(response.text, 'html.parser')
    # 获取小说名字
    novel_name = soup.select_one('#novelName').text.strip()
    print(f"小说名称：{novel_name}\n")
 
    # 获取章节名字和url
    chapters = soup.select('.DivTd a')
    chapter_list = []
    for chapter in chapters:
        # 拼接章节URL
        chapter_url = 'https:' + chapter['href']
        # 获取完整的章节标题
        chapter_title = chapter['title']
        # 提取 "第" 字后面的部分作为新的章节标题
        chapter_title = chapter_title.split('第', 1)[1]
        # 将小说名称、章节标题和章节URL加入到章节列表中
        chapter_list.append((novel_name, chapter_title, chapter_url))
    return chapter_list
 
def save_chapter_content(novel_name, chapter_title, chapter_content):
    with open(f"{novel_name}.txt", mode='a', encoding='UTF-8') as f:
        f.write(f"章节：第{chapter_title}\n")
        f.write(f"内容：\n{chapter_content}\n\n")
 
 
def get_novel(url):
    # 调用get_chapter_urls函数以获取章节URL列表
    chapter_list = get_chapter_urls(url)
 
    for novel_name, chapter_title, chapter_url in chapter_list:
        # 发送请求以获取章节内容
        chapter_response = requests.get(chapter_url)
        # 使用BeautifulSoup解析响应文本
        chapter_soup = BeautifulSoup(chapter_response.text, 'html.parser')
        # 从解析结果中提取章节内容
        chapter_content = chapter_soup.select_one('.noveContent').text.strip()
 
        # 调用save_chapter_content函数保存章节内容
        save_chapter_content(novel_name, chapter_title, chapter_content)
 
        print(f"已保存章节：{chapter_title}")
 
    print("全部章节保存完成！")
 
 
url = 'https://b.faloo.com/1328711.html'
get_novel(url)
