# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem


class WeibouserPipeline(object):
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            print(image_url)
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item


class WeiboVideoPipline(FilesPipeline):
    # 从item中取出分段视频的url列表并下载文件
    def get_media_requests(self, item, info):
        urls = item['video_urls']
        for url in urls:
            yield Request(url=url, meta={'item': item, 'index': urls.index(url)})

    # 自定义分段视频下载到本地的路径(以及命名), 注意该路径是 FILES_STORE 的相对路径
    def file_path(self, request, response=None, info=None):
        index = request.meta['index']  # 获取当前分段文件序号
        return "/%s.mp4" % index  # 返回路径及命名格式

    # 下载完成后, 将分段视频本地路径列表(FILES_STORE + 相对路径)填入到 item 的 file_paths
    # 这些请求将被管道处理，当它们完成下载后，结果将以2个元素的元组组成的列表形式传送到item_completed()方法。每个元组包含(success, file_info_or_error)：
    # results=(success, file_info_or_error)：
    # success是一个布尔值，当图片成功下载时为True ，因为某个原因下载失败为False。
    # file_info_or_error是一个包含下列关键字的字典（如果成功为True）或者出问题时为Twisted Failure 。
    #   url - 文件下载的url。这是从get_media_requests()方法返回请求的url。
    #   path - 文件存储的路径（相对于FILES_STORE）。
    #   checksum - 文件内容的MD5 hash

    def item_completed(self, results, item, info):
        item['video_paths'] = [self.store.basedir + x['path'] for ok, x in results if ok]
        return item


class WeiboUserVideoPipline(FilesPipeline):
    # 从item中取出分段视频的url列表并下载文件
    def get_media_requests(self, item, info):
        headers ={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/103.0.0.0 Safari/537.36'
            # 'cookie':"SINAGLOBAL=1709822810072.259.1658223272247; _s_tentry=-; "
            #          "Apache=889227180943.0352.1658559032141; "
            #          "ULV=1658559032192:2:2:2:889227180943.0352.1658559032141:1658223272575; "
            #          "XSRF-TOKEN=Yfl-f958_Hm08jZ0iTBQ4Zg1; "
            #          "SUB=_2A25P2H2bDeRhGeBL7FMY9SfFyTSIHXVsrOhTrDV8PUNbmtB-LVDlkW9NRvUjOguqsYFxX1czBTwbT4MVk9gkd2YG; "
            #          "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5Il4DJWM_fxzm436ObB32s5JpX5KzhUgL.FoqfS024SK"
            #          ".4eon2dJLoI7RLxK-LBo5L129NqPxoI5tt; ALF=1690124619; SSOLoginState=1658588619; "
            #          "WBPSESS=mgkxesxTEg75-VRgnRx8O482d2btMVGuLHqgyewpQOM93BZoClXhIOc9LqVhAxU6jbeV2bNfatVYrfT3bMFxzftg3IYjs5j9z08dAfF0zSxfoJaIJP9NuBJYkxwzODh2uG39wjFzXFiqPIQprsMZLw==; UPSTREAM-V-WEIBO-COM=b09171a17b2b5a470c42e2f713edace0 "
        }
        url = item['video_url']
        yield Request(url=url, meta={'item': item},headers=headers)

    # 自定义分段视频下载到本地的路径(以及命名), 注意该路径是 FILES_STORE 的相对路径
    def file_path(self, request, response=None, info=None):
        index = request.meta['item']['name']  # 获取当前分段文件序号
        return "/%s.mp4" % index  # 返回路径及命名格式

    def item_completed(self, results, item, info):
        item['video_path'] = [self.store.basedir + x['path'] for ok, x in results if ok]
        return item