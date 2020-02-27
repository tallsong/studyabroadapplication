# -*- coding: utf-8 -*-
import scrapy
import urllib
from saamis.items import SaamisItem
from copy import deepcopy
from collections import defaultdict
import pprint
class UniversitylistSpider(scrapy.Spider):
    name = 'universitylist'
    allowed_domains = ['usnews.com']
    start_urls = ['https://www.usnews.com/education/best-global-universities/rankings']
    def parse(self, response):
        item = SaamisItem()
        div_list = response.xpath('//div[@class="sep"]')
        for div in div_list:
            item=deepcopy(item)
            item['GlobalRank'] = div.xpath('./div[contains(@class,"thumb-left")]/span/text()').extract_first()
            item['GlobalRank'] = int(item['GlobalRank'].replace('#',''))
            item['Name'] = div.xpath('.//div[@class="block unwrap"]/h2/a/text()').extract_first().replace('\n', '').replace('\r', '')
            item['Country'] = div.xpath('.//div[@class="t-taut"]/span[1]/text()').extract_first()
            item['City'] = div.xpath('.//div[@class="t-taut"]/span[2]/text()').extract_first()
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
        item['Address']='\n'.join(response.xpath('''//h2[text()="Address"]/../div[1]/text()''').extract())   # list
        item['Website'] = response.xpath('''//h2[text()="Website"]/../a/@href''').extract_first()
        #item['Summary']=''.join(''.join(response.xpath('//div[@data-test-id="summary-blurb"]/text()').extract()).strip().replace('\n', '').replace('\r', ''))
        item['Summary'] = response.xpath('string(//div[@data-test-id="summary-blurb"])').extract_first()
        if(response.xpath('//div[@id="mapThumb"]/@data-long').extract_first() is not None):
            item['data_long']=float(response.xpath('//div[@id="mapThumb"]/@data-long').extract_first())
            item['data_lat']=float(response.xpath('//div[@id="mapThumb"]/@data-lat').extract_first())
        else:
            item['data_long']=None
            item['data_lat']=None
        item['data_url']=response.url
        yield item
