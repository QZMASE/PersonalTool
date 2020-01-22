
<h1 align="center">👉PersonalTool👈</h1>
<p align="center">食之无味，弃之可惜</p>

个人工具集合，日常编程写的一些小工具，汇集了bat，cpp，python，shell，保留在github上，免得日后重复造轮子

- [bat](#bat)
  - [clear python.bat](#clear-pythonbat)
  - [clear vs.bat](#clear-vsbat)
  - [JpgToTxt.bat](#jpgtotxtbat)
  - [LibToTxt.bat](#libtotxtbat)
  - [ts2mp4.bat](#ts2mp4bat)
- [cpp](#cpp)
  - [image_fill.cpp](#image_fillcpp)
  - [image_resize.cpp](#image_resizecpp)
  - [image_roi.cpp](#image_roicpp)
  - [image_save.cpp](#image_savecpp)
  - [image_xml.cpp](#image_xmlcpp)
- [python](#python)
  - [image_random_data.py](#image_random_datapy)
  - [download_m3u8.py](#download_m3u8py)
  - [crawler_m3u8.py](#crawler_m3u8py)
  - [ffmpeg_get_time.py](#ffmpeg_get_timepy)
  - [upper_lower_case.py](#upper_lower_casepy)
- [shell](#shell)
  - [clean_update.sh](#clean_updatesh)
  - [configure.sh](#configuresh)
  - [ts2mp4.sh](#ts2mp4sh)


# bat
## clear python.bat
- 2019.01.09，清理python产生的缓存文件
  
## clear vs.bat
- 2019.01.09，清理Visual Studio产生的缓存文件

## JpgToTxt.bat
- 2019.01.09，将当前文件夹下“.jpg”文件的文件名缓存至“img.txt”
  
## LibToTxt.bat
- 2019.01.09，将当前文件夹下“.lib”文件的文件名缓存至“lib.txt”

## ts2mp4.bat
- 2019.12.28，使用ffmpeg将当前文件夹下“.ts”文件转码为“.mp4”


# cpp
## image_fill.cpp
- 2019.01.09， 使用opencv批量填充图像，填充颜色可在cpp内调整（默认黑色），该操作是覆盖操作，请保存好原始文件，图像文件需存放在“Path”路径（可在cpp文件内修改）下，同时“Path”路径下需要有“img.txt”（使用“JpgToTxt.bat”生成）缓存好所有图像文件名（不包括路径）

## image_resize.cpp
- 2019.01.09， 使用opencv批量放缩图像，放缩比例可在cpp内调整（默认缩放成宽64高48），该操作是覆盖操作，请保存好原始文件，图像文件需存放在“Path”路径（可在cpp文件内修改）下，同时“Path”路径下需要有“img.txt”（使用“JpgToTxt.bat”生成）缓存好所有图像文件名（不包括路径）

## image_roi.cpp
- 2019.01.09， 使用opencv批量截取图像，截取ROI可在cpp内调整，图像文件需存放在“Path”路径（可在cpp文件内修改）下，同时“Path”路径下需要有“img.txt”（使用“JpgToTxt.bat”生成）缓存好所有图像文件名（不包括路径），截取图像缓存至“Path”路径，生成的文件名前缀“000-”，后缀为“img.txt”中顺序

## image_save.cpp
- 2019.01.09， 使用opencv批量截取摄像头图像，按“空格键”截图图像，截取图像缓存至“Path”路径（可在cpp文件内修改），生成的文件名为截取顺序

## image_xml.cpp
- 2019.01.09， 使用opencv对“Mat”、“xml”进行读写转换，默认“Mat”为cpp路径下的“image.jpg”，默认“xml”为cpp路径下的“MatFile.xml”


# python
## image_random_data.py
- 2019.02.10， 打乱数据集，读取指定路径下所有文件名，按照指定比例生成“train.txt”、“test.txt”，默认不包含“.jpg”后缀

## download_m3u8.py
- 2020.01.19，读取同目录下所有m3u8文件，使用多线程下载并合并，含失败重启机制，支持linux和Windows，默认文件名为m3u8文件名，缓存路径在“temp_dir”设置（程序开始运行会自动清理），保存路径在“down_dir”设置
- 2020.01.22，精简程序

## crawler_m3u8.py
- 2020.01.19，爬取同目录下“http.txt”文件中所有网页中的m3u8文件，并缓存最终ts分片路径，缓存文件名默认为网页标题。该爬虫操作高度自定义，若需使用需要自行修改

## ffmpeg_get_time.py
- 2020.01.20，调用ffmpeg获取当前文件夹下视频时长至“video.txt”文件，首先获取“.mp4”文件，再获取同名“.ts”文件

## upper_lower_case.py
- 2020.01.20，重命名大小写


# shell
若提示无执行权限，执行命令 chmod +x ./xxx.sh 

## clean_update.sh
- 2019.01.22，清理、升级Ubuntu

## configure.sh
- 2019.01.22，安装完Ubuntu16.04后进行系统配置，修改菜单栏位置、修改系统时间、禁用自动挂载、删除无用软件、安装exFAt格式U盘软件、清理缓存

## ts2mp4.sh
- 2020.01.02，使用ffmpeg将当前文件夹下“.ts”文件转码为“.mp4”