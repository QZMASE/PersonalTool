# -*- coding: utf-8 -*-

import os
import random

pt="./images/"
image_name=os.listdir(pt)#linux下会丢弃前面的0，windows不会
random.shuffle(image_name)
for temp in image_name:
    print(temp.replace('.jpg',''))