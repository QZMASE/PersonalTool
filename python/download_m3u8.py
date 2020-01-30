# -*- coding: utf-8 -*-

import os
import re
import threading
import time
import requests
import queue
import shutil
import platform
import sys
import getopt

class M3U8:
    temp_dir = "./temp/"# 缓存路径
    down_dir = "./download/"# 下载完成目录
    temp_file = temp_dir + 'temp.txt'# 缓存文件路径
    sum_ts = 0# ts文件总数
    num_ts = 0# 当前ts文件下载数量
    flag_save = False
    headers = {# 包头
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/78.0.3904.97 Safari/537.36'
    }
    m3u8 = ""# m3u8文件
    base_url = ""# 链接头
    filename = ""# 文件名
    ts_queue = queue.Queue()
    
    def __init__(self, m3u8, flag_save, base_url = ""):
        self.m3u8 = m3u8
        self.flag_save = flag_save
        self.base_url = base_url
        self.filename = self.m3u8.replace(".m3u8", ".ts")
        
        if os.path.exists(self.temp_dir):# 判断文件夹是否存在
            if os.listdir(self.temp_dir):# 缓存路径存在文件
                shutil.rmtree(self.temp_dir)
                os.mkdir(self.temp_dir)
        else:
            os.mkdir(self.temp_dir)
        if not os.path.exists(self.down_dir):
            os.mkdir(self.temp_dir)
        
    def analysis(self):
        file = open(self.m3u8)
        m3u8_text = file.read()
        file.close()
        lines = m3u8_text.split('\n')# 按行拆分m3u8文档
        
        file = open(self.temp_file, mode="w")# 打开文件只用于写入，若文件不存在则创建
        for line in lines:
            if '.ts' in line:# 找到文档中含有ts字段的行
                if 'http' in line:# 检查ts文件链接是否完整，若不完整需拼凑
                    self.ts_queue.put(line)
                else:
                    line = self.base_url + line
                    self.ts_queue.put(line)
                name = re.search('([a-zA-Z0-9-_]+.ts)', line).group(1).strip()# 从line中提取文件名
                file.write("%s\n" % name)# 保存文件顺序，用于后面合并前的重命名
        file.close()
        
    def run(self):
        while not self.ts_queue.empty():
            url = self.ts_queue.get()
            name = re.search('([a-zA-Z0-9-_]+.ts)', url).group(1).strip()
            try:
                requests.packages.urllib3.disable_warnings()
                r = requests.get(url, stream=True, headers=self.headers, verify=False, timeout=(10, 20))
                # 以二进制格式打开只用于写入。若文件存在则覆盖。若文件不存在，创建新文件
                with open(self.temp_dir + name, 'wb') as fp:
                    for chunk in r.iter_content(5242):
                        if chunk:
                            fp.write(chunk)
            except:
                print(name, "下载失败")
                self.ts_queue.put(url)
            else:
                # 使用ffmpeg检查完整性
                cmd = "ffmpeg -i " + self.temp_dir + name + " 2>&1"
                result = os.popen(cmd).read().splitlines()
                if "Invalid data" in result[-1]:# 文件错误，重新下载
                    print(name, "文件错误，重新下载")
                    self.ts_queue.put(url)
                else:
                    self.num_ts += 1
                    print("\r", name, "下载成功，进度", self.num_ts , "/", self.sum_ts, end="", flush=True)# 刷新显示进度

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
            t = threading.Thread(target=self.run, name='th-' + str(i))
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
        lines = file.readlines()# 读取缓存的文件名
        file.close()
        
        i = 0
        for line in lines:
            line = line.strip("\n")
            i += 1
            # 按照文件名顺序进行重命名，防止合并顺序出错
            os.rename(self.temp_dir + str(line), self.temp_dir + str(i).zfill(5) + ".ts")

        system = platform.system()# 不同的操作系统合并命令不一样
        if system == "Windows":
            cmd = "copy /b *.ts temp.ts"
        elif system == "Linux":
            cmd = "cat *.ts > temp.ts"
        
        os.chdir(self.temp_dir)# 进入缓存文件夹
        os.system(cmd)# 执行合并操作
        os.chdir("..")
        shutil.move(self.temp_dir + "temp.ts", self.down_dir + self.filename)# 移动合并文件到下载文件夹
        shutil.move(self.m3u8, self.down_dir + self.m3u8)# 移动m3u8文件到下载文件夹
        if flag_save:# 若保存缓存文件夹
            os.rename(self.temp_dir, self.down_dir + self.m3u8.replace(".m3u8", ""))
        else:
            shutil.rmtree(self.temp_dir)# 清理缓存文件夹


def analysis_parameter(argv):
    flag = False
    try:
        opts, args = getopt.getopt(argv, "s", ["save"])
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-s", "--save"):
            flag = True
    return flag


if __name__ == '__main__':
    files = sorted(os.listdir("."))
    flag_save = analysis_parameter(sys.argv[1:])
    for file in files:
        if ".m3u8" in file:
            m3u8 = M3U8(file, flag_save)
            print("解析开始**********************************************")
            m3u8.analysis()
            print("解析结束**********************************************")
            print("下载开始**********************************************")
            m3u8.download()
            print("下载结束**********************************************")
            print("合并开始**********************************************")
            m3u8.merge()
            print("合并结束**********************************************")
        

