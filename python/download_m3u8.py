# -*- coding: utf-8 -*-

import os
import re
import threading
import time
import requests
from queue import Queue
import shutil
import platform

class M3U8:
    temp_dir = "./temp/"# 缓存路径
    down_dir = "./download/"# 下载完成目录
    temp_file = temp_dir + 'temp.txt'# 缓存文件路径
    sum_ts = 0# ts文件总数
    num_ts = 0# 当前ts文件下载数量
    headers = {# 包头
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/78.0.3904.97 Safari/537.36'
    }
    url = ""# 链接地址
    base_url = ""# 链接头
    filename = ""# 文件名
    ts_queue = Queue(10000)
    
    def __init__(self, url, base_url = ""):
        self.url = url
        self.base_url = base_url
        
        if os.path.exists(self.temp_dir):# 判断文件夹是否存在
            if os.listdir(self.temp_dir):# 缓存路径存在文件
                shutil.rmtree(self.temp_dir)
                os.mkdir(self.temp_dir)
        else:
            os.mkdir(self.temp_dir)
        if not os.path.exists(self.down_dir):
            os.mkdir(self.temp_dir)
        
    def analysis(self):
        # 请求链接并转化为文本
        if 'http' in self.url:# 判断是本地路径还是网络路径
            self.filename = re.search('([a-zA-Z0-9-_]+.m3u8)', self.url).group(1).strip()# 从line中提取文件名
            resp = requests.get(self.url, headers=self.headers)
            m3u8_text = resp.text
        else:
            self.filename = self.url
            file = open(self.url)
            m3u8_text = file.read()
            file.close()
        lines = m3u8_text.split('\n')# 按行拆分m3u8文档
        self.filename = self.filename.replace(".m3u8", ".ts")
    
        file = open(self.temp_file, mode='a+')
        for i,line in enumerate(lines):
            if '.ts' in line:# 找到文档中含有ts字段的行
                if 'http' in line:# 检查ts文件链接是否完整，若不完整需拼凑
                    self.ts_queue.put(line)
                else:
                    line = self.base_url + line
                    self.ts_queue.put(line)
                name = re.search('([a-zA-Z0-9-_]+.ts)', line).group(1).strip()# 从line中提取文件名
                file.write("%s\n" % name)# 保存文件顺序
        file.close()
        
    def run(self, ts_queue, headers):
        while not ts_queue.empty():
            url = ts_queue.get()
            filename = re.search('([a-zA-Z0-9-_]+.ts)', url).group(1).strip()
            try:
                requests.packages.urllib3.disable_warnings()
                r = requests.get(url, stream=True, headers=self.headers, verify=False, timeout=(10, 20))
                with open(self.temp_dir + "temp_" + filename, 'wb') as fp:
                    for chunk in r.iter_content(5242):
                        if chunk:
                            fp.write(chunk)
                shutil.move(self.temp_dir + "temp_" + filename, self.temp_dir + filename)
                self.num_ts += 1
                print("\r", filename, '下载成功，进度', self.num_ts , "/", self.sum_ts, end="", flush=True)# 刷新显示进度
            except:
                print('任务文件', filename, '下载失败')
                ts_queue.put(url)
        
    def download(self):
        self.sum_ts = self.ts_queue.qsize()
        if self.sum_ts > 5:
            sum_threads = self.sum_ts // 5
        else:
            sum_threads = 1
        if sum_threads > 50:
            sum_threads = 50
        threads = []
        for i in range(sum_threads):
            t = threading.Thread(target=self.run, name='th-' + str(i), kwargs={'ts_queue': self.ts_queue, 'headers': self.headers})
            t.setDaemon(True)
            threads.append(t)
        for t in threads:
            time.sleep(0.4)
            t.start()
        for t in threads:
            t.join()
        print('\n')
            
    def merge(self):
        file = open(self.temp_file)
        lines = file.readlines()
        file.close()
        
        i = 0
        for line in lines:
            line = line.strip("\n")
            i += 1
            os.rename(self.temp_dir + str(line), self.temp_dir + str(i).zfill(5) + ".ts")

        system = platform.system()
        if system == "Windows":
            cmd = "copy /b *.ts temp.ts"
        elif system == "Linux":
            cmd = "cat *.ts > temp.ts"
        
        os.chdir(self.temp_dir)
        os.system(cmd)
        os.chdir("..")
        shutil.move(self.temp_dir + "temp.ts", self.down_dir + self.filename)
        if 'http' not in self.url:# 如果是本地文件
            shutil.move(self.url, self.down_dir + self.url)
        shutil.rmtree(self.temp_dir)


if __name__ == '__main__':
    files = sorted(os.listdir("."))
    for file in files:
        if ".m3u8" in file:
            m3u8 = M3U8(url = file)
            print("解析开始**********************************************")
            m3u8.analysis()
            print("解析结束**********************************************")
            print("下载开始**********************************************")
            m3u8.download()
            print("下载结束**********************************************")
            print("合并开始**********************************************")
            m3u8.merge()
            print("合并结束**********************************************")
        

