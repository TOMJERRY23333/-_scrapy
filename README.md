# -_scrapy
基于scrapy框架，获取微博博主发布的所有视频，并下载到本地（1080P）
### 如何运行？
在scrapy文件夹下的终端输入：scrapy run_spider.py u_v 
### 如何爬取指定博主视频？
在spiders/user_video.py 的spider类中，在名为uid的列表中添加目的博主ID
