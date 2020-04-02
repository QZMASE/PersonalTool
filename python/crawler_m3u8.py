# -*- coding: utf-8 -*-

import requests
import random
import time
import re
import os

class CRAWLER:
    down_dir = "./download/"# 下载目录
    fail_file = down_dir + "fail.txt"# 缓存失败的路径
    url = ""# 链接地址
    headers = {# 包头
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/78.0.3904.97 Safari/537.36'
    }
    title = ""# 标题
    requests_flag = False# 请求标志位，默认请求失败False，请求成功True
    requests_num = 5# 请求次数

    def __init__(self, url, title=""):
        self.url = url
        self.title = title

        if not os.path.exists(self.down_dir):
            os.mkdir(self.down_dir)

    def requests_fail(self, title, url):
        # 打开文件只用于写入，若文件存在则在末尾添加，若文件不存在则创建新文件
        with open(self.fail_file, mode='a+', encoding='utf-8') as file:
            file.write("%s\n" % title)
            file.write("%s\n" % url)
        print("请求失败！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！\n")

    def requests_url(self):
        while(self.requests_num):
            self.requests_num -= 1
            try:
                time.sleep(random.random())# 随机暂停0~1秒
                text = requests.get(self.url, headers=self.headers, timeout=(10, 20))
            except:
                self.requests_flag = False
            else:
                self.requests_num = 0
                self.requests_flag = True
        else:
            if self.requests_flag == True:
                return text
            else:
                self.requests_fail(self.title, self.url)
                return None


class JPG(CRAWLER):
    def __init__(self, url, title=""):
        CRAWLER.__init__(self, url, title)
        self.fail_file = self.down_dir + "fail_jpg.txt"# 覆写缓存失败的路径

    def get_jpg(self):
        jpg = self.requests_url()
        if(self.requests_flag == True):
            # 以二进制格式打开只用于写入。若文件存在则覆盖。若文件不存在，创建新文件
            with open(self.down_dir + self.title + ".jpg", 'wb') as file:
                for chunk in jpg.iter_content(5242):
                    if chunk:
                        file.write(chunk)


class HTML(CRAWLER):
    text = ""# 链接内html内容
    
    def __init__(self, url, title=""):
        CRAWLER.__init__(self, url, title)
        fail_file = self.down_dir + "fail_url.txt"# 覆写缓存失败的路径

        self.text = self.requests_url()
        if self.requests_flag == True:
            self.text = self.text.text

    def save(self, filename="temp.html"):
        if self.requests_flag == True:
            # 打开文件只用于写入，若文件存在则覆盖。若文件不存在，创建新文件
            with open(self.down_dir+filename, 'w', encoding='utf-8') as file:
                file.write(self.text)

    # 返回正则表达式在字符串中所有匹配结果的列表
    def find(self, regex):
        lists = re.findall(regex, self.text)
        return lists


def get_m3u8(src_url, title=""):
    print("原始地址 %s" % src_url)

    m3u8 = HTML(src_url, title)
    url = m3u8.find(r"http.*.m3u8")[0].replace("\/", "/")
    if title == "":
        title = m3u8.find(r"<title>(.*)</title>")[0]
    print("第一层地址 %s" % url)

    m3u8 = HTML(url, title)
    if m3u8.requests_flag == True:
        url = url.replace("index.m3u8", "") + m3u8.find(r".*.m3u8")[0]
        url = "/".join(list(dict.fromkeys(url.split("/"))))# 去除重复字符串
        print("第二层地址 %s" % url)
        
        base_url = url.replace("index.m3u8", "")# 提取当前基础路径
        m3u8 = HTML(url, title)
        if m3u8.requests_flag == True:
            m3u8.save("temp.m3u8")
            temps = m3u8.find(r"([a-zA-Z0-9-_]+.ts)")
            # 打开文件只用于写入，若文件存在则覆盖，若文件不存在则创建新文件
            with open(m3u8.down_dir + title + ".m3u8", mode='w', encoding='utf-8') as file:
                for temp in temps:
                    ts_url = base_url + temp
                    file.write("%s\n" % ts_url)

            # 打开文件只用于写入，若文件存在则在末尾添加，若文件不存在则创建新文件
            with open(m3u8.down_dir + "！！！totle.txt", mode='a+', encoding='utf-8') as file:
                file.write("%s\n" % title)
                file.write("%s\n\n" % url)


if __name__=='__main__':
    url_site = ""# 网站域名
    url_head = ""# 批量爬取网页头
    url_tail = ""# 批量爬取网页尾
    for i in range(1, 2):
        print("********************************************************************************************当前在第%s页" % i)
        html_total = HTML(url_head + str(i) + url_tail)
        title_totle = html_total.find(r'<span class="nn">(.*)</span>')
        jpg_totle = html_total.find(r'src="(.*.jpg)"')
        url_totle = html_total.find(r'<a href="(.*html)" target')
        for j in range(len(title_totle)):
            print(title_totle[j])
            print(url_totle[j])
            title_totle[j] = re.sub(r"[\/\\\:\*\?\"\<\>\|]", " ", title_totle[j])# 替换win下非法字符，'/ \ : * ? " < > |'

            # 下载图片
            jpg = JPG(jpg_totle[j], title_totle[j])
            jpg.get_jpg()

            # 下载m3u8文件
            url_detil = HTML(url_site + url_totle[j])
            get_m3u8(url_site + url_detil.find(r'<li><a href="(.*)" target')[0], title_totle[j])

            print()


    # with open("", encoding='utf-8') as file:
    #     text = file.read()
    #     lines = text.splitlines()
    #     for line in lines:
    #         if "http" not in line:# 非网址页
    #             title = line
    #             print(title)
    #         else:
    #             get_m3u8(line, title)
    #             print()
        
