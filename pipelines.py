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


class WeiboUserVideoPipline(FilesPipeline):
    # 从item中取出分段视频的url列表并下载文件
    def get_media_requests(self, item, info):
        headers ={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/103.0.0.0 Safari/537.36'
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
