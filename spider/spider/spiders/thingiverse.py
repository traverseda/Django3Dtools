# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from spider.items import ProjectItem, fileObjectItem
from scrapy.contrib.linkextractors import LinkExtractor
import re

class ThingiverseSpider(CrawlSpider):
    name = "thingiverse"
    allowed_domains = ["thingiverse.com"]
    start_urls = (
        'http://www.thingiverse.com/thing:446851',
    )
    ##Find the links.
    def parse(self, response):
        design = LinkExtractor(allow=('design')).extract_links(response)
        if design:
            yield scrapy.http.Request(url=design[0].url, callback=self.projectGet)
        if re.search('thing:\d\d+',response.url):
            yield scrapy.http.Request(url=response.url, callback=self.project)


    def projectGet(self, response):
        objects = LinkExtractor(allow=('thing:\d\d+')).extract_links(response)
        for i in objects:
            yield scrapy.http.Request(url=i.url, callback=self.project)

    def project(self,response):
        projectObject=ProjectItem()
        hxs = response.selector.xpath('//*[contains(@class,\'thing-file\')]')
        hxs.pop(0)
        print(projectObject)
        pass