# -*- coding: utf-8 -*-

import os
import random

image_name = os.listdir("./image/")#获取文件名
num = round(len(image_name) * 0.2)#测试集数量，四舍五入取整
random.shuffle(image_name)#打乱数据集

#覆盖文件，若文件不存在自动创建
train = open("train.txt", "w")
test = open("test.txt", "w")

n = 0#循环累计
for temp in image_name:
    n = n + 1
    if n > num:
        train.write(temp.replace('.jpg','') + "\n")
    else:
        test.write(temp.replace('.jpg','') + "\n")
