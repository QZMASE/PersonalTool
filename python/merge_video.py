import os

if __name__ == '__main__':
    filenames = sorted(os.listdir("."))
    # 打开文件只用于写入，若文件存在则在末尾添加，若文件不存在则创建新文件
    with open("filelist.txt", mode='a+', encoding='utf-8') as txt:
        for filename in filenames:
            if ".py" not in filename and ".txt" not in filename:
                txt.write("file '%s'\n" % filename)
                extensions = os.path.splitext(filename)[1]# 获取文件后缀

    cmd = "ffmpeg -f concat -i filelist.txt -vcodec copy -acodec copy output" + extensions
    os.system(cmd)# 执行合并操作
