import scrapy
from scrapy.selector import Selector

from selenium import webdriver
from time import sleep


class GetdataSpider(scrapy.Spider):
    name = 'getdata'
    allowed_domains = ['https://www.immowelt.de/']
    start_urls = ['https://www.immowelt.de/liste/berlin/wohnungen/mieten?sort=price']

    def parse(self, response):
        url = 'https://www.immowelt.de/liste/berlin/wohnungen/mieten?sort=price'
        
        #insert your driver path
        self.driver = webdriver.Chrome('/Users/maxl/chromedriver/chromedriver')
        #
        #
        #
        self.driver.get(url)
        #create Selector
        sel = Selector(text=self.driver.page_source)
