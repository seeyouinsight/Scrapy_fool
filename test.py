import requests
import re
import os

def bug(id):
    sum = 1
    url1 = "https://b.faloo.com/"+id+".html"
    html1 = requests.get(url1)
    length_ml = len(re.findall(r'<a href=.+? target="_self" title=.+?',html1.text))
    title = re.search(r'<title>.+?</title>',html1.text)
    title = title.group(0).strip("<title></title>")

    print(title+":共"+str(length_ml)+'章')

    try:
        os.mkdir(os.getcwd()+'\\'+title)
    except FileExistsError:
        return title
        return 0

    while sum < length_ml:
        url2 = "https://b.faloo.com/"+id+"_"+str(sum)+".html"
        html2 = requests.get(url2)
        titles = re.search(r"<title>.+?</title>",html2.text)
        titles = titles.group(0).strip("<title></title>")
        print("正在爬取第"+str(sum)+"章:"+titles)
        tt = os.getcwd()+'\\'+title+'\\'+titles+".txt"
        with open(tt,'w',encoding="utf-8") as fp:
            txt = re.findall(r'<p>.+?</p>',html2.text)
            if txt == "[]":
                print('第'+str(sum)+"章:"+titles+"爬取失败")
                break
            else:
                for i in txt:
                    fp.write(i.strip("<p></p>")+'\n')
                print('第'+str(sum)+"章:"+titles+"爬取成功")
        sum += 1

    return title
def GL(title):
    path = os.getcwd() + '\\' + title
    names = os.listdir(path)
    length = len(names)
    sum = 0
    while sum < length:
        if ".txt" in names[sum]:
            with open(path+'\\'+names[sum],'r',encoding="utf-8") as fp:
                size = os.path.getsize(path+'\\'+names[sum])
                if size < 1000:
                    flag = True
                    debug = False
                else:
                    flag = False
            if flag == True:
                os.remove(path+'\\'+names[sum])
                print("无效文件"+names[sum]+"已删除")
            else:
                debug = True
            sum += 1
    if debug == True:
        print("无效文件已全部删除")
    else:
        print("无效文件还没删除")

def main():
    id = input("请输入漫画id>>>")
    title = bug(id)
    GL(title)


if __name__ == '__main__':
    main()


