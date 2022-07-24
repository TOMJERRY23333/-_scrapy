# coding:utf-8
"""
个人博客视频抓取
date = 2022年7月24日 13点48分
"""

import scrapy
from scrapy import Request, Spider
import json
from scrapy.shell import inspect_response
from items import weibouservideoItem


class UserVideoSpider(Spider):
    name = 'user_video'
    allowed_domain = ['weibo.com', 's.weibo.com']
    scheme = 'https://'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'cookie': "SINAGLOBAL=1709822810072.259.1658223272247; _s_tentry=-; Apache=889227180943.0352.1658559032141; ULV=1658559032192:2:2:2:889227180943.0352.1658559032141:1658223272575; XSRF-TOKEN=Yfl-f958_Hm08jZ0iTBQ4Zg1; SUB=_2A25P2H2bDeRhGeBL7FMY9SfFyTSIHXVsrOhTrDV8PUNbmtB-LVDlkW9NRvUjOguqsYFxX1czBTwbT4MVk9gkd2YG; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5Il4DJWM_fxzm436ObB32s5JpX5KzhUgL.FoqfS024SK.4eon2dJLoI7RLxK-LBo5L129NqPxoI5tt; ALF=1690124619; SSOLoginState=1658588619; WBPSESS=mgkxesxTEg75-VRgnRx8O482d2btMVGuLHqgyewpQOM93BZoClXhIOc9LqVhAxU6jbeV2bNfatVYrfT3bMFxzftg3IYjs5j9z08dAfF0zSxfoJaIJP9NuBJYkxwzODh2uG39wjFzXFiqPIQprsMZLw==; UPSTREAM-V-WEIBO-COM=b09171a17b2b5a470c42e2f713edace0"
    }

    def start_requests(self):

        uids = ['5768168516']
        for uid in uids:
            url = f'https://weibo.com/ajax/profile/getWaterFallContent?uid={uid}&cursor='
            yield Request(url+str(0),callback=self.parse, headers=self.headers)

    def parse(self, response):
        # inspect_response(response,self)
        url = 'https://weibo.com/ajax/profile/getWaterFallContent?uid=5768168516&cursor='
        dic = json.loads(response.text)
        next_cursor = dic['data']['next_cursor']
        self.logger.info('next_cursor: %s',next_cursor)
        # 调用自身
        if next_cursor != -1:
            yield Request(url+next_cursor, callback=self.parse, headers=self.headers)

        video_list = dic['data']['list']
        for i in video_list:
            item = weibouservideoItem()

            item['name'] = i['page_info']['cards'][0]['content2']
            item['video_url'] = i['page_info']['media_info']['playback_list'][0]['play_info']['url']
            yield item


