# -*- coding: utf-8 -*-

import requests
import re
import os

class URL:
    down_dir = "./download/"# 下载目录
    fail_file = down_dir + "fail.txt"# 缓存失败的路径
    headers = {# 包头
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/78.0.3904.97 Safari/537.36'
    }
    url = ""# 链接地址
    htlm = ""# 链接内html内容
    title = ""# 网页标题
    requests_flag = True# 请求标志位，默认请求成功True，请求失败False
    
    def __init__(self, url):
        self.url = url

        self.html = self.requests_url(self.url).text
        if self.requests_flag == True:
            self.title = self.find(r'<title>+.+</title>')[0].replace("<title>", "").replace("</title>", "")
            
            if not os.path.exists(self.down_dir):
                os.mkdir(self.temp_dir)

    # url.save("temp.html")
    def save(self, filename):
        file = open(self.down_dir+filename, 'w', encoding='utf-8')
        file.write(self.html)
        file.close()

    # 返回正则表达式在字符串中所有匹配结果的列表
    def find(self, regex):
        lists = re.findall(regex, self.html)
        # print(list)
        return lists

    def requests_fail(self):
        file = open(self.fail_file, mode='a+')
        file.write("%s\n" % self.url)
        file.close()
        requests_flag = False
        print("请求失败！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！\n")

    def requests_url(self, url):
        try:
            text = requests.get(url, headers=self.headers, timeout=(10, 20))
        except:
            requests_fail()
            return None
        else:
            return text

    def get_m3u8(self, lists):
        print(self.url)
        if self.requests_flag == True:
            print(self.title)
            m3u8_url = lists[0].split("=")[-1]# 第一层只有一个m3u8文件
            print("第一层地址", m3u8_url)

            m3u8_text = self.requests_url(m3u8_url).text
            if self.requests_flag == True:
                m3u8_text = m3u8_text.split('\n')
                for m3u8_text_list in m3u8_text:
                    if ".m3u8" in m3u8_text_list:# 找到第二层m3u8文件地址
                        print("第二层地址", m3u8_text_list)
                        url = "https://v.ff-cdn.com/" + m3u8_text_list# 合成地址
                        # url = m3u8_url.replace("index.m3u8", "") + m3u8_text_list# 合成地址
                        base_url = url.replace("index.m3u8", "")# 提取当前基础路径

                        text = self.requests_url(url)
                        if self.requests_flag == True:
                            if text.status_code != 200:
                                requests_fail()
                            else:
                                file = open(self.down_dir + self.title + ".m3u8", mode='a+')
                                text = text.text.split('\n')
                                for text_line in text:
                                    if ".ts" in text_line:
                                        ts_url = base_url + re.findall(r'([a-zA-Z0-9-_]+.ts)', text_line)[0]
                                        file.write("%s\n" % ts_url)  
                                file.close()
                                print()


if __name__=='__main__':
    file = open("http.txt")
    text = file.read()
    file.close()
    lines = text.split('\n')
    for line in lines:
        if "http" in line:
            url = URL(line)
            url.get_m3u8(url.find(r'<iframe src="([^"]+\.m3u8)"'))# 爬取网页内m3u8地址，<iframe src="/packs/dplayer/?url=

                