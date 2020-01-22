# -*- coding: utf-8 -*-

import os

if __name__ == '__main__':
    file_txt = open("video.txt", mode = "w")
    files = sorted(os.listdir("."))
    for file in files:
        if ".mp4" in file:
            print(file.replace(".mp4", ""))
            file_txt.write(file.replace(".mp4", "") + "\n")
            cmd = "ffmpeg -i " + file.replace(" ", "\ ") + " 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//"
            file_txt.write(os.popen(cmd).read())
            cmd = "ffmpeg -i " + file.replace(" ", "\ ").replace(".mp4", ".ts") + " 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//"
            file_txt.write(os.popen(cmd).read())
    file_txt.close()