# -*- coding: utf-8 -*-

import os

if __name__ == '__main__':
    files = sorted(os.listdir("."))
    for file in files:
        if ".mp4" in file:
            name = file.split(" ")
            ole = name[0]
            new = name[0].upper()
            if ole != new:
                os.rename(file, file.replace(ole, new))