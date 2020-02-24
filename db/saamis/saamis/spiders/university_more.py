# -*- coding: utf-8 -*-
import scrapy
import urllib
from saamis.items import SaamisItem
from copy import deepcopy
from collections import defaultdict
import pprint

class UniversityMoreSpider(scrapy.Spider):
    name = 'university_more'
    allowed_domains = ['usnews.com']
    start_urls = ['https://www.usnews.com/education/best-global-universities/rankings']

    def parse(self, response):
        item = SaamisItem()
        div_list = response.xpath('//div[@class="sep"]')
        for div in div_list:
            item=deepcopy(item)
            item['Name'] = div.xpath('.//div[@class="block unwrap"]/h2/a/text()').extract_first().replace('\n', '').replace('\r', '')
            url = div.xpath('.//div[@class="block unwrap"]/h2/a/@href').extract_first()
            yield scrapy.Request(
                        url,
                        callback=self.parse_detail,
                        meta = {"item":item},
                    )
        next_url = response.xpath('//a[contains(text(),"Next")]/@href').extract_first()
        next_url = urllib.parse.urljoin(response.url,next_url)
        if(next_url is not None):
            yield scrapy.Request(
                        next_url,
                        callback=self.parse,
                        meta = {"item":item},
                        #dont_filter=True
                    )

    def parse_detail(self, response):
        item = response.meta["item"]
        kv_list=response.xpath('''//div[@class="t-slack sep"]''')
        subject_rankings={}
        if(kv_list is not None):
            for kv in kv_list:
                k=kv.xpath('''./div[@class="t-dim"]/text()''').extract_first().strip()
                v=kv.xpath('''./div[@class="right t-strong"]/text()''').extract_first().strip().replace('\n', '').replace('\r', '')
                subject_rankings[k]=v
            item['subject_rankings']=subject_rankings
        yield item

