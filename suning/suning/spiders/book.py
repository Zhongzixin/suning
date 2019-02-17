# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import re
class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com/']

    def parse(self, response):
        # 获取大分类的分组
        div_list = response.xpath("//div[@class='left-menu-container']/div[@class='menu-list']/div[@class='menu-item']")
        div_sub_list = response.xpath(
            "//div[@class='left-menu-container']/div[@class='menu-list']/div[@class='menu-sub']")
        for div in div_list:
            item = {}
            item["b_cate"] = div.xpath(".//h3/a/text()").extract_first()
            current_sub_list = div_sub_list[div_list.index(div)]
            p_list = current_sub_list.xpath('.//div[@class="submenu-left"]/p')
            for p in p_list:
                item['m_cate'] = p.xpath('.//a/text()').extract_first()
                s_list = p.xpath("./following-sibling::ul[1]/li")
                for s in s_list:
                    item['s_cate'] = s.xpath('.//a/text()').extract_first()
                    item['s_href'] = s.xpath('.//a/@href').extract_first()
                    yield scrapy.Request(
                        item['s_href'],
                        callback=self.parse_book_list,
                        meta={'item':item}
                    )


    def parse_book_list(self,response):
        item = response.meta['item']
        book_list = response.xpath("//li[contains(@class,'product      book')]")
        for book in book_list:
            item['book_name'] = book.xpath('.//div[@class="res-info"]/p[2]/a/text()').extract_first()
            item['book_href'] = book.xpath('.//div[@class="res-info"]/p[2]/a/@href').extract_first()
            item['book_store'] = book.xpath('.//div[@class="res-info"]/p[4]/a/text()').extract_first()
            print(item)